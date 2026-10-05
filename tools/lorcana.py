#!/usr/bin/env python3
"""Local, reproducible Lorcana retrieval and checks. Run through the locked uv environment."""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import date, datetime
from fractions import Fraction
from zoneinfo import ZoneInfo
import hashlib
import json
from math import comb
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile
import unicodedata
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
RAW = ROOT / 'data/raw/ravensburger/catalog.en.json'
DERIVED = ROOT / 'data/derived'
MECHANICAL = ('name', 'subtitle', 'card_type', 'ink_cost', 'inkable', 'ink_colors',
              'strength', 'willpower', 'lore', 'move_cost', 'classifications',
              'rules_text', 'copy_limit', 'extra_character_classification')
IDENTIFIER = re.compile(r'^(\d+)([a-z]?)/(\d+) EN (\d+)$')


def user_today():
    return datetime.now(ZoneInfo('America/Phoenix')).date().isoformat()


def norm(value):
    return unicodedata.normalize('NFKC', str(value)).translate(
        str.maketrans({'–': '-', '—': '-', '’': "'", '‘': "'"})).casefold().strip()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def read_jsonl(path):
    # Iterate physical newlines, not Unicode separators embedded in card/flavor text.
    with Path(path).open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def catalog_rows(data):
    if not isinstance(data, dict) or not isinstance(data.get('cards'), dict):
        raise ValueError('Expected a Ravensburger catalog with a cards object.')
    sets = {s['id']: s for s in data['card_sets']}
    rows = []
    seen = set()
    for category, cards in data['cards'].items():
        for c in cards:
            pid = c['culture_invariant_id']
            if pid in seen:
                raise ValueError(f'Duplicate printing ID: {pid}')
            seen.add(pid)
            if not c.get('deck_building_id'):
                raise ValueError(f'Missing deck-building identity: {pid}')
            if any(s not in sets for s in c['card_sets']):
                raise ValueError(f'Unknown assigned set: {pid}')
            if not isinstance(c['ink_cost'], int) or c['ink_cost'] < 0:
                raise ValueError(f'Invalid cost: {pid}')
            m = IDENTIFIER.fullmatch(c['card_identifier'])
            # The API uses 99 as a sentinel for Microbots; its printed rule is unlimited.
            limit = c.get('deck_building_limit', 4)
            if c['name'] == 'Microbots' and 'any number' in c['rules_text']:
                limit = None
            rows.append({
                'printing_id': pid, 'identity_id': c['deck_building_id'],
                'card_identifier': c['card_identifier'], 'name': c['name'],
                'subtitle': c.get('subtitle', ''),
                'full_name': c['name'] + (' - ' + c['subtitle'] if c.get('subtitle') else ''),
                'card_type': {'characters': 'character', 'actions': 'action',
                              'items': 'item', 'locations': 'location'}.get(category, category),
                'assigned_sets': c['card_sets'],
                'printed_set_number': int(m[4]) if m else None,
                'collector_number': int(m[1]) if m else None,
                'base_denominator': int(m[3]) if m else None,
                'is_base': bool(m and int(m[1]) <= int(m[3])),
                'ink_cost': c['ink_cost'], 'inkable': c['ink_convertible'],
                'ink_colors': sorted(c['magic_ink_colors']),
                'strength': c.get('strength'), 'willpower': c.get('willpower'),
                'lore': c.get('quest_value'), 'move_cost': c.get('move_cost'),
                'classifications': sorted(c['subtypes']),
                'rules_text': c['rules_text'], 'flavor_text': c['flavor_text'],
                'copy_limit': limit,
                'extra_character_classification': c.get('allows_adding_character_cards_to_deck_with_subtype'),
                'rarity': c['rarity'], 'special_rarity': c.get('special_rarity_id'),
                'artist': c['author'], 'search_tags': c.get('searchable_keywords', []),
                'additional_info': c['additional_info'], 'variants': c['variants'],
                'api_rotation_state': c['set_rotation_state'],
                'source_id': 'ravensburger-catalog-en',
            })
    if not rows:
        raise ValueError('Catalog contains no cards.')
    return sorted(rows, key=lambda r: r['printing_id'])


