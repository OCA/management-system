# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemIndicatorValue(models.Model):
    _name = "mgmtsystem.indicator.value"
    _description = "Indicator Value"
    _order = "date desc"

    indicator_id = fields.Many2one("mgmtsystem.indicator", required=True)
    date = fields.Date(required=True)
    value = fields.Float(required=True)
    uom_id = fields.Many2one(related="indicator_id.uom_id")
    comment = fields.Text()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("posted", "Posted"),
        ],
        default="draft",
        readonly=True,
    )
    value_state = fields.Selection(
        [
            ("on_target", "On Target"),
            ("below_target", "Below Target"),
            ("above_target", "Above Target"),
            ("no_target", "No Target"),
        ],
        compute="_compute_value_state",
        string="On Target?",
        store=True,
    )

    @api.depends("value", "indicator_id")
    def _compute_value_state(self):
        for record in self:
            if (
                not record.indicator_id.has_max_target
                and not record.indicator_id.has_min_target
            ):
                record.value_state = "no_target"
            elif (
                record.indicator_id.has_min_target
                and record.value < record.indicator_id.min_target_value
            ):
                record.value_state = "below_target"
            elif (
                record.indicator_id.has_max_target
                and record.value > record.indicator_id.max_target_value
            ):
                record.value_state = "above_target"
            else:
                record.value_state = "on_target"

    def post(self):
        self.update({"state": "posted"})
