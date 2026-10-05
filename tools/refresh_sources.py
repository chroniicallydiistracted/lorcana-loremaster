#!/usr/bin/env python3
"""Refresh registered public official sources; never infer/update game policy."""
import argparse
from datetime import date, datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href', '')
            if '.pdf' in href.lower():
                self.urls.add(href)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--as-of', default=datetime.now(ZoneInfo('America/Phoenix')).date().isoformat(),
                   help='Verification date in the user timezone (default America/Phoenix).')
    p.add_argument('--only', nargs='+', help='Source IDs from sources/manifest.json.')
    args = p.parse_args(); date.fromisoformat(args.as_of)
    path = ROOT / 'sources/manifest.json'; manifest = json.loads(path.read_text())
    if args.only:
        unknown = set(args.only) - {r['source_id'] for r in manifest['sources']}
        if unknown:
            raise ValueError('Unknown source IDs: ' + ', '.join(sorted(unknown)))
    results, failed, discovered = [], False, []
    for rec in manifest['sources']:
        if rec['source_id'] == 'ravensburger-catalog-en' or (args.only and rec['source_id'] not in args.only):
            continue
        try:
            req = urllib.request.Request(rec['url'], headers={'User-Agent': 'LorcanaLoremaster/1.0 source verification'})
            with urllib.request.urlopen(req, timeout=20) as response:
                content = response.read(); resolved_url = response.url
            is_pdf = urllib.parse.urlparse(rec['url']).path.lower().endswith('.pdf')
            if is_pdf and not content.startswith(b'%PDF'):
                raise ValueError('Expected PDF; received another document type.')
            digest = hashlib.sha256(content).hexdigest()
            directory = ROOT / 'sources/official' / args.as_of
            directory.mkdir(parents=True, exist_ok=True)
            name = rec['source_id'] + ('.pdf' if is_pdf else '.html')
            dest = directory / name
            if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() != digest:
                dest = directory / (rec['source_id'] + '-' + digest[:12] + dest.suffix)
            changed = digest != rec.get('sha256')
            if changed and rec.get('path'):
                rec.setdefault('previous_snapshots', []).append({k: rec[k] for k in
                    ['path', 'sha256', 'checked_at', 'text_path'] if k in rec})
            dest.write_bytes(content)
            rec.update(path=str(dest.relative_to(ROOT)), sha256=digest, checked_at=args.as_of,
                       status='downloaded', resolved_url=resolved_url)
            rec.pop('error', None); rec.pop('text_path', None); rec.pop('extraction', None)
            if is_pdf:
                # Optional extraction; the original PDF remains the authority.
                try:
                    import pymupdf
                    with pymupdf.open(dest) as doc:
                        text = '\n\f\n'.join(page.get_text() for page in doc)
                    out = dest.with_suffix('.txt'); out.write_text(text, encoding='utf-8')
                    rec.update(text_path=str(out.relative_to(ROOT)), extraction='PyMuPDF')
                except ImportError:
                    pass
                except Exception as exc:
                    rec['extraction_error'] = str(exc)
            if rec['source_id'] == 'resources':
                links = Links(); links.feed(content.decode('utf-8'))
                discovered = sorted(urllib.parse.urljoin(resolved_url, u) for u in links.urls)
            results.append({'source_id': rec['source_id'], 'status': 'downloaded', 'content_changed': changed})
        except Exception as exc:
            # Preserve last good source and its original verification date.
            rec['last_attempt'] = {'date': args.as_of, 'error': str(exc)}
            results.append({'source_id': rec['source_id'], 'status': 'failed', 'error': str(exc)})
            failed = True
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    report = {'attempted_at': args.as_of, 'sources': results, 'resource_pdf_links': discovered,
              'policy_updated': False,
              'next_step': 'Review current hub links and effective dates, then update policy/guides explicitly.'}
    output = ROOT / 'reports' / ('source-refresh-' + args.as_of + '.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr); sys.exit(1)
