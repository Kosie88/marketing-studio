"""Observable readiness and resume invariants; no external services."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/marketing-studio-codex/scripts/validate_campaign.py'
spec = importlib.util.spec_from_file_location('validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CampaignValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / 'photo.jpg').write_bytes(b'fixture')
        self.data = {
            'campaign_id': 'food-offer', 'channels': ['facebook'],
            'brief': {'audience': 'Family gathering', 'objective': 'Sell approved set',
                      'offer': '$798 delivery included', 'variants': ['garlic'],
                      'cta': {'text': 'Order', 'url': 'https://example.com/order'},
                      'proofPoints': [{'id': 'offer', 'claim': '$798 delivery included',
                                       'source': 'Client approval', 'status': 'verified'}]},
            'copy': {'facebook': {'text': 'Offer and CTA', 'claim_ids': ['offer']}},
            'product_quantities': {'steak': 2},
            'assets': [{'id': 'photo', 'path': 'photo.jpg', 'status': 'approved',
                        'kind': 'reference', 'product_ids': ['steak'], 'variant_ids': ['garlic'],
                        'depicted_quantities': {'steak': 2}, 'review': 'Identity checked'}],
            'gates': {'facts': 'approved', 'copy': 'approved', 'visuals': 'approved', 'authorization': 'pending'}
        }

    def check(self, **kwargs):
        return validator.validate(self.data, self.base, **kwargs)

    def test_ready_does_not_imply_publish(self):
        self.assertEqual(self.check(ready=True), ([], []))
        self.assertTrue(self.check(publish=True)[0])
        self.data['gates']['authorization'] = {'source': 'User instruction', 'channels': ['facebook'], 'timing': '2026-10-02 12:00 Asia/Hong_Kong'}
        self.assertEqual(self.check(publish=True), ([], []))

    def test_pending_proof_draft_vs_ready(self):
        self.data['brief']['proofPoints'][0]['status'] = 'pending'
        self.assertFalse(self.check()[0])
        self.assertTrue(self.check()[1])
        self.assertTrue(self.check(ready=True)[0])

    def test_rejected_and_unsourced_claim_fail(self):
        point = self.data['brief']['proofPoints'][0]
        point['status'] = 'rejected'
        self.assertTrue(self.check()[0])
        point['status'], point['source'] = 'verified', ''
        self.assertTrue(self.check()[0])

    def test_missing_finished_file_invalidates_saved_status(self):
        (self.base / 'photo.jpg').unlink()
        self.assertTrue(self.check()[0])
        self.data['assets'][0]['status'] = 'planned'
        self.assertFalse(self.check()[0])
        self.assertTrue(self.check(ready=True)[0])

    def test_unknown_claim_and_variant_fail(self):
        self.data['copy']['facebook']['claim_ids'] = ['fiction']
        self.data['assets'][0]['variant_ids'] = ['raw']
        self.assertEqual(len(self.check(ready=True)[0]), 2)

    def test_quantity_mismatch_fails(self):
        self.data['assets'][0]['depicted_quantities']['steak'] = 4
        self.assertTrue(self.check()[0])

    def test_malformed_types_report_errors(self):
        for field, value in [('channels', [['bad']]), ('assets', 7), ('brief', [])]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data[field] = value
                self.assertTrue(validator.validate(data, self.base)[0])

    def test_publish_scope_cannot_expand(self):
        self.data['gates']['authorization'] = {'source': 'User', 'channels': ['instagram'], 'timing': 'today'}
        self.assertTrue(self.check(publish=True)[0])


if __name__ == '__main__':
    unittest.main()
