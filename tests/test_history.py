import json
from pathlib import Path
import shutil
import tempfile
import unittest

from server.history import DEFAULT_CORPUS, HistoryIndex, physical_lines


class HistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = HistoryIndex()

    @classmethod
    def tearDownClass(cls):
        cls.index.close()

    def test_every_record_is_an_exact_physical_line_slice(self):
        for record in self.index.records:
            lines = self.index.lines[record['source_id']]
            self.assertEqual(record['text'], '\n'.join(lines[record['start_line']-1:record['end_line']]))
        self.assertEqual(physical_lines('a\u2028b\nc'), ['a\u2028b', 'c'])

    def test_evidence_attribution(self):
        for evidence in json.loads((DEFAULT_CORPUS / 'evidence.json').read_text()):
            labels = self.index.labels[evidence['source_id']]
            for n in range(evidence['start_line']-1, evidence['end_line']):
                self.assertEqual(labels[n][0], evidence['speaker'], evidence['id'])

    def test_wrong_and_missing_delimiters(self):
        for source, line, role in [('game_finder',288,'user'), ('game_finder',291,'assistant'),
                                    ('game_finder',277,'assistant'), ('pokejam',585,'assistant')]:
            self.assertEqual(self.index.labels[source][line-1][0], role)

    def test_search_beyond_selected_evidence(self):
        result = self.index.search('pump faking', project='pokejam')
        self.assertTrue(any('pump faking' in r['text'] for r in result['results']))
        self.assertTrue(all(r['speaker'] == 'user' for r in result['results']))

    def test_compound_query_and_relevant_excerpt(self):
        result = self.index.search('specific examples', project='game_finder', limit=1)
        top = result['results'][0]
        self.assertEqual(set(top['matched_terms']), {'specific', 'examples'})
        self.assertIn("Don't just fix specific examples", top['text'])

    def test_old_and_new_decisions_are_retrievable(self):
        results = self.index.search('spec old', project='pokejam')['results']
        self.assertTrue(any('2k stats' in r['text'] for r in results))

    def test_inherited_author_is_never_default_personal_history(self):
        result = self.index.search('madden', speaker='all')
        self.assertFalse(any(r['prompt_author'] == 'inherited_author' for r in result['results']))
        result = self.index.search('madden', project='basketball_original', speaker='all')
        self.assertTrue(result['results'])
        self.assertEqual(result['results'][0]['prompt_author'], 'inherited_author')
        self.assertEqual(result['results'][0]['speaker'], 'unknown')

    def test_no_match_is_explicit(self):
        result = self.index.search('nonexistentwordxyzzy123')
        self.assertEqual(result['results'], [])
        self.assertEqual(len(result['coverage']['sources']), 7)
        self.assertIn('not that a decision never existed', result['interpretation'])

    def test_invalid_inputs(self):
        for kwargs in ({'query':''}, {'query':'   '}, {'query':'*()'}, {'query':'a'*301},
                       {'query':' '.join(str(i) for i in range(21))}, {'query':'test','project':'../'},
                       {'query':'test','speaker':'developer'}, {'query':'test','limit':0},
                       {'query':'test','limit':6}, {'query':'test','limit':True}):
            with self.assertRaises(ValueError):
                self.index.search(**kwargs)

    def test_literal_query_does_not_inject_fts(self):
        result = self.index.search('" OR * - ; DROP TABLE records; --')
        self.assertIsInstance(result['results'], list)
        self.assertTrue(self.index.search('pump', project='pokejam')['results'])

    def test_bounds_and_exact_excerpt_offsets(self):
        result = self.index.search('game model', speaker='all', limit=2)
        self.assertLessEqual(len(result['results']), 2)
        self.assertTrue(result['results_truncated'])
        records = {r['record_id']:r for r in self.index.records}
        for r in result['results']:
            raw = records[r['record_id']]['text']
            self.assertEqual(r['text'], raw[r['start_character_in_record']:r['end_character_in_record']])
            self.assertLessEqual(len(r['text']), 1400)

    def test_context_has_valid_line_locations_at_file_boundary(self):
        record = next(r for r in self.index.records if r['source_id']=='nba_vs_wnba' and r['start_line']==1)
        context = self.index.context(record)
        self.assertIsNone(context['before']['start_line'])
        self.assertIsNone(context['before']['end_line'])
        self.assertEqual(context['before']['text'], '')
        for r in self.index.records:
            for excerpt in self.index.context(r).values():
                if excerpt['start_line'] is not None:
                    self.assertEqual(excerpt['end_line'], excerpt['start_line'] + excerpt['text'].count('\n'))

    def test_token_fallback(self):
        index = HistoryIndex(use_fts=False)
        try:
            self.assertEqual(index.engine, 'token scan')
            result = index.search('pump faking', project='pokejam')
            self.assertTrue(any('pump faking' in r['text'] for r in result['results']))
            self.assertEqual(index.search('nonexistentwordxyzzy123')['results'], [])
        finally:
            index.close()

    def test_tampered_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            corpus = Path(folder)/'corpus'
            shutil.copytree(DEFAULT_CORPUS, corpus)
            with (corpus/'logs/hw7_bird_keeper.md').open('a') as stream:
                stream.write('changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                HistoryIndex(corpus)


if __name__ == '__main__':
    unittest.main()
