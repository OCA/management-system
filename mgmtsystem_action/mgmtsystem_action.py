# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from osv import fields, osv
from crm import crm

class mgmtsystem_action(osv.osv):
    _name = "mgmtsystem.action"
    _description = "Action"
    _inherit = "crm.claim"
    _columns = {
        'reference': fields.char('Reference', size=64, required=True, readonly=True),
	'type_action': fields.selection([('immediate','Immediate Action'),('correction','Corrective Action'),('prevention','Preventive Action'),('improvement','Improvement Opportunity')], 'Action Type'),
        'message_ids': fields.one2many('mailgate.message', 'res_id', 'Messages', domain=[('model','=',_name)]),
    }

    _defaults = {
        'reference': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'reference': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.action')
        })
        return super(mgmtsystem_action, self).create(cr, uid, vals, context)

mgmtsystem_action()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
