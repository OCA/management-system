# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestMgmtsystemHazard(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.department = cls.env["hr.department"].create({"name": "Test Department"})
        cls.hazard_type = cls.env["mgmtsystem.hazard.type"].create({"name": "Type"})
        cls.hazard_hazard = cls.env["mgmtsystem.hazard.hazard"].create(
            {"name": "Hazard"}
        )
        cls.hazard_origin = cls.env["mgmtsystem.hazard.origin"].create(
            {"name": "Origin"}
        )
        cls.risk_type = cls.env["mgmtsystem.hazard.risk.type"].create(
            {"name": "Physical"}
        )
        cls.probability = cls.env["mgmtsystem.hazard.probability"].create(
            {"name": "Maybe", "value": 2}
        )
        cls.severity = cls.env["mgmtsystem.hazard.severity"].create(
            {"name": "Heavy", "value": 3}
        )
        cls.usage = cls.env["mgmtsystem.hazard.usage"].create(
            {"name": "Very high", "value": 5}
        )
        cls.computation = cls.env["mgmtsystem.hazard.risk.computation"].create(
            {"name": "A * B * C"}
        )

    def _create_hazard(self, **extra):
        values = {
            "name": "Hazard Test",
            "type_id": self.hazard_type.id,
            "hazard_id": self.hazard_hazard.id,
            "origin_id": self.hazard_origin.id,
            "department_id": self.department.id,
            "responsible_user_id": self.env.user.id,
            "analysis_date": "2026-01-01",
            "risk_type_id": self.risk_type.id,
        }
        values.update(extra)
        return self.env["mgmtsystem.hazard"].create(values)

    def test_hazard_risk_without_formula_inputs(self):
        record = self._create_hazard()
        self.assertFalse(record.risk)

    def test_hazard_risk_computation_a_times_b_times_c(self):
        self.env.company.risk_computation_id = self.computation
        record = self._create_hazard(
            probability_id=self.probability.id,
            severity_id=self.severity.id,
            usage_id=self.usage.id,
        )
        self.assertEqual(record.risk, 30)
