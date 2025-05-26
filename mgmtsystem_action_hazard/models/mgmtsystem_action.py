# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemAction(models.Model):

    _inherit = "mgmtsystem.action"

    mgmtsystem_hazard_ids = fields.Many2many(
        "mgmtsystem.hazard",
        string="Hazards",
    )
