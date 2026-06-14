# Copyright (C) 2020 Guadaltech Soluciones Tecnológicas (<http://www.guadaltech.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    risk_computation_id = fields.Many2one(
        "mgmtsystem.hazard.risk.computation", string="Risk Computation"
    )