def build(root=ROOT):
    raw = root / 'data/raw/ravensburger/catalog.en.json'
    data = read_json(raw)
    rows = catalog_rows(data)
    grouped = defaultdict(list)
    for r in rows:
        grouped[r['identity_id']].append(r)
    identities, conflicts = [], []
    for identity_id, printings in sorted(grouped.items()):
        # A retrieval candidate only. Never declare the latest printing an oracle.
        representative = max(printings, key=lambda r: (
            r['is_base'], r['printed_set_number'] or 0, -r['printing_id']))
        differences = [k for k in MECHANICAL if len({json.dumps(r[k], sort_keys=True)
                                                   for r in printings}) > 1]
        i = {k: representative[k] for k in MECHANICAL}
        i.update(identity_id=identity_id, full_name=representative['full_name'],
                 aliases=sorted({r['full_name'] for r in printings}),
                 printing_ids=[r['printing_id'] for r in printings],
                 assigned_sets=sorted({s for r in printings for s in r['assigned_sets']}),
                 candidate_printing_id=representative['printing_id'],
                 text_status='requires_review' if differences else 'api_consistent_unreviewed',
                 conflict_fields=differences, source_id='ravensburger-catalog-en')
        identities.append(i)
        if differences:
            conflicts.append({'identity_id': identity_id, 'full_name': i['full_name'],
                              'fields': differences, 'printing_ids': i['printing_ids']})
    raw_identities = identities
    from loremaster.reviews import overlay
    identities, review_report = overlay(identities, root, user_today())
    coverage = []
    for s in data['card_sets']:
        match = re.fullmatch(r'set(\d+)', s['id'])
        if not match:
            continue
        number = int(match[1])
        rs = [r for r in rows if r['printed_set_number'] == number]
        base = [r for r in rs if r['is_base']]
        denominators = sorted({r['base_denominator'] for r in base})
        expected = denominators[0] if len(denominators) == 1 else None
        numbers = {r['collector_number'] for r in base}
        missing = sorted(set(range(1, expected + 1)) - numbers) if expected else None
        coverage.append({'set_id': s['id'], 'name': s['name'], 'printing_records': len(rs),
                         'base_records': len(base), 'base_numbers': len(numbers),
                         'expected_base_numbers': expected, 'missing_numbers': missing,
                         'base_number_coverage_complete': expected is not None and not missing,
                         'all_collectible_variants_complete': None})
    report = {'schema_version': 1, 'source_sha256': sha(raw),
              'catalog_hash': data.get('catalog_hash'), 'printing_records': len(rows),
              'gameplay_identities': len(identities), 'identities_with_conflicts': len(conflicts),
              'coconut_records': len(data.get('coconut_cards', [])), 'sets': coverage,
              'review_report': review_report,
              'review_ledger_sha256': sha(root / 'data/policy/card-text-reviews.json')
                if (root / 'data/policy/card-text-reviews.json').exists() else None,
              'note': 'Number coverage verifies mechanical base coverage, not every finish or variant.'}
    derived = root / 'data/derived'
    derived.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=derived.parent) as td:
        stage = Path(td)
        for filename, records in [('printings.jsonl', rows), ('identities.raw.jsonl', raw_identities),
                                  ('identities.jsonl', identities)]:
            (stage / filename).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n'
                                                for r in records), encoding='utf-8')
        with (stage / 'printings.csv').open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader()
            for r in rows:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict))
                            else v for k, v in r.items()})
        write_json(stage / 'coverage.json', report)
        write_json(stage / 'conflicts.json', conflicts)
        write_json(stage / 'coconut.json', data.get('coconut_cards', []))
        con = sqlite3.connect(stage / 'cards.sqlite')
        con.execute('CREATE TABLE identities (identity_id TEXT PRIMARY KEY, full_name TEXT, '
                    'search_text TEXT, data TEXT)')
        con.executemany('INSERT INTO identities VALUES (?,?,?,?)',
                        [(i['identity_id'], i['full_name'], norm(' '.join(i['aliases']) + ' ' + i['rules_text']),
                          json.dumps(i, ensure_ascii=False)) for i in identities])
        con.execute('CREATE TABLE printings (printing_id INTEGER PRIMARY KEY, identity_id TEXT, data TEXT)')
        con.executemany('INSERT INTO printings VALUES (?,?,?)',
                        [(r['printing_id'], r['identity_id'], json.dumps(r, ensure_ascii=False)) for r in rows])
        con.execute('CREATE INDEX printing_identity ON printings(identity_id)')
        con.execute('CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)')
        con.execute('INSERT INTO metadata VALUES (?,?)', ('source_sha256', report['source_sha256']))
        con.execute('INSERT INTO metadata VALUES (?,?)',
                    ('review_ledger_sha256', report['review_ledger_sha256']))
        con.commit(); con.close()
        for p in stage.iterdir():
            os.replace(p, derived / p.name)
    return report


