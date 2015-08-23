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

from openerp.tools.translate import _
from openerp import netsvc
from openerp.osv import fields, orm
from openerp.addons.base_status.base_state import base_state
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT,
)

import time


class MgmtsystemNonconformity(base_state, orm.Model):
    """
    Management System - Nonconformity
    """
    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity of the management system"
    _inherit = ['mail.thread']
    _order = "date desc"

    _columns = {
        # 1. Description
        'id': fields.integer('ID', readonly=True),
        'ref': fields.char('Reference', size=64, required=True, readonly=True),
        'name': fields.char('Name', required=True),
        'date': fields.date('Date', required=True),
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'reference': fields.char('Related to', size=50),
        'responsible_user_id': fields.many2one(
            'res.users',
            'Responsible',
            required=True,
        ),
        'manager_user_id': fields.many2one(
            'res.users',
            'Manager',
            required=True,
        ),
        'author_user_id': fields.many2one(
            'res.users',
            'Filled in by',
            required=True,
        ),
        'origin_ids': fields.many2many(
            'mgmtsystem.nonconformity.origin',
            'mgmtsystem_nonconformity_origin_rel',
            'nonconformity_id',
            'origin_id', 'Origin', required=True,
        ),
        'procedure_ids': fields.many2many(
            'document.page', 'mgmtsystem_nonconformity_procedure_rel',
            'nonconformity_id', 'procedure_id', 'Procedure'
        ),
        'description': fields.text('Description', required=True),
        'state': fields.selection(
            lambda self, *a, **kw: self._get_states(*a, **kw),
            'State',
            readonly=True,
        ),
        'state_name': fields.function(
            lambda self, *a, **kw: self._state_name(*a, **kw),
            string='State Description',
            type='char',
            size=40,
        ),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        # 2. Root Cause Analysis
        'cause_ids': fields.many2many(
            'mgmtsystem.nonconformity.cause',
            'mgmtsystem_nonconformity_cause_rel',
            'nonconformity_id',
            'cause_id',
            'Cause',
        ),
        'severity_id': fields.many2one(
            'mgmtsystem.nonconformity.severity',
            'Severity',
        ),
        'analysis': fields.text('Analysis'),
        'immediate_action_id': fields.many2one(
            'mgmtsystem.action',
            'Immediate action',
            domain="[('nonconformity_id', '=', id)]",
        ),
        'analysis_date': fields.datetime('Analysis Date', readonly=True),
        'analysis_user_id': fields.many2one(
            'res.users',
            'Analysis by',
            readonly=True,
        ),
        # 3. Action Plan
        'action_ids': fields.many2many(
            'mgmtsystem.action',
            'mgmtsystem_nonconformity_action_rel',
            'nonconformity_id',
            'action_id',
            'Actions',
        ),
        'actions_date': fields.datetime('Action Plan Date', readonly=True),
        'actions_user_id': fields.many2one(
            'res.users',
            'Action Plan by',
            readonly=True,
        ),
        'action_comments': fields.text(
            'Action Plan Comments',
            help="Comments on the action plan.",
        ),
        # 4. Effectiveness Evaluation
        'evaluation_date': fields.datetime('Evaluation Date', readonly=True),
        'evaluation_user_id': fields.many2one(
            'res.users',
            'Evaluation by',
            readonly=True,
        ),
        'evaluation_comments': fields.text(
            'Evaluation Comments',
            help="Conclusions from the last effectiveness evaluation.",
        ),
        # Multi-company
        'company_id': fields.many2one('res.company', 'Company'),
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c:
            self.pool['res.users'].browse(cr, uid, uid, c).company_id.id),
        'date': lambda *a: time.strftime(DATE_FORMAT),
        'state': 'draft',
        'author_user_id': lambda cr, uid, id, c={}: id,
        'ref': 'NEW',
    }

    def _state_name(self, cr, uid, ids, name, args, context=None):
        res = dict()
        for o in self.browse(cr, uid, ids, context=context):
            state_selection = self._columns['state'].selection
            res[o.id] = dict(state_selection).get(o.state, o.state)
        return res

    def _get_states(self, cr, uid, context=None):
        return [
            ('draft', _('Draft')),
            ('analysis', _('Analysis')),
            ('pending', _('Pending Approval')),
            ('open', _('In Progress')),
            ('done', _('Closed')),
            ('cancel', _('Cancelled')),
        ]

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'ref': self.pool['ir.sequence'].get(
                cr, uid, 'mgmtsystem.nonconformity')
        })
        return super(MgmtsystemNonconformity, self).create(
            cr, uid, vals, context)

    def message_auto_subscribe(
            self, cr, uid, ids, updated_fields, context=None, values=None):
        """Add the reponsible, manager and OpenChatter follow list."""
        o = self.browse(cr, uid, ids, context=context)[0]
        user_ids = [
            o.responsible_user_id.id,
            o.manager_user_id.id,
            o.author_user_id.id,
        ]
        self.message_subscribe_users(
            cr, uid, ids, user_ids=user_ids, subtype_ids=None, context=context
        )
        return super(MgmtsystemNonconformity, self).message_auto_subscribe(
            cr, uid, ids, updated_fields=updated_fields, context=context,
            values=values
        )

    def case_send_note(self, cr, uid, ids, text, data=None, context=None):
        for id in ids:
            pre = self.case_get_note_msg_prefix(cr, uid, id, context=context)
            msg = '%s <b>%s</b>' % (pre, text)
            if data:
                o = self.browse(cr, uid, ids, context=context)[0]
                post = '''<br /><ul><li> <b>''' + _('Stage:') + u'''</b> \
%s → %s</li></ul>''' % (o.state, data['state'])
                msg += post
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_get_note_msg_prefix(self, cr, uid, id, context=None):
        return _('Nonconformity')

    def wkf_analysis(self, cr, uid, ids, context=None):
        """Change state from draft to analysis"""
        data = {
            'state': 'analysis',
            'analysis_date': None,
            'analysis_user_id': None}
        self.case_send_note(
            cr, uid, ids, _('Analysis'), data=data, context=context
        )
        return self.write(cr, uid, ids, data, context=context)

    def action_sign_analysis(self, cr, uid, ids, context=None):
        """Sign-off the analysis"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'analysis':
            raise orm.except_orm(
                _('Error !'),
                _('This action can only be done in the Analysis state.')
            )
        if o.analysis_date:
            raise orm.except_orm(
                _('Error !'),
                _('Analysis is already approved.')
            )
        if not o.analysis:
            raise orm.except_orm(
                _('Error !'),
                _('Please provide an analysis before approving.')
            )
        vals = {
            'analysis_date': time.strftime(DATETIME_FORMAT),
            'analysis_user_id': uid,
        }
        self.write(cr, uid, ids, vals, context=context)
        note = _('Analysis Approved')
        self.case_send_note(cr, uid, ids, note, context=context)
        return True

    def wkf_review(self, cr, uid, ids, context=None):
        """Change state from analysis to pending approval"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if not o.analysis_date:
            err = _('Analysis must be performed before submiting to approval.')
            raise orm.except_orm(_('Error !'), err)
        vals = {
            'state': 'pending',
            'actions_date': None,
            'actions_user_id': None}
        self.case_send_note(
            cr, uid, ids, _('Pending Approval'), data=vals, context=context
        )
        return self.write(cr, uid, ids, vals, context=context)

    def action_sign_actions(self, cr, uid, ids, context=None):
        """Sign-off the action plan"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'pending':
            raise orm.except_orm(
                _('Error !'),
                _('This action can only be done in the Pending for Approval '
                  'state.')
            )
        if o.actions_date:
            raise orm.except_orm(
                _('Error !'),
                _('Action plan is already approved.')
            )
        if not self.browse(cr, uid, ids, context=context)[0].analysis_date:
            raise orm.except_orm(
                _('Error !'),
                _('Analysis approved before the review confirmation.')
            )
        vals = {
            'actions_date': time.strftime(DATETIME_FORMAT),
            'actions_user_id': uid,
        }
        self.write(cr, uid, ids, vals, context=context)
        note = _('Action Plan Approved')
        self.case_send_note(cr, uid, ids, note, context=context)
        return True

    def wkf_open(self, cr, uid, ids, context=None):
        """Change state from pending approval to in progress, and Open
        the related actions
        """
        o = self.browse(cr, uid, ids, context=context)[0]
        if not o.actions_date:
            raise orm.except_orm(
                _('Error !'),
                _('Action plan must be approved before opening.')
            )
        self.case_open_send_note(cr, uid, ids, context=context)
        # Open related Actions
        if o.immediate_action_id and o.immediate_action_id.state == 'draft':
            o.immediate_action_id.case_open()
        for a in o.action_ids:
            if a.state == 'draft':
                a.case_open()
        return self.write(cr, uid, ids, {
            'state': 'open',
            'evaluation_date': None,
            'evaluation_user_id': None,
        }, context=context)

    def action_sign_evaluation(self, cr, uid, ids, context=None):
        """Sign-off the effectiveness evaluation"""
        o = self.browse(cr, uid, ids, context=context)[0]
        if o.state != 'open':
            raise orm.except_orm(
                _('Error !'),
                _('This action can only be done in the In Progress state.')
            )
        vals = {
            'evaluation_date': time.strftime(DATETIME_FORMAT),
            'evaluation_user_id': uid,
        }
        self.write(cr, uid, ids, vals, context=context)
        note = _('Effectiveness Evaluation Approved')
        self.case_send_note(cr, uid, ids, note, context=context)
        return True

    def wkf_cancel(self, cr, uid, ids, context=None):
        """Change state to cancel"""
        self.case_cancel_send_note(cr, uid, ids, context=context)
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def wkf_close(self, cr, uid, ids, context=None):
        """Change state from in progress to closed"""
        o = self.browse(cr, uid, ids, context=context)[0]
        done_states = ['done', 'cancelled']
        if (o.immediate_action_id and
                o.immediate_action_id.state not in done_states):
            raise orm.except_orm(
                _('Error !'),
                _('Immediate action from analysis has not been closed.')
            )
        if ([i for i in o.action_ids if i.state not in done_states]):
            raise orm.except_orm(
                _('Error !'),
                _('Not all actions have been closed.')
            )
        if not o.evaluation_date:
            raise orm.except_orm(
                _('Error !'),
                _('Effectiveness evaluation must be performed before closing.')
            )
        self.case_close_send_note(cr, uid, ids, context=context)
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)

    def case_reset(self, cr, uid, ids, context=None, *args):
        """Reset to Draft and restart the workflows"""
        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            wf_service.trg_create(uid, self._name, id, cr)
        self.case_reset_send_note(cr, uid, ids, context=context)
        vals = {
            'state': 'draft',
            'analysis_date': None, 'analysis_user_id': None,
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
        }
        return self.write(cr, uid, ids, vals, context=context)
