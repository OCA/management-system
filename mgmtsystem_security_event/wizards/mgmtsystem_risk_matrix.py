# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemRiskMatrix(models.TransientModel):
    _name = "mgmtsystem.risk.matrix"
    _description = "Management System Risk Matrix"

    @api.model
    def _default_system_id(self):
        return self.env["mgmtsystem.system"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )

    type = fields.Selection(
        selection=[
            ("original", "Before applying any control"),
            ("current", "With current controls"),
            ("residual", "After applying the planned controls"),
        ],
        required=True,
        default="current",
    )
    system_id = fields.Many2one(
        "mgmtsystem.system",
        required=True,
        default=lambda self: self._default_system_id(),
    )
    company_id = fields.Many2one(
        related="system_id.company_id",
        readonly=True,
        store=True,
    )

    def get_event_list(self, severity_id, probability_id):
        self.ensure_one()
        events = self.get_events()
        if self.type == "original":
            return events.filtered(
                lambda e: e.original_probability_id == probability_id
                and e.original_severity_id == severity_id
            )
        if self.type == "current":
            return events.filtered(
                lambda e: e.current_probability_id == probability_id
                and e.current_severity_id == severity_id
            )
        return events.filtered(
            lambda e: e.residual_probability_id == probability_id
            and e.residual_severity_id == severity_id
        )

    def probability_name(self, probability):
        return f"{probability.value}.{probability.name}"

    def severity_name(self, severity):
        return f"{severity.value}.{severity.name}"

    def get_events(self):
        self.ensure_one()
        return self.env["mgmtsystem.security.event"].search(
            [("system_id", "=", self.system_id.id)]
        )

    def get_probabilities(self):
        return self.env["mgmtsystem.hazard.probability"].search(
            [("company_id", "in", (False, self.env.company.id))],
            order="value",
        )

    def get_severities(self):
        return self.env["mgmtsystem.hazard.severity"].search(
            [("company_id", "in", (False, self.env.company.id))],
            order="value desc",
        )

    def get_cell_color(self, severity, probability):
        level = self.env["mgmtsystem.risk.matrix.level"].search(
            [
                ("severity_min", "<=", severity.value),
                ("severity_max", ">=", severity.value),
                ("probability_min", "<=", probability.value),
                ("probability_max", ">=", probability.value),
            ],
            limit=1,
        )
        if not level:
            return "#B6D7A8"
        return {
            "green": "#B6D7A8",
            "orange": "#F9CB9C",
            "red": "#EA9999",
        }.get(level.color, "#B6D7A8")

    def print_report(self):
        return self.env.ref(
            "mgmtsystem_security_event.action_report_risk_matrix"
        ).report_action(self)
