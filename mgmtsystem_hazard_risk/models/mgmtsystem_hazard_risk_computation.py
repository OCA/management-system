# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemHazardRiskComputation(models.Model):
    _name = "mgmtsystem.hazard.risk.computation"
    _description = "Computation Risk"

    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    name = fields.Char("Computation Risk", size=50, required=True)
    description = fields.Text("Description")
