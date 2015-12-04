# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class ResCompany(orm.Model):
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
