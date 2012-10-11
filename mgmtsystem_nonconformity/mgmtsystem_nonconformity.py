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

from tools.translate import _
import netsvc as netsvc
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
        'name': fields.char('Cause', size=50, required=True, translate=True),
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
        'name': fields.char('Origin', size=50, required=True, translate=True),
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
    _inherit = ['mail.thread']
    _order = "date desc"

    _columns = {
        #1. Description
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
        'state': fields.selection((('d','Draft'),('p','Pending'),('o','Open'),('c','Closed'),('x','Cancelled')), 'State', size=16, readonly=True),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        'message_ids': fields.one2many('mail.message', 'res_id', 'Messages', domain=[('model','=',_name)]),
        #2. Root Cause Analysis
        'cause_ids': fields.many2many('mgmtsystem.nonconformity.cause','mgmtsystem_nonconformity_cause_rel', 'nonconformity_id', 'cause_id', 'Cause'),
        'analysis': fields.text('Analysis'),
        'immediate_action_id': fields.many2one('mgmtsystem.action', 'Immediate action',
            domain="[('nonconformity_id','=',id)]"),
        'analysis_date': fields.datetime('Analysis Date', readonly=True),
        'analysis_user_id': fields.many2one('res.users','Analysis by', readonly=True),
        #3. Action Plan
        'action_ids': fields.many2many('mgmtsystem.action', 'mgmtsystem_nonconformity_action_rel', 'nonconformity_id', 'action_id', 'Actions'),
        'actions_date': fields.datetime('Action Plan Date', readonly=True),
        'actions_user_id': fields.many2one('res.users','Action Plan by', readonly=True),
        'action_comments': fields.text('Action Plan Comments',
            help="Comments on the action plan."),
        #4. Effectiveness Evaluation
        'evaluation_date': fields.datetime('Evaluation Date', readonly=True),
        'evaluation_user_id': fields.many2one('res.users','Evaluation by', readonly=True),
        'evaluation_comments': fields.text('Evaluation Comments',
            help="Conclusions from the last effectiveness evaluation."),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'state': 'd',
        'author_user_id': lambda cr, uid, id, c={}: id,
        'ref': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'ref': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.nonconformity')
        })
        return super(mgmtsystem_nonconformity, self).create(cr, uid, vals, context)


    def action_sign_analysis(self, cr, uid, ids, context=None):
        if not self.browse(cr, uid, ids)[0].analysis:
            raise osv.except_osv(_('Error !'), _('Please provide an analysis before approving.'))
        vals = {'analysis_date': time.strftime('%Y-%m-%d %H:%M'), 
                'analysis_user_id': uid }
        self.write(cr, uid, ids, vals, context=context)
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Analysis Approved'))
        return True

    def action_sign_actions(self, cr, uid, ids, context=None):
        if not self.browse(cr, uid, ids)[0].analysis_date:
            raise osv.except_osv(_('Error !'), _('Analysis and causes identification must be performed before an action plan is approved.'))
        vals = {'actions_date': time.strftime('%Y-%m-%d %H:%M'), 
                'actions_user_id': uid }
        self.write(cr, uid, ids, vals, context=context)
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Action Plan Approved'))
        return True

    def action_sign_evaluation(self, cr, uid, ids, context=None):
        vals = {'evaluation_date': time.strftime('%Y-%m-%d %H:%M'), 
                'evaluation_user_id': uid }
        self.write(cr, uid, ids, vals, context=context)
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Effectiveness Evaluation Approved'))
        return True

    def wkf_cancel(self, cr, uid, ids, context=None):
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Cancel'))
        return self.write(cr, uid, ids, {'state': 'x'})

    def wkf_review(self, cr, uid, ids, context=None):
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Pending'))
        return self.write(cr, uid, ids, {'state': 'p'})

    def wkf_open(self, cr, uid, ids, context=None):
        if not self.browse(cr, uid, ids)[0].actions_date:
            raise osv.except_osv(_('Error !'), _('Action plan must be approved in order to be able to Open.'))
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Open'))
        return self.write(cr, uid, ids, {'state': 'o'})

    def wkf_close(self, cr, uid, ids, context=None):
        if not self.browse(cr, uid, ids)[0].evaluation_date:
            raise osv.except_osv(_('Error !'), _('Effectiveness evaluation must be performed in order be able to Close.'))
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Close'))
        return self.write(cr, uid, ids, {'state': 'c'})

    def _restart_workflow(self, cr, uid, ids, *args):
        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            wf_service.trg_create(uid, self._name, id, cr)
        return True

    def case_reset(self, cr, uid, ids, *args):
        """If model has a workflow, it's restarted."""
        res = self._restart_workflow(cr, uid, ids, *args)
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Draft'))
        return res

mgmtsystem_nonconformity()


class mgmtsystem_action(osv.osv):
    _inherit = "mgmtsystem.action"
    _columns = {
        'nonconformity_ids': fields.many2many('mgmtsystem.nonconformity', 'mgmtsystem_nonconformity_action_rel', 'action_id', 'nonconformity_id', 
                                              'Nonconformities', readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