def load_identities(as_of=None):
    if not (DERIVED / 'coverage.json').exists():
        raise ValueError('Run python3 tools/lorcana.py build first.')
    if read_json(DERIVED / 'coverage.json')['source_sha256'] != sha(RAW):
        raise ValueError('Generated data is stale; run build after importing a catalog.')
    from loremaster.reviews import overlay
    raw_path = DERIVED / 'identities.raw.jsonl'
    if not raw_path.exists():
        raise ValueError('Rebuild catalog to create raw identity candidates before applying reviews.')
    identities, _ = overlay(read_jsonl(raw_path), ROOT, as_of or user_today())
    return identities


def resolve(entry, identities):
    key = entry if isinstance(entry, str) else entry.get('deck_building_id', entry.get('identity_id'))
    if not key and isinstance(entry, dict):
        key = entry.get('full_name') or entry.get('name', '') + (
            ' - ' + entry['subtitle'] if entry.get('subtitle') else '')
    found = [i for i in identities if key == i['identity_id'] or
             norm(key) in {norm(a) for a in i['aliases']}]
    if len(found) != 1:
        raise ValueError(f'Card identity must resolve exactly once: {key!r}; matches={len(found)}')
    return found[0]


def load_deck(path, identities):
    path = Path(path)
    if path.suffix == '.json':
        d = read_json(path)
        entries = d['cards'] if isinstance(d, dict) else d
        if not isinstance(entries, list):
            raise ValueError('JSON must contain a cards list; site-specific card-ID maps need conversion.')
    else:
        entries = []
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            m = re.fullmatch(r'\s*(\d+)\s*(?:x\s+)?(.+?)\s*', line)
            if not m:
                raise ValueError(f'Expected "4 Exact Card - Version": {line!r}')
            entries.append({'quantity': int(m[1]), 'full_name': m[2]})
    counts = Counter()
    for entry in entries:
        q = entry.get('quantity')
        if isinstance(q, bool) or not isinstance(q, int) or q <= 0:
            raise ValueError('Every quantity must be a positive integer.')
        counts[resolve(entry, identities)['identity_id']] += q
    by_id = {i['identity_id']: i for i in identities}
    return [(by_id[k], v) for k, v in sorted(counts.items())]


def card_legality(card, fmt, as_of, policy):
    sets = [int(s[3:]) for s in card['assigned_sets'] if re.fullmatch(r'set\d+', s)]
    if not sets:
        return False, 'No expansion-set assignment; encounter/special cards require product-specific rules.'
    eligible = []
    for n in sets:
        release = policy['sets'].get(str(n))
        if not release:
            continue
        if release.get('legal_from') and as_of < release['legal_from']:
            continue
        if fmt == 'core' and n < policy['core_first_set']:
            continue
        eligible.append(n)
    if card['full_name'] in policy['bans'].get(fmt, []):
        return False, f'Banned in {fmt} under the policy snapshot.'
    return bool(eligible), f'Eligible assigned sets: {eligible}'


