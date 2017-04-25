# -*- coding: utf-8 -*-
# Copyright 2015 Savoir-faire Linux <https://www.savoirfairelinux.com/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestCreateProbability(TransactionCase):

    """
    Test management probability object.

    Test the management probability object creation.
    It checks that each fields are required and that
    a valid value creates an entry.
    """

    def setUp(self):
        super(TestCreateProbability, self).setUp()

        self.probability_model = self.registry('mgmtsystem.probability')

    def test_create_probability(self):
        probability_id = self.probability_model.create(self.cr, self.uid, {
            "name": "test",
            "value": 0,
            "category": "hazard",
            "description": 'Test 1',
        })

        self.assertNotEqual(probability_id, 0)

        obj = self.probability_model.browse(self.cr, self.uid, probability_id)

        self.assertEqual(obj.value, 0)
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.category, "hazard")

        probability_id = self.probability_model.create(self.cr, self.uid, {
            "name": "test2",
            "value": 10,
            "category": "security",
            "description": 'Test 2',
        })

        self.assertNotEqual(probability_id, 0)

        obj = self.probability_model.browse(self.cr, self.uid, probability_id)

        self.assertEqual(obj.value, 10)
        self.assertEqual(obj.name, "test2")
        self.assertEqual(obj.category, "security")
