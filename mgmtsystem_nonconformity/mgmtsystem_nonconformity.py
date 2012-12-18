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

from tools.translate import _
import netsvc as netsvc
from openerp.osv import fields, orm

import time
from tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

class mgmtsystem_nonconformity_cause(orm.Model):
    """
    Cause of the nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.cause"
    _description = "Cause of the nonconformity of the management system"
    _order   = 'parent_id, sequence' 

    def name_get(self, cr, uid, ids, context=None):
        ids = ids or []
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res
        
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    def _check_recursion(self, cr, uid, ids, context=None, parent=None):
        return super(mgmtsystem_nonconformity_cause, self)._check_recursion(cr, uid, ids, context=context, parent=parent)

    _columns = {
        'id': fields.integer('ID', readonly=True),
        'name': fields.char('Cause', size=50, required=True, translate=True),
        'description': fields.text('Description'),
        'sequence': fields.integer('Sequence', help="Defines the order to present items"),
        'parent_id': fields.many2one('mgmtsystem.nonconformity.cause', 'Group'),
        'child_ids': fields.one2many('mgmtsystem.nonconformity.cause', 'parent_id', 'Child Causes'),
        'ref_code': fields.char('Reference Code', size=20),
    }
    _constraints = [
        (_check_recursion, 'Error! Cannot create recursive cycle.', ['parent_id'])
    ]


class mgmtsystem_nonconformity_origin(orm.Model):
    """
    Origin of nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.origin"
    _description = "Origin of nonconformity of the management system"
    _order   = 'parent_id, sequence' 

    def name_get(self, cr, uid, ids, context=None):
        ids = ids or []
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res
        
    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    def _check_recursion(self, cr, uid, ids, context=None, parent=None):
        return super(mgmtsystem_nonconformity_origin, self)._check_recursion(cr, uid, ids, context=context, parent=parent)

    _columns = {
        'id': fields.integer('ID', readonly=True),
        'name': fields.char('Origin', size=50, required=True, translate=True),
        'description': fields.text('Description'),
        'sequence': fields.integer('Sequence', help="Defines the order to present items"),
        'parent_id': fields.many2one('mgmtsystem.nonconformity.origin', 'Group'),
        'child_ids': fields.one2many('mgmtsystem.nonconformity.origin', 'parent_id', 'Childs'),
        'ref_code': fields.char('Reference Code', size=20),
    }


class mgmtsystem_nonconformity_severity(orm.Model):
    """Nonconformity Severity - Critical, Major, Minor, Invalid, ..."""
    _name = "mgmtsystem.nonconformity.severity"
    _description = "Severity of Complaints and Nonconformities"
    _columns = {
        'name': fields.char('Title', size=50, required=True, translate=True),
        'sequence': fields.integer('Sequence',),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active?'),
    }
    _defaults = {
        'active': True,
    }


_STATES = [
    ('draft', _('Draft')),
    ('analysis', _('Analysis')),
    ('pending', _('Pending Approval')),
    ('open', _('In Progress')),
    ('done', _('Closed')),
    ('cancel', _('Cancelled')),
    ]
_STATES_DICT =  dict(_STATES)

