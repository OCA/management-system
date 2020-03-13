# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime

from odoo import tools
from odoo.tests import common

DATE_FORMAT = tools.DEFAULT_SERVER_DATE_FORMAT


class TestMgmtsystemHazard(common.TransactionCase):
    """
    Unit Test For mgmtsystem.hazard model
    """

    def test_hazard_risk(self):
        """
        Test Hazard Risk creation
        :return: (None)
        """
        type_rec = self.env.ref("mgmtsystem_hazard.type_ohsas_position")
        hazard_rec = self.env.ref("mgmtsystem_hazard.hazard_spilling")
        origin_rec = self.env.ref("mgmtsystem_hazard.origin_ignition_gas")
        department_rec = self.env["hr.department"].create({"name": "Department 01"})
        r_type_rec = self.env.ref("mgmtsystem_hazard_risk.risk_type_physical")

        record = self.env["mgmtsystem.hazard"].create(
            {
                "name": "Hazard Test 01",
                "type_id": type_rec.id,
                "hazard_id": hazard_rec.id,
                "origin_id": origin_rec.id,
                "department_id": department_rec.id,
                "responsible_user_id": self.env.user.id,
                "analysis_date": datetime.now().strftime(DATE_FORMAT),
                "risk_type_id": r_type_rec.id,
            }
        )
        self.assertEqual(record.name, "Hazard Test 01")
        self.assertEqual(record.risk, False)

    def test_hazard_risk_computation_a_time_b_time_c(self):
        """
        Test the hazard risk computation A * B * C
        :return: (None)
        """
        # A * B * C
        computation_risk = self.env.ref(
            "mgmtsystem_hazard_risk" ".risk_computation_a_times_b_times_c"
        )
        self.env.user.company_id.risk_computation_id = computation_risk

        type_rec = self.env.ref("mgmtsystem_hazard.type_ohsas_position")
        hazard_rec = self.env.ref("mgmtsystem_hazard.hazard_spilling")
        origin_rec = self.env.ref("mgmtsystem_hazard.origin_ignition_gas")
        department_rec = self.env["hr.department"].create({"name": "Department 01"})

        # Probability = 2
        probability_rec = self.env.ref("mgmtsystem_hazard.probability_maybe")

        # Severity = 3
        severity_rec = self.env.ref("mgmtsystem_hazard.severity_heavy")

        # Usage = 5
        usage_rec = self.env.ref("mgmtsystem_hazard.usage_very_high")
        r_type_rec = self.env.ref("mgmtsystem_hazard_risk.risk_type_physical")

        record = self.env["mgmtsystem.hazard"].create(
            {
                "name": "Hazard Test 02",
                "type_id": type_rec.id,
                "hazard_id": hazard_rec.id,
                "origin_id": origin_rec.id,
                "department_id": department_rec.id,
                "responsible_user_id": self.env.user.id,
                "analysis_date": datetime.now().strftime(DATE_FORMAT),
                "probability_id": probability_rec.id,
                "severity_id": severity_rec.id,
                "usage_id": usage_rec.id,
                "risk_type_id": r_type_rec.id,
            }
        )
        self.assertEqual(record.risk, 30)  # 2 * 3 * 5
