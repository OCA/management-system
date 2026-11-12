# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemIndicator(models.Model):
    _name = "mgmtsystem.indicator"
    _description = "Indicator"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    objective_id = fields.Many2one("mgmtsystem.objective", required=True)
    description = fields.Html()
    frequency = fields.Selection(
        [
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("semester", "Semester"),
            ("yearly", "Yearly"),
        ],
        default="yearly",
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    value_ids = fields.One2many("mgmtsystem.indicator.value", "indicator_id")
    has_min_target = fields.Boolean(string="Has Minimum Target")
    min_target_value = fields.Float()
    has_max_target = fields.Boolean(string="Has Maximum Target")
    max_target_value = fields.Float()
    value = fields.Float(compute="_compute_value", store=True, string="Values")
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure")
    value_state = fields.Selection(
        selection=lambda r: r.env["mgmtsystem.indicator.value"]
        ._fields["value_state"]
        .selection,
        compute="_compute_value",
        string="On Target?",
        store=True,
    )

    @api.depends("value_ids.value", "value_ids.state", "value_ids")
    def _compute_value(self):
        for record in self:
            posted_values = record.value_ids.filtered(
                lambda r: r.state == "posted"
            ).sorted(key=lambda r: r.date, reverse=True)[:1]
            record.value_state = (
                posted_values.value_state if posted_values else "no_target"
            )
            record.value = posted_values and posted_values.value or 0.0
