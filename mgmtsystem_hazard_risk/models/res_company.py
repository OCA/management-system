# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):

    _inherit = "res.company"

    def _get_formula(self):
        ids = self.env['mgmtsystem.hazard.risk.computation'].search(
            [('name', '=', 'A * B * C')],
            limit=1,
        )
        return ids

    risk_computation_id = fields.Many2one(
        'mgmtsystem.hazard.risk.computation',
        'Risk Computation',
        default=_get_formula
    )
