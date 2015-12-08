# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from .common import _parse_risk_formula


class MgmtsystemHazard(models.Model):

    _inherit = "mgmtsystem.hazard"
    risk_type_id = fields.Many2one(
        'mgmtsystem.hazard.risk.type',
        'Risk Type',
        required=True,
    )
    risk = fields.Integer(compute="_compute_risk", string='Risk')
    residual_risk_ids = fields.One2many(
        'mgmtsystem.hazard.residual_risk',
        'hazard_id',
        'Residual Risk Evaluations',
    )

    @api.depends("probability_id", "severity_id", "usage_id")
    def _compute_risk(self):
        mycompany = self.env['res.users'].browse(self._uid).company_id
        for hazard in self:
            if hazard.probability_id and \
                    hazard.severity_id and\
                    hazard.usage_id:
                hazard.risk = _parse_risk_formula(
                    mycompany.risk_computation_id.name,
                    hazard.probability_id.value,
                    hazard.severity_id.value,
                    hazard.usage_id.value
                )
            else:
                hazard.risk = False
