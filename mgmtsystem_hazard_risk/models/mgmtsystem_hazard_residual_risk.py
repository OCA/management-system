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


class MgmtsystemHazardResidualRisk(models.Model):

    _name = "mgmtsystem.hazard.residual_risk"
    _description = "Residual Risks of hazard"

    name = fields.Char('Name', size=50, required=True, translate=True)
    probability_id = fields.Many2one(
        'mgmtsystem.hazard.probability',
        'Probability',
        required=True,
    )
    severity_id = fields.Many2one(
        'mgmtsystem.hazard.severity',
        'Severity',
        required=True,
    )
    usage_id = fields.Many2one('mgmtsystem.hazard.usage', 'Occupation / Usage')
    acceptability = fields.Boolean('Acceptability')
    justification = fields.Text('Justification')
    hazard_id = fields.Many2one(
        'mgmtsystem.hazard',
        'Hazard',
        ondelete='cascade',
        select=True,
    )

    @api.depends("probability_id", "severity_id", "usage_id")
    def _compute_risk(self):
        mycompany = self.env['res.users'].browse(self._uid).company_id
        if self.probability_id and self.severity_id and self.usage_id:
            self.risk = _parse_risk_formula(
                mycompany.risk_computation_id.name,
                self.probability_id.value,
                self.severity_id.value,
                self.usage_id.value
            )
        else:
            self.risk = False

    risk = fields.Integer('Risk', compute=_compute_risk)
