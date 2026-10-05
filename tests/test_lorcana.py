"""Behavioral regressions for identity, date, construction and probability checks."""
from collections import Counter
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('lorcana', Path(__file__).resolve().parents[1] / 'tools/lorcana.py')
L = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(L)


class ProbabilityTests(unittest.TestCase):
    def test_jsonl_keeps_unicode_separators_inside_card_text(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'printings.jsonl'
            row = {'rules_text': 'First\u2028Second', 'flavor_text': 'Third\u0085Fourth'}
            path.write_text(json.dumps(row, ensure_ascii=False) + '\n')
            self.assertEqual(L.read_jsonl(path), [row])

    def test_matches_exhaustive_small_population(self):
        # Independent enumeration, not a copy of the calculation formula.
        for n in range(1, 7):
            for k in range(n + 1):
                for draws in range(n + 1):
                    outcomes = list(itertools.combinations(range(n), draws))
                    for threshold in range(draws + 2):
                        wins = sum(sum(card < k for card in outcome) >= threshold for outcome in outcomes)
                        self.assertEqual(L.probability(n, k, draws, threshold), Fraction(wins, len(outcomes)))

    def test_invalid_inputs(self):
        for args in [(0, 0, 0), (60, 61, 7), (60, 4, 61), (60, -1, 7), (60, 4, -1)]:
            with self.assertRaises(ValueError): L.probability(*args)


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = L.load_identities()
        cls.policy = L.read_json(L.ROOT / 'data/policy/legality.json')

    def card(self, name):
        return L.resolve(name, self.cards)

    def analyze(self, entries, fmt='infinity', as_of='2026-10-04', pool=None):
        return L.analyze_deck(entries, fmt, as_of, self.policy, pool)

    def test_set14_complete_base_pool(self):
        rows = L.catalog_rows(L.read_json(L.RAW))
        base = [r for r in rows if r['printed_set_number'] == 14 and r['is_base']]
        self.assertEqual({r['collector_number'] for r in base}, set(range(1, 205)))
        self.assertEqual(len(base), 204)

    def test_prerelease_gate_is_not_api_rotation(self):
        card = self.card('Madam Mim - Resourceful Trickster')
        self.assertFalse(L.card_legality(card, 'core', '2026-10-15', self.policy)[0])
        self.assertTrue(L.card_legality(card, 'core', '2026-10-16', self.policy)[0])
        self.assertTrue(L.card_legality(card, 'infinity', '2026-10-16', self.policy)[0])

    def test_old_printing_legal_through_reprint_identity(self):
        rows = L.catalog_rows(L.read_json(L.RAW))
        old = next(r for r in rows if r['printed_set_number'] == 1 and
                   any(s in self.card(r['identity_id'])['assigned_sets'] for s in ['set9', 'set10', 'set11', 'set12', 'set13']))
        card = self.card(old['identity_id'])
        self.assertTrue(L.card_legality(card, 'core', '2026-10-04', self.policy)[0])

    def test_format_specific_ban_and_rotation(self):
        hiram = self.card('Hiram Flaversham - Toymaker')
        fortisphere = self.card('Fortisphere')
        self.assertFalse(L.card_legality(hiram, 'infinity', '2026-10-04', self.policy)[0])
        self.assertTrue(L.card_legality(fortisphere, 'infinity', '2026-10-04', self.policy)[0])
        self.assertEqual(self.policy['bans']['core'], [])
        self.assertFalse(L.card_legality(fortisphere, 'core', '2026-10-04', self.policy)[0])

    def test_printings_aggregate_for_copy_limit(self):
        i = self.card('The Glass Slipper')
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'deck.json'
            path.write_text(json.dumps({'cards': [{'identity_id': i['identity_id'], 'quantity': 2},
                                                {'full_name': i['full_name'], 'quantity': 1}]}))
            entries = L.load_deck(path, self.cards)
        self.assertEqual(entries[0][1], 3)
        self.assertTrue(any('exceeds limit 2' in x for x in self.analyze(entries)['issues']))

    def test_unlimited_microbots_and_99_puppies(self):
        microbots = self.card('Microbots'); puppy = self.card('Dalmatian Puppy - Tail Wagger')
        self.assertIsNone(microbots['copy_limit'])
        self.assertFalse(any('copies exceeds' in x for x in self.analyze([(microbots, 100)])['issues']))
        self.assertTrue(any('exceeds limit 99' in x for x in self.analyze([(puppy, 100)])['issues']))

    def test_hunny_exception_excludes_provider_itself(self):
        robin = self.card('Christopher Robin - Hunny Sage')
        # Real raw card data drives a cross-ink exemption test without relying on a known deck.
        hunny = next(i for i in self.cards if i['card_type'] == 'character' and 'Hunny' in i['classifications']
                     and not i['extra_character_classification'] and set(i['ink_colors']) - set(robin['ink_colors']))
        entries = [(robin, 4), (hunny, 4)]
        self.assertFalse(any('non-exempt ink' in x for x in self.analyze(entries)['issues']))
        ordinary = next(i for i in self.cards if i['card_type'] == 'character' and 'Hunny' not in i['classifications']
                        and set(i['ink_colors']) - set(robin['ink_colors']))
        self.assertTrue(any('non-exempt ink' in x for x in self.analyze(entries + [(ordinary, 1)])['issues']))

    def test_dual_ink_adds_both_colors(self):
        robin = self.card('Christopher Robin - Hunny Sage')
        third = next(i for i in self.cards if set(i['ink_colors']) - set(robin['ink_colors'])
                     and 'Hunny' not in i['classifications'])
        self.assertTrue(any('non-exempt ink' in x for x in self.analyze([(robin, 1), (third, 1)])['issues']))

    def test_limited_uses_pool_not_constructed_copy_ink_limits(self):
        card = self.card('Microbots')
        result = self.analyze([(card, 40)], 'sealed', pool=[(card, 39)])
        self.assertTrue(any('40 selected, 39 in pool' in x for x in result['issues']))
        result = self.analyze([(card, 40)], 'sealed', pool=[(card, 40)])
        self.assertFalse(result['issues'])
        self.assertTrue(self.analyze([(card, 40)], 'sealed')['review_required'])

    def test_encounter_card_excluded_from_constructed(self):
        card = next(i for i in self.cards if not any(s.startswith('set') for s in i['assigned_sets']))
        self.assertFalse(L.card_legality(card, 'infinity', '2026-10-04', self.policy)[0])

    def test_unknown_identity_and_nonpositive_quantities_rejected(self):
        with self.assertRaises(ValueError): self.card('Unknown - Invented Card')
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'deck.json'
            for quantity in [0, -4, True, 2.5]:
                path.write_text(json.dumps({'cards': [{'full_name': 'Microbots', 'quantity': quantity}]}))
                with self.assertRaises(ValueError): L.load_deck(path, self.cards)

    def test_future_and_historical_policy_require_review(self):
        card = self.card('Microbots')
        for as_of in ['2026-07-16', '2026-10-16']:
            self.assertTrue(self.analyze([(card, 60)], as_of=as_of)['review_required'])

    def test_text_conflicts_not_silently_resolved(self):
        # Pre-review dates expose raw differences rather than retroactive corrections.
        card = next(i for i in L.load_identities('2026-10-03') if i['text_status'] == 'requires_review')
        self.assertTrue(self.analyze([(card, 4)])['review_required'])

    def test_saved_deck_quantities_and_ink_metrics(self):
        for path in (L.ROOT / 'decks').glob('*.json'):
            entries = L.load_deck(path, self.cards)
            result = self.analyze(entries, 'core')
            self.assertEqual(result['card_count'], 60)
            self.assertEqual(result['inkable'] + result['uninkable'], 60)
            self.assertFalse(result['issues'])

    def test_rebuild_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); raw = root / 'data/raw/ravensburger/catalog.en.json'
            raw.parent.mkdir(parents=True); raw.write_bytes(L.RAW.read_bytes())
            L.build(root)
            first = {p.name: L.sha(p) for p in (root / 'data/derived').iterdir()}
            L.build(root)
            self.assertEqual(first, {p.name: L.sha(p) for p in (root / 'data/derived').iterdir()})

    def test_invalid_catalog_import_preserves_last_good_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); target = root / 'data/raw/ravensburger/catalog.en.json'
            target.parent.mkdir(parents=True); target.write_bytes(L.RAW.read_bytes())
            bad = root / 'bad.json'; bad.write_text('{"cards": []}')
            original = L.sha(target)
            with self.assertRaises(ValueError): L.import_catalog(bad, root)
            self.assertEqual(L.sha(target), original)


if __name__ == '__main__':
    unittest.main()
