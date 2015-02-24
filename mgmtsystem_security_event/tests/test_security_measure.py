# -*- encoding: utf-8 -*-
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


class TestCreateSecurityMeasure(TransactionCase):

    """Test management security measure object."""

    def setUp(self):
        super(TestCreateSecurityMeasure, self).setUp()

        self.model = self.registry('mgmtsystem.security.measure')

        self.doc = self.registry('document.page')
        self.page = self.doc.create(
            self.cr, self.uid, {"name": "Testdoc", "content": "allo"}
        )

    def test_create_security_measure(self):
        id = self.model.create(self.cr, self.uid, {
            "name": "test",
            "description": "description",
        })

        self.assertNotEqual(id, 0)

        obj = self.model.browse(self.cr, self.uid, id)

        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.description, "description")
        self.assertEqual(obj.work_instructions.id, 0)

        obj.write({"work_instructions": self.page})

        obj = self.model.browse(self.cr, self.uid, id)
        self.assertEqual(obj.work_instructions.id, self.page)
        self.assertEqual(obj.work_instructions.name, "Testdoc")
