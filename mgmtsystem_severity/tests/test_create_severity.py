# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 - Present
#    Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
