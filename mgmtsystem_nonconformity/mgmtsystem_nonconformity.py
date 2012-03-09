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
import time

class mgmtsystem_nonconformity_cause(osv.osv):
    """
    Cause of the nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.cause"
    _description = "Cause of the nonconformity of the management system"
    _columns = {
        'id': fields.integer('ID', readonly=True),
        'name': fields.char('Cause', size=50, required=True),
        'description': fields.text('Description')
    }

mgmtsystem_nonconformity_cause()

class mgmtsystem_nonconformity_origin(osv.osv):
    """
    Origin of nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.origin"
    _description = "Origin of nonconformity of the management system"
    _columns = {
        'id': fields.integer('ID', readonly=True),
        'name': fields.char('Origin', size=50, required=True),
        'description': fields.text('Description')
    }

mgmtsystem_nonconformity_origin()

class mgmtsystem_nonconformity(osv.osv):
    """
    Management System - Nonconformity 
    """
    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity of the management system"
    _rec_name = "description"
    _order = "date desc"

    _columns = {
        'id': fields.integer('ID', readonly=True),
        'ref': fields.char('Reference', size=64, required=True, readonly=True),
        'date': fields.date('Date', required=True),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'reference': fields.char('Related to', size=50),
        'responsible_user_id': fields.many2one('res.users','Responsible', required=True),
        'manager_user_id': fields.many2one('res.users','Manager', required=True),
        'author_user_id': fields.many2one('res.users','Filled in by', required=True),
        'origin_ids': fields.many2many('mgmtsystem.nonconformity.origin','mgmtsystem_nonconformity_origin_rel', 'nonconformity_id', 'origin_id', 'Origin', required=True),
        'procedure_ids': fields.many2many('wiki.wiki','mgmtsystem_nonconformity_procedure_rel', 'nonconformity_id', 'procedure_id', 'Procedure'),
        'description': fields.text('Description', required=True),
        'cause_ids': fields.many2many('mgmtsystem.nonconformity.cause','mgmtsystem_nonconformity_cause_rel', 'nonconformity_id', 'cause_id', 'Cause'),
        'analysis': fields.text('Analysis'),
        'immediate_action_id': fields.many2one('mgmtsystem.action', 'Immediate action'),
        'efficiency_immediate': fields.text('Efficiency of the immediate action'),
        'corrective_action_id': fields.many2one('mgmtsystem.action', 'Corrective action'),
        'efficiency_corrective': fields.text('Efficiency of the corrective action'),
        'preventive_action_id': fields.many2one('mgmtsystem.action', 'Preventive action'),
        'efficiency_preventive': fields.text('Efficiency of the preventive action'),
        'state': fields.selection((('o','Open'),('c','Closed')), 'State', size=16, readonly=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'state': 'o',
        'author_user_id': lambda cr, uid, id, c={}: id,
        'ref': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'ref': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.nonconformity')
        })
        return super(mgmtsystem_nonconformity, self).create(cr, uid, vals, context)


    def button_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'c'})

mgmtsystem_nonconformity()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
