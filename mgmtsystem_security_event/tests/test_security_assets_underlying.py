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
from psycopg2 import IntegrityError
from . import pool


class TestCreateUnderlyingAssets(TransactionCase):

    """Test management underlying assets object."""

    def setUp(self):
        super(TestCreateUnderlyingAssets, self).setUp()
        pool.init_pools(self)

        self.category_id = self.asset_category.create(
            self.cr, self.uid, {
                "name": "category",
            }
        )

        self.essential_ids = [
            self.asset_essential.create(
                self.cr, self.uid, {
                    "name": "essential%d" % i,
                }
            )

            for i in range(10)
        ]

    def test_create_underlying_asset(self):
        # (6, 0, ids) means replacing the list of possible ids
        # with those ids and creating relationships.
        id = self.asset_underlying.create(
            self.cr, self.uid, {
                "name": "underlying",
                "category": self.category_id,
                "essential_assets": [(6, 0, self.essential_ids)]
            }
        )

        self.assertNotEqual(id, 0)

        obj = self.asset_underlying.browse(self.cr, self.uid, id)

        self.assertEqual(obj.name, "underlying")
        self.assertEqual(obj.category.name, "category")

        for id in self.essential_ids:
            self.assertNotEqual(id, 0)

        self.assertEqual(len(obj.essential_assets), len(self.essential_ids))
