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


class TestCreateEventScenario(TransactionCase):

    """Test management event scenario object."""

    def setUp(self):
        super(TestCreateEventScenario, self).setUp()
        pool.init_pools(self)

        # origin
        self.threat_origin_id = self.threat_origin.create(
            self.cr, self.uid, {
                "name": "origin",
            }
        )

        # scenario
        self.threat_scenario_id = self.threat_scenario.create(
            self.cr, self.uid, {
                "name": "scenario",
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

        # security_event_id
        self.event_id = self.event.create(
            self.cr, self.uid, {
                "name": "event"
            }
        )

    def test_create_event_scenario(self):
        # (6, 0, ids) means replacing the list of possible ids
        # with those ids and creating relationships.
        scenario_id = self.event_scenario.create(
            self.cr, self.uid, {
                "description": "description",
                "severity": self.severity_id,
                "security_event_id": self.event_id,
                "origin": self.threat_origin_id,
                "scenario": self.threat_scenario_id,
            }
        )

        self.assertNotEqual(scenario_id, 0)

        obj = self.event_scenario.browse(self.cr, self.uid, scenario_id)

        self.assertEqual(obj.name_get()[scenario_id], "Events - scenario - origin")
        self.assertEqual(obj.description, "description")
