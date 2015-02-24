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


class TestCreateThreatOrigin(TransactionCase):

    """Test management threat origin object."""

    def setUp(self):
        super(TestCreateThreatOrigin, self).setUp()

        self.model = self.registry('mgmtsystem.security.threat.origin')

    def test_create_threat_origin(self):
        id = self.model.create(self.cr, self.uid, {
            "name": "test",
        })

        self.assertNotEqual(id, 0)

        obj = self.model.browse(self.cr, self.uid, id)

        self.assertEqual(obj.name, "test")
