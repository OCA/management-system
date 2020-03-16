# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemHazardType(models.Model):
    _name = "mgmtsystem.hazard.type"
    _description = "Type of Hazard"

    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    name = fields.Char("Type", required=True, translate=True)
    description = fields.Text("Description")
