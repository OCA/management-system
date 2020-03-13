# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    risk_computation_id = fields.Many2one(
        related="company_id.risk_computation_id", string="Risk formula", readonly=False
    )
