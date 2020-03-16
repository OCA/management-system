# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemHazardUsage(models.Model):
    _name = "mgmtsystem.hazard.usage"
    _description = "Usage of hazard"

    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    name = fields.Char("Occupation / Usage", required=True, translate=True)
    value = fields.Integer("Value", required=True)
    description = fields.Text("Description")
