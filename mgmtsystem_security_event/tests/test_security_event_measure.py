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
from . import pool


class TestCreateEventMeasure(TransactionCase):

    """Test management event measure object."""

    def setUp(self):
        super(TestCreateEventMeasure, self).setUp()
        pool.init_pools(self)

        measure = self.registry("mgmtsystem.security.measure")

        self.measure_id = measure.create(
            self.cr, self.uid, {
                "name": "measure",
                "description": "hmm",
            }
        )

        self.underlying_asset_id = self.asset_underlying.create(
            self.cr, self.uid, {
                "name": "underlying"
            }
        )

        self.event_id = self.event.create(
            self.cr, self.uid, {
            }
        )

    def test_create_event_measure(self):
        id = self.event_measure.create(self.cr, self.uid, {
            "measures": self.measure_id,
            "underlying_assets": self.underlying_asset_id,
            "security_event_id": self.event_id,
            "prevention": False,
            "protection": True,
            "recovery": True,
        })

        self.assertNotEqual(id, 0)

        obj = self.event_measure.browse(self.cr, self.uid, id)

        self.assertEqual(obj.name, "Events - measure - underlying")
        self.assertEqual(obj.security_event_id.id, self.event_id)
        self.assertEqual(obj.underlying_assets.id, self.underlying_asset_id)
        self.assertEqual(obj.measures.id, self.measure_id)
