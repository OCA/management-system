# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemReview(models.Model):
    _inherit = "mgmtsystem.review"

    start_date = fields.Date()
    end_date = fields.Date()
    objective_ids = fields.Many2many(
        "mgmtsystem.objective", string="Reviewed objectives"
    )
    objective_domain = fields.Binary(compute="_compute_objective_domain")

    @api.depends("start_date", "end_date", "system_id")
    def _compute_objective_domain(self):
        for record in self:
            record.objective_domain = record._get_objective_domain()

    def _get_objective_domain(self):
        self.ensure_one()
        domain = [("state", "not in", ["draft", "cancelled"])]
        if self.start_date:
            domain += [
                "|",
                ("date_end", "=", False),
                ("date_end", ">=", self.start_date),
            ]
        if self.end_date:
            domain += [
                "|",
                ("date_start", "=", False),
                ("date_start", "<=", self.end_date),
            ]
        if self.system_id:
            domain += [
                "|",
                ("system_id", "=", False),
                ("system_id", "=", self.system_id.id),
            ]
        return domain

    def action_open_objectives(self):
        self.ensure_one()
        action = self.env.ref(
            "mgmtsystem_review_objective.mgmtsystem_indicator_value_action"
        ).read()[0]
        domain = [("objective_id", "in", self.objective_ids.ids)]
        if self.start_date:
            domain += [("date", ">=", self.start_date)]
        if self.end_date:
            domain += [("date", "<=", self.end_date)]
        action["domain"] = domain
        return action
