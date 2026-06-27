# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.mgmtsystem_hazard_risk.models.common import _parse_risk_formula


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
        cls.probability = cls.env["mgmtsystem.risk.probability"].create(
            {"name": "Maybe", "value": 2}
        )
        cls.severity = cls.env["mgmtsystem.risk.severity"].create(
            {"name": "Heavy", "value": 3}
        )
        cls.usage = cls.env["mgmtsystem.hazard.usage"].create(
            {"name": "Very high", "value": 5}
        )
        cls.computation = cls.env["mgmtsystem.hazard.risk.computation"].create(
            {"name": "A * B * C"}
        )
        cls.computation_ab = cls.env["mgmtsystem.hazard.risk.computation"].create(
            {"name": "A * B"}
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

    def test_hazard_risk_computation_a_times_b(self):
        self.env.company.risk_computation_id = self.computation_ab
        record = self._create_hazard(
            probability_id=self.probability.id,
            severity_id=self.severity.id,
            usage_id=self.usage.id,
        )
        self.assertEqual(record.risk, 6)

    def test_residual_risk_computation(self):
        self.env.company.risk_computation_id = self.computation
        hazard = self._create_hazard()
        residual = self.env["mgmtsystem.hazard.residual_risk"].create(
            {
                "name": "Residual 1",
                "hazard_id": hazard.id,
                "probability_id": self.probability.id,
                "severity_id": self.severity.id,
                "usage_id": self.usage.id,
            }
        )
        self.assertEqual(residual.risk, 30)

    def test_residual_risk_without_usage(self):
        self.env.company.risk_computation_id = self.computation
        hazard = self._create_hazard()
        residual = self.env["mgmtsystem.hazard.residual_risk"].create(
            {
                "name": "Residual 2",
                "hazard_id": hazard.id,
                "probability_id": self.probability.id,
                "severity_id": self.severity.id,
            }
        )
        self.assertFalse(residual.risk)

    def test_parse_risk_formula_missing(self):
        with self.assertRaises(UserError):
            _parse_risk_formula(self.env, False, 1, 2, 3)
