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

from openerp.osv import fields, orm
from .common import _parse_risk_formula


class mgmtsystem_hazard_residual_risk(orm.Model):

    _name = "mgmtsystem.hazard.residual_risk"
    _description = "Residual Risks of hazard"

    def _compute_risk(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        mycompany = user.company_id

        for obj in self.browse(cr, uid, ids, context=context):
            if obj.probability_id and obj.severity_id and obj.usage_id:
                result[obj.id] = _parse_risk_formula(
                    mycompany.risk_computation_id.name,
                    obj.probability_id.value,
                    obj.severity_id.value,
                    obj.usage_id.value,
                )
            else:
                result[obj.id] = False

        return result

    _columns = {
        'name': fields.char('Name', size=50, required=True, translate=True),
        'probability_id': fields.many2one(
            'mgmtsystem.hazard.probability',
            'Probability',
            required=True,
        ),
        'severity_id': fields.many2one(
            'mgmtsystem.hazard.severity',
            'Severity',
            required=True,
        ),
        'usage_id': fields.many2one(
            'mgmtsystem.hazard.usage',
            'Occupation / Usage',
        ),
        'risk': fields.function(_compute_risk, string='Risk', type='integer'),
        'acceptability': fields.boolean('Acceptability'),
        'justification': fields.text('Justification'),
        'hazard_id': fields.many2one(
            'mgmtsystem.hazard',
            'Hazard',
            ondelete='cascade',
            select=True,
        ),
    }