class mgmtsystem_nonconformity(orm.Model):
    """
    Management System - Nonconformity 
    """
    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity of the management system"
    _rec_name = "description"
    _inherit = ['mail.thread']
    _order = "date desc"

    def _state_name(self, cr, uid, ids, name, args, context=None):
        res = dict()
        for o in self.browse(cr, uid, ids, context=context):
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res

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
        'procedure_ids': fields.many2many('document.page','mgmtsystem_nonconformity_procedure_rel', 'nonconformity_id', 'procedure_id', 'Procedure'),
        'description': fields.text('Description', required=True),
        'state': fields.selection(_STATES, 'State', readonly=True),
        'state_name': fields.function(_state_name, string='State Description', type='char', size=40),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        'message_ids': fields.one2many('mail.message', 'res_id', 'Messages', domain=[('model','=',_name)]),
        #2. Root Cause Analysis
        'cause_ids': fields.many2many('mgmtsystem.nonconformity.cause','mgmtsystem_nonconformity_cause_rel', 'nonconformity_id', 'cause_id', 'Cause'),
        'severity_id': fields.many2one('mgmtsystem.nonconformity.severity', 'Severity'),
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
        'date': lambda *a: time.strftime(DATE_FORMAT),
        'state': 'draft',
        'author_user_id': lambda cr, uid, id, c={}: id,
        'ref': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'ref': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.nonconformity')
        })
        return super(mgmtsystem_nonconformity, self).create(cr, uid, vals, context)

    def wkf_analysis(self, cr, uid, ids, context=None):
        """Change state from draft to analysis"""
        self.message_append(cr, uid, self.browse(cr, uid, ids), _('Analysis'))
        return self.write(cr, uid, ids, {'state': 'analysis', 'analysis_date': None, 'analysis_user_id': None}, context=context)

    def action_sign_analysis(self, cr, uid, ids, context=None):
        """Sign-off the analysis"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'analysis':
            raise osv.except_osv(_('Error !'), _('This action can only be done in the Analysis state.'))
        if o.analysis_date:
            raise osv.except_osv(_('Error !'), _('Analysis is already approved.'))
        if not o.analysis:
            raise osv.except_osv(_('Error !'), _('Please provide an analysis before approving.'))
        vals = {'analysis_date': time.strftime(DATETIME_FORMAT), 'analysis_user_id': uid }
        self.write(cr, uid, ids, vals, context=context)
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Analysis Approved'))
        return True

    def wkf_review(self, cr, uid, ids, context=None):
        """Change state from analysis to pending approval"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if not o.analysis_date:
            raise osv.except_osv(_('Error !'), _('Analysis must be performed before submiting to approval.'))
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Pending Approval'))
        return self.write(cr, uid, ids, {'state': 'pending', 'actions_date': None, 'actions_user_id': None}, context=context)

    def action_sign_actions(self, cr, uid, ids, context=None):
        """Sign-off the action plan"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'pending':
            raise osv.except_osv(_('Error !'), _('This action can only be done in the Pending for Approval state.'))
        if o.actions_date:
            raise osv.except_osv(_('Error !'), _('Action plan is already approved.'))
        if not self.browse(cr, uid, ids, context=context)[0].analysis_date:
            raise osv.except_osv(_('Error !'), _('Analysis approved before the review confirmation.'))
        vals = {'actions_date': time.strftime(DATETIME_FORMAT), 'actions_user_id': uid }
        self.write(cr, uid, ids, vals, context=context)
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Action Plan Approved'))
        return True

    def wkf_open(self, cr, uid, ids, context=None):
        """Change state from pending approval to in progress, and Open  the related actions"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if not o.actions_date:
            raise osv.except_osv(_('Error !'), _('Action plan must be approved before opening.'))
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('In Progress'))
        #Open related Actions
        if o.immediate_action_id and o.immediate_action_id.state == 'draft':
            o.immediate_action_id.case_open(cr, uid, [o.immediate_action_id.id])
        for a in o.action_ids:
            if a.state == 'draft':
                a.case_open(cr, uid, [a.id])
        return self.write(cr, uid, ids, {'state': 'open', 'evaluation_date': None, 'evaluation_user_id': None}, context=context)

    def action_sign_evaluation(self, cr, uid, ids, context=None):
        """Sign-off the effectiveness evaluation"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'open':
            raise osv.except_osv(_('Error !'), _('This action can only be done in the In Progress state.'))
        vals = {'evaluation_date': time.strftime(DATETIME_FORMAT), 'evaluation_user_id': uid }
        self.write(cr, uid, ids, vals, context=context)
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Effectiveness Evaluation Approved'))
        return True

    def wkf_cancel(self, cr, uid, ids, context=None):
        """Change state to cancel"""
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Cancel'))
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def wkf_close(self, cr, uid, ids, context=None):
        """Change state from in progress to closed"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if not o.evaluation_date:
            raise osv.except_osv(_('Error !'), _('Effectiveness evaluation must be performed before closing.'))
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Close'))
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)

    def case_reset(self, cr, uid, ids, context=None, *args):
        """Reset to Draft and restart the workflows"""
        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            res = wf_service.trg_create(uid, self._name, id, cr)
        self.message_append(cr, uid, self.browse(cr, uid, ids, context=context), _('Draft'))
        vals = {
            'state': 'draft',
            'analysis_date': None, 'analysis_user_id': None, 
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
            }
        return self.write(cr, uid, ids, vals, context=context)


class mgmtsystem_action(orm.Model):
    _inherit = "mgmtsystem.action"
    _columns = {
        'nonconformity_immediate_id': fields.one2many('mgmtsystem.nonconformity', 'immediate_action_id', readonly=True),
        'nonconformity_ids': fields.many2many(
            'mgmtsystem.nonconformity', 'mgmtsystem_nonconformity_action_rel', 'action_id', 'nonconformity_id', 'Nonconformities', readonly=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