def analyze_deck(entries, fmt, as_of, policy, pool=None):
    date.fromisoformat(as_of)
    if fmt not in ['core', 'infinity', 'sealed', 'draft']:
        raise ValueError('Automated deck checks support core, infinity, sealed, draft only.')
    issues, review = [], []
    total = sum(q for _, q in entries)
    minimum = {'core': 60, 'infinity': 60, 'sealed': 40, 'draft': 35}[fmt]
    if total < minimum:
        issues.append(f'{total} cards; minimum {minimum}.')
    for i, _ in entries:
        if i['text_status'] == 'requires_review':
            review.append(i['full_name'] + ': printing differences in ' + ', '.join(i['conflict_fields']))
    if fmt in ['core', 'infinity']:
        if as_of < policy['valid_from']:
            review.append('Date predates supported policy; use archived contemporary official policy.')
        if as_of > policy['checked_at']:
            review.append('Future/unverified date: results are conditional on this frozen policy remaining in effect.')
        # Christopher Robin exempts other Hunny characters from the ink restriction.
        exemptions = {i['extra_character_classification'] for i, _ in entries
                      if i['extra_character_classification']}
        base_colors = {color for i, _ in entries for color in i['ink_colors']
                       if not (i['card_type'] == 'character' and
                               exemptions.intersection(i['classifications']) and
                               not i['extra_character_classification'])}
        if len(base_colors) > 2:
            issues.append(f'{len(base_colors)} non-exempt ink types; maximum 2.')
        by_name = Counter()
        limits = defaultdict(list)
        for i, q in entries:
            by_name[norm(i['full_name'])] += q
            limits[norm(i['full_name'])].append(i['copy_limit'])
            legal, reason = card_legality(i, fmt, as_of, policy)
            if not legal:
                issues.append(i['full_name'] + ': ' + reason)
        for name, q in by_name.items():
            finite = [n for n in limits[name] if n is not None]
            if finite and q > min(finite):
                issues.append(f'{name}: {q} copies exceeds limit {min(finite)}.')
    else:
        if pool is None:
            review.append('Personal registered/drafted pool is required to verify Limited ownership.')
        else:
            available = Counter({i['identity_id']: q for i, q in pool})
            for i, q in entries:
                if q > available[i['identity_id']]:
                    issues.append(f'{i["full_name"]}: {q} selected, {available[i["identity_id"]]} in pool.')
    return {'format': fmt, 'as_of': as_of, 'policy_checked_at': policy['checked_at'],
            'verdict': 'fails_checks' if issues else 'review_required' if review else 'passes_supported_checks',
            'issues': issues, 'review_required': review, 'card_count': total,
            'ink_colors': sorted({c for i, _ in entries for c in i['ink_colors']}),
            'inkable': sum(q for i, q in entries if i['inkable']),
            'uninkable': sum(q for i, q in entries if not i['inkable']),
            'printed_cost_curve': dict(sorted(Counter({cost: sum(q for i, q in entries if i['ink_cost'] == cost)
                                                      for cost in {i['ink_cost'] for i, _ in entries}}).items())),
            'card_types': dict(Counter({t: sum(q for i, q in entries if i['card_type'] == t)
                                       for t in sorted({i['card_type'] for i, _ in entries})})),
            'limits': 'Snapshot checks, not event certification; verify current sources, card text, and event terms.'}


