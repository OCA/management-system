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


class res_company(orm.Model):
    _inherit = "res.company"
    _columns = {
        'risk_computation_id': fields.many2one(
            'mgmtsystem.hazard.risk.computation',
            'Risk Computation',
            required=True,
        ),
    }

    def _get_formula(self, cr, uid, context=None):
        ids = self.pool.get('mgmtsystem.hazard.risk.computation').search(
            cr, uid, [('name', '=', 'A * B * C')], context=context
        )
        return ids and ids[0] or False

    _defaults = {
        'risk_computation_id': _get_formula
    }
