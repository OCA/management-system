# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemObjective(models.Model):
    _name = "mgmtsystem.objective"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Objective"

    name = fields.Char(required=True)
    system_id = fields.Many2one("mgmtsystem.system")
    description = fields.Html()
    user_id = fields.Many2one("res.users", string="Owner")
    date_start = fields.Date()
    date_end = fields.Date()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("reached", "Reached"),
            ("not_reached", "Not Reached"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        required=True,
    )
    indicator_ids = fields.One2many("mgmtsystem.indicator", "objective_id")
