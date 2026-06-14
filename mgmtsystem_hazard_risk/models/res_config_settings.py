# Copyright (C) 2020 Guadaltech Soluciones Tecnológicas (<http://www.guadaltech.es>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    risk_computation_id = fields.Many2one(
        related="company_id.risk_computation_id", string="Risk formula", readonly=False
    )
