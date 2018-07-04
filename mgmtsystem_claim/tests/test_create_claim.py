# -*- encoding: utf-8 -*-

from openerp.tests import common


class TestModelClaim(common.TransactionCase):
    def test_create_claim(self):
        record = self.env['mgmtsystem.claim'].create({
            "name": "SampleAction",
        })

        self.assertEqual(record.name, "SampleAction")
        self.assertNotEqual(record.reference, "NEW")
