# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemHazard(models.Model):

    _inherit = "mgmtsystem.hazard"

    mgmtsystem_action_ids = fields.Many2many(
        "mgmtsystem.action",
        string="Actions",
    )