def audit_collection(path, identities):
    mapped, unresolved = [], []
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        for number, row in enumerate(csv.DictReader(f), 2):
            try:
                quantity = int(row['Count'])
                if quantity < 0:
                    raise ValueError('Negative owned quantity.')
                card = resolve(row['Name'], identities)
                mapped.append({'row': number, 'identity_id': card['identity_id'],
                               'full_name': card['full_name'], 'quantity': quantity,
                               'set_number': row['Set Number'], 'card_number': row['Card Number'],
                               'variant': row['Variant']})
            except (ValueError, KeyError) as exc:
                unresolved.append({'row': number, 'name': row.get('Name'), 'error': str(exc)})
    totals = Counter()
    for r in mapped:
        totals[r['identity_id']] += r['quantity']
    return {'source_path': str(path), 'source_sha256': sha(path), 'mapped_rows': len(mapped),
            'unresolved_rows': unresolved, 'mapped_copies': sum(totals.values()),
            'identity_counts': dict(sorted(totals.items())),
            'limits': 'Exact-name gameplay reconciliation only; physical variants/printing matches require separate verification.'}


def probability(population, successes, draws, at_least=1):
    for name, value in [('population', population), ('successes', successes), ('draws', draws), ('at_least', at_least)]:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f'{name} must be a nonnegative integer.')
    if population == 0 or successes > population or draws > population:
        raise ValueError('Require population > 0, successes <= population, draws <= population.')
    numerator = sum(comb(successes, k) * comb(population - successes, draws - k)
                    for k in range(max(at_least, draws - (population - successes)), min(successes, draws) + 1))
    return Fraction(numerator, comb(population, draws))


def import_catalog(path, root=ROOT):
    source = Path(path)
    data = read_json(source)
    catalog_rows(data)  # Validate before modifying any file.
    target = root / 'data/raw/ravensburger/catalog.en.json'
    if source.resolve() == target.resolve():
        return build(root)
    digest = sha(source)
    if target.exists():
        backup = root / 'archive/catalogs' / (sha(target) + '.json')
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(target, backup)
    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as f:
        f.write(source.read_bytes()); tmp = Path(f.name)
    os.replace(tmp, target)
    manifest_path = root / 'sources/manifest.json'
    manifest = read_json(manifest_path)
    rec = next(r for r in manifest['sources'] if r['source_id'] == 'ravensburger-catalog-en')
    if rec.get('sha256') != digest:
        rec.setdefault('previous_exports', []).append({k: rec[k] for k in
            ['sha256', 'imported_at', 'retrieved_at'] if k in rec})
    rec.update(sha256=digest, status='imported', imported_at=user_today(), retrieved_at=None,
               note='Imported local export; original retrieval timestamp unknown.')
    write_json(manifest_path, manifest)
    return build(root)


