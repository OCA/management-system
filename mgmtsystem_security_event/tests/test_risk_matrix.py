# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.mgmtsystem_security_event.tests.test_security_event import (
    TestSecurityEventBase,
)


class TestRiskMatrix(TestSecurityEventBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.matrix = cls.env["mgmtsystem.risk.matrix"].create(
            {"type": "current", "system_id": cls.system.id}
        )

    def test_get_event_list(self):
        self.assertEqual(self.event.current_probability_id, self.probabilities[3])
        self.assertEqual(self.event.current_severity_id, self.severities[3])
        self.assertEqual(self.event_2.current_probability_id, self.probabilities[2])
        self.assertEqual(self.event_2.current_severity_id, self.severities[2])

        res = self.matrix.get_event_list(self.severities[3], self.probabilities[3])
        self.assertEqual(len(res), 1)

        res = self.matrix.get_event_list(self.severities[2], self.probabilities[2])
        self.assertEqual(len(res), 1)

        res = self.matrix.get_event_list(self.severities[3], self.probabilities[2])
        self.assertEqual(len(res), 0)

    def _render_risk_matrix_pdf(self):
        return self.env["ir.actions.report"]._render_qweb_pdf(
            "mgmtsystem_security_event.action_report_risk_matrix",
            res_ids=self.matrix.ids,
        )

    def test_generate_risk_matrix_report(self):
        report = self._render_risk_matrix_pdf()
        self.assertTrue(report[0])

    def test_generate_risk_matrix_original(self):
        self.matrix.type = "original"
        report = self._render_risk_matrix_pdf()
        self.assertTrue(report[0])

    def test_generate_risk_matrix_residual(self):
        self.matrix.type = "residual"
        report = self._render_risk_matrix_pdf()
        self.assertTrue(report[0])
