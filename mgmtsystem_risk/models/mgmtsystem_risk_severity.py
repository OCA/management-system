# Copyright (C) 2025 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemRiskSeverity(models.Model):
    _name = "mgmtsystem.risk.severity"
    _description = "Risk Severity"

    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    name = fields.Char("Severity", required=True, translate=True)
    value = fields.Integer(required=True)
    description = fields.Text(required=False, translate=False)
