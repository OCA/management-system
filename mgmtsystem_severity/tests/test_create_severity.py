# -*- coding: utf-8 -*-
# Copyright 2015 Savoir-faire Linux <https://www.savoirfairelinux.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestCreateSeverity(TransactionCase):

    """
    Test management severity object.

    Test the management severity object creation.
    It checks that each fields are required and that
    a valid value creates an entry.
    """

    def setUp(self):
        super(TestCreateSeverity, self).setUp()

        self.severity_model = self.registry('mgmtsystem.severity')

    def test_create_severity(self):
        severity_id = self.severity_model.create(self.cr, self.uid, {
            "name": "test",
            "value": 0,
            "category": "hazard",
            "description": 'Test 1',
        })

        self.assertNotEqual(severity_id, 0)

        obj = self.severity_model.browse(self.cr, self.uid, severity_id)

        self.assertEqual(obj.value, 0)
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.category, "hazard")

        severity_id = self.severity_model.create(self.cr, self.uid, {
            "name": "test2",
            "value": 10,
            "category": "security",
            "description": 'Test 2',
        })

        self.assertNotEqual(severity_id, 0)

        obj = self.severity_model.browse(self.cr, self.uid, severity_id)

        self.assertEqual(obj.value, 10)
        self.assertEqual(obj.name, "test2")
        self.assertEqual(obj.category, "security")
