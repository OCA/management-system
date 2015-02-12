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


class TestCreateThreatScenario(TransactionCase):

    """Test management threat scenario object."""

    def setUp(self):
        super(TestCreateThreatScenario, self).setUp()
        pool.init_pools(self)

        # origin
        self.threat_origin_id = self.threat_origin.create(
            self.cr, self.uid, {
                "name": "origin",
            }
        )

        # severity
        severity = self.registry("mgmtsystem.severity")
        self.severity_id = severity.create(
            self.cr, self.uid, {
                "name": "scenario",
                "category": "security",
                "value": 10,
            }
        )

        # probability
        probability = self.registry("mgmtsystem.probability")
        self.probability_id = probability.create(
            self.cr, self.uid, {
                "name": "probability",
                "category": "security",
                "value": 10,
            }
        )

        # underlying_assets
        self.underlying_ids = [
            self.asset_underlying.create(
                self.cr, self.uid, {
                    "name": "underlying%s" % i
                }
            )
            for i in range(10)
        ]

    def test_create_threat_scenario(self):
        # (6, 0, ids) means replacing the list of possible ids
        # with those ids and creating relationships.
        id = self.threat_scenario.create(
            self.cr, self.uid, {
                "name": "threat scenario",
                "description": "description",
                "origin": self.threat_origin_id,
                "underlying_assets": [(6, 0, self.underlying_ids)],
                # probability
                'original_probability': self.probability_id,
                'current_probability': self.probability_id,
                'residual_probability': self.probability_id,
                # severity
                'original_severity': self.severity_id,
                'residual_severity': self.severity_id,
                'current_severity': self.severity_id,
            }
        )

        self.assertNotEqual(id, 0)
        self.assertEqual(len(self.underlying_ids), 10)

        obj = self.threat_scenario.browse(self.cr, self.uid, id)

        self.assertEqual(obj.name, "threat scenario")
        self.assertEqual(obj.description, "description")
        self.assertEqual(len(obj.underlying_assets), len(self.underlying_ids))

        for i, asset in enumerate(obj.underlying_assets):
            self.assertEqual(asset.id, self.underlying_ids[i])
