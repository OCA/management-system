# -*- encoding: utf-8 -*-
from osv import fields, osv

class mgmtsystem_nonconformity(osv.osv):
    _inherit = "mgmtsystem.nonconformity"
    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account', 'Contract'),
    }
mgmtsystem_nonconformity()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