def check_workspace():
    errors = []
    manifest = read_json(ROOT / 'sources/manifest.json')
    for rec in manifest['sources']:
        if rec.get('path'):
            p = ROOT / rec['path']
            if not p.is_file() or sha(p) != rec['sha256']:
                errors.append('Source missing or hash mismatch: ' + rec['source_id'])
    data = read_json(RAW)
    rows = catalog_rows(data)
    identities = load_identities()
    coverage = read_json(DERIVED / 'coverage.json')
    if coverage.get('review_ledger_sha256') != sha(ROOT / 'data/policy/card-text-reviews.json'):
        errors.append('Generated review ledger is stale; rebuild catalog.')
    if coverage.get('review_report', {}).get('stale'):
        errors.append('Card reviews have changed/missing source evidence.')
    printings = read_jsonl(DERIVED / 'printings.jsonl')
    if len(rows) != coverage['printing_records'] or len(identities) != coverage['gameplay_identities']:
        errors.append('Generated row count mismatch.')
    if len(printings) != len(rows) or {r['printing_id'] for r in printings} != {r['printing_id'] for r in rows}:
        errors.append('Generated printing identities/count mismatch.')
    for s in coverage['sets']:
        if not s['base_number_coverage_complete']:
            errors.append('Incomplete base-number coverage: ' + s['set_id'])
    con = sqlite3.connect(f'file:{DERIVED / "cards.sqlite"}?mode=ro', uri=True)
    if con.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
        errors.append('SQLite integrity failure.')
    if con.execute('SELECT count(*) FROM identities').fetchone()[0] != len(identities):
        errors.append('SQLite identity count mismatch.')
    if con.execute('SELECT count(*) FROM printings').fetchone()[0] != len(rows):
        errors.append('SQLite printing count mismatch.')
    if con.execute('SELECT value FROM metadata WHERE key=?', ('source_sha256',)).fetchone()[0] != sha(RAW):
        errors.append('SQLite source hash mismatch.')
    con.close()
    images_path = ROOT / 'sources/images/manifest.json'
    if images_path.exists():
        images = read_json(images_path)
        for rec in images['records']:
            if rec.get('status') == 'downloaded' and (not (ROOT / rec['path']).exists()
                    or sha(ROOT / rec['path']) != rec['sha256']):
                errors.append('Image missing or hash mismatch: ' + str(rec['printing_id']))
    return {'status': 'failed' if errors else 'passed', 'errors': errors,
            'printing_records': len(rows), 'identities': len(identities),
            'card_reviews': coverage.get('review_report', {})}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ['build', 'status', 'check']:
        sub.add_parser(name)
    s = sub.add_parser('search'); s.add_argument('query', nargs='?', default='')
    s.add_argument('--set', type=int); s.add_argument('--ink'); s.add_argument('--type')
    s.add_argument('--field', choices=['text', 'name', 'flavor', 'tag'], default='text')
    s.add_argument('--limit', type=int, default=10)
    s = sub.add_parser('show'); s.add_argument('card'); s.add_argument('--printings', action='store_true')
    s.add_argument('--as-of', default=user_today())
    s = sub.add_parser('collection'); s.add_argument('path')
    s = sub.add_parser('deck'); s.add_argument('path'); s.add_argument('--format', choices=['core', 'infinity', 'sealed', 'draft'], default='core')
    s.add_argument('--as-of', default=user_today()); s.add_argument('--pool')
    s = sub.add_parser('review', help='Sourced deck review with probabilities, collection and balanced candidates')
    s.add_argument('path'); s.add_argument('--as-of', default=user_today())
    s.add_argument('--format', choices=['core', 'infinity', 'sealed', 'draft'], default='core')
    s.add_argument('--pool'); s.add_argument('--profile'); s.add_argument('--output')
    s.add_argument('--collection', default='data/collections/andys-lore-library-2026-09-15.csv')
    s = sub.add_parser('probability')
    for name in ['population', 'successes', 'draws']:
        s.add_argument('--' + name, type=int, required=True)
    s.add_argument('--at-least', type=int, default=1)
    s = sub.add_parser('mulligan', help='Conditional target access for an actual observed opening hand')
    for name in ['population', 'successes', 'opening-successes', 'returned', 'kept-successes']:
        s.add_argument('--' + name, type=int, required=True)
    s.add_argument('--opening-size', type=int, default=7)
    s = sub.add_parser('import-catalog'); s.add_argument('path')
    args = p.parse_args()
    exit_code = 0
    if args.command == 'build':
        result = build()
    elif args.command == 'status':
        result = {'coverage': read_json(DERIVED / 'coverage.json'),
                  'policy': read_json(ROOT / 'data/policy/legality.json'),
                  'sources': read_json(ROOT / 'sources/manifest.json')}
    elif args.command == 'check':
        result = check_workspace(); exit_code = 1 if result['errors'] else 0
    elif args.command in ['search', 'show']:
        identities = load_identities(getattr(args, 'as_of', None))
        if args.command == 'show':
            result = resolve(args.card, identities)
            snapshot = read_json(ROOT / 'sources/manifest.json')
            catalog_source = next(s for s in snapshot['sources'] if s['source_id'] == 'ravensburger-catalog-en')
            result['evidence_context'] = {
                'as_of': args.as_of, 'catalog_sha256': sha(RAW),
                'catalog_imported_at': catalog_source.get('imported_at'),
                'catalog_retrieved_at': catalog_source.get('retrieved_at'),
                'note': 'Current supplied snapshot. Historical/future card text is not established by this export.'
                    if args.as_of != catalog_source.get('imported_at') else
                    'Reviewed values apply only where the dated ledger supplies evidence; otherwise API-consistent text.'}
            if args.printings:
                result['printings'] = [printing for printing in read_jsonl(DERIVED / 'printings.jsonl')
                                       if printing['identity_id'] == result['identity_id']]
        else:
            if args.field in ['flavor', 'tag']:
                matching_ids = set()
                for printing in read_jsonl(DERIVED / 'printings.jsonl'):
                    value = printing['flavor_text'] if args.field == 'flavor' else ' '.join(printing['search_tags'])
                    if norm(args.query) in norm(value):
                        matching_ids.add(printing['identity_id'])
            else:
                matching_ids = {i['identity_id'] for i in identities if norm(args.query) in
                                norm(' '.join(i['aliases']) + (' ' + i['rules_text'] if args.field == 'text' else ''))}
            found = [i for i in identities if i['identity_id'] in matching_ids
                     and (args.set is None or 'set' + str(args.set) in i['assigned_sets'])
                     and (args.ink is None or args.ink.upper() in i['ink_colors'])
                     and (args.type is None or args.type.lower() == i['card_type'])]
            result = {'total_matches': len(found), 'cards': [{k: i[k] for k in
                      ['identity_id', 'full_name', 'ink_cost', 'inkable', 'ink_colors',
                       'card_type', 'text_status']} for i in found[:max(args.limit, 0)]]}
    elif args.command == 'collection':
        result = audit_collection(args.path, load_identities())
        exit_code = 2 if result['unresolved_rows'] else 0
    elif args.command == 'deck':
        identities = load_identities(args.as_of)
        entries = load_deck(args.path, identities)
        pool = load_deck(args.pool, identities) if args.pool else None
        result = analyze_deck(entries, args.format, args.as_of,
                              read_json(ROOT / 'data/policy/legality.json'), pool)
        result['catalog_sha256'] = sha(RAW)
        exit_code = 2 if result['verdict'] != 'passes_supported_checks' else 0
    elif args.command == 'probability':
        value = probability(args.population, args.successes, args.draws, args.at_least)
        result = {'model': 'hypergeometric, uniform sampling without replacement, no mulligan/selection',
                  'population': args.population, 'successes': args.successes, 'draws': args.draws,
                  'at_least': args.at_least, 'exact_fraction': str(value), 'probability': float(value),
                  'percent': 100 * float(value)}
    elif args.command == 'review':
        from loremaster.deck_review import ReviewContext, write_review
        result = ReviewContext(ROOT, args.as_of, args.collection).review(
            Path(args.path), args.format, args.profile, args.pool)
        if args.output:
            write_review(result, Path(args.output), Path(args.path).stem)
        exit_code = 2 if result['validation']['verdict'] != 'passes_supported_checks' or result['review_required'] else 0
    elif args.command == 'mulligan':
        from loremaster.deck_review import conditional_mulligan, distribution
        value = conditional_mulligan(args.population, args.successes, args.opening_size,
                                    args.opening_successes, args.returned, args.kept_successes)
        result = {**distribution(value), 'model': 'Conditional on an actual observed opening hand and chosen returns; replacement draws exclude the whole original hand. No subsequent draws or unconditional keep policy modeled.',
                  'population': args.population, 'successes': args.successes,
                  'opening_size': args.opening_size, 'opening_successes': args.opening_successes,
                  'returned': args.returned, 'kept_successes': args.kept_successes}
    else:
        result = import_catalog(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
