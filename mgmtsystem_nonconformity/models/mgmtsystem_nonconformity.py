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
from openerp.osv import orm
from openerp import models, api, fields

from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT,
)

import time


_STATES = [
    ('draft', _('Draft')),
    ('analysis', _('Analysis')),
    ('pending', _('Pending Approval')),
    ('open', _('In Progress')),
    ('done', _('Closed')),
    ('cancel', _('Cancelled')),
]
_STATES_DICT = dict(_STATES)

own_company = lambda self: self.env.user.company_id.id
default_date = lambda *a: time.strftime(DATE_FORMAT)
default_user_id = lambda self: self.env.user.id


class mgmtsystem_nonconformity(models.Model):
    """
    Management System - Nonconformity
    """
    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity of the management system"
    _rec_name = "description"
    _inherit = ['mail.thread']
    _order = "date desc"

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res

    # 1. Description
    id = fields.Integer('ID', readonly=True)
    ref = fields.Char(
        'Reference',
        size=64,
        required=True,
        readonly=True,
        default="NEW"
    )
    date = fields.Date('Date', required=True, default=default_date)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    reference = fields.Char('Related to', size=50)
    responsible_user_id = fields.Many2one(
       'res.users',
       'Responsible',
       required=True,
    )
    manager_user_id = fields.Many2one(
        'res.users',
        'Manager',
        required=True,
    )
    author_user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=default_user_id,
    )
    origin_ids = fields.Many2many(
        'mgmtsystem.nonconformity.origin',
        'mgmtsystem_nonconformity_origin_rel',
        'nonconformity_id',
        'origin_id',
        'Origin',
        required=True,
    )
    procedure_ids = fields.Many2many(
        'document.page',
        'mgmtsystem_nonconformity_procedure_rel',
        'nonconformity_id',
        'procedure_id',
        'Procedure',
    )
    description = fields.Text('Description', required=True)
    state = fields.Selection(_STATES, 'State', readonly=True, default="draft")
    state_name = fields.Char(
        compute='_state_name',
        string='State Description',
        size=40,
    )
    system_id = fields.Many2one('mgmtsystem.system', 'System')

    # 2. Root Cause Analysis
    cause_ids = fields.Many2many(
        'mgmtsystem.nonconformity.cause',
        'mgmtsystem_nonconformity_cause_rel',
        'nonconformity_id',
        'cause_id',
        'Cause',
    )
    severity_id = fields.Many2one(
        'mgmtsystem.nonconformity.severity',
        'Severity',
    )
    analysis = fields.Text('Analysis')
    immediate_action_id = fields.Many2one(
        'mgmtsystem.action',
        'Immediate action',
        domain="[('nonconformity_id', '=', id)]",
    )
    analysis_date = fields.Datetime('Analysis Date', readonly=True)
    analysis_user_id = fields.Many2one(
        'res.users',
        'Analysis by',
        readonly=True,
    )

    # 3. Action Plan
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_nonconformity_action_rel',
        'nonconformity_id',
        'action_id',
        'Actions',
    )
    actions_date = fields.Datetime('Action Plan Date', readonly=True)
    actions_user_id = fields.Many2one(
        'res.users',
        'Action Plan by',
        readonly=True,
    )
    action_comments = fields.Text(
        'Action Plan Comments',
        help="Comments on the action plan.",
    )

    # 4. Effectiveness Evaluation
    evaluation_date = fields.Datetime('Evaluation Date', readonly=True)
    evaluation_user_id = fields.Many2one(
        'res.users',
        'Evaluation by',
        readonly=True,
    )
    evaluation_comments = fields.Text(
        'Evaluation Comments',
        help="Conclusions from the last effectiveness evaluation.",
    )

    # Multi-company
    company_id = fields.Many2one('res.company', 'Company', default=own_company)

    @api.model
    def create(self, vals):
        vals.update({
            'ref': self.env['ir.sequence'].get('mgmtsystem.nonconformity')
        })
        return super(mgmtsystem_nonconformity, self).create(vals)

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
        return super(mgmtsystem_nonconformity, self).message_auto_subscribe(
            cr, uid, ids, updated_fields=updated_fields, context=context,
            values=values
        )

    def case_send_note(self, cr, uid, ids, text, data=None, context=None):
        for id in ids:
            pre = self.case_get_note_msg_prefix(cr, uid, id, context=context)
            msg = '%s <b>%s</b>' % (pre, text)
            if data:
                o = self.browse(cr, uid, ids, context=context)[0]
                post = _(u'''
<br />
<ul><li> <b>Stage:</b> %s → %s</li></ul>\
''') % (o.state, data['state'])
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
        # TODO static variables... hmm update state isn't going to work
        if (o.immediate_action_id
                and o.immediate_action_id.stage_id.name.lower() == 'draft'):
            o.immediate_action_id.case_open()
        for a in o.action_ids:
            if a.stage_id.name.lower() == 'draft':
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
        # TODO make it more friendly
        done_states = ['done', 'cancelled', 'settled', 'rejected']
        if (o.immediate_action_id
                and o.immediate_action_id.stage_id.name.lower()
                not in done_states):
            raise orm.except_orm(
                _('Error !'),
                _('Immediate action from analysis has not been closed.')
            )
        if ([i for i in o.action_ids
                if i.stage_id.name.lower() not in done_states]):
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

    def case_cancel_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>canceled</b>.') % (
                self.case_get_note_msg_prefix(cr, uid, id, context=context)
            )
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_reset_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>renewed</b>.') % (
                self.case_get_note_msg_prefix(cr, uid, id, context=context)
            )
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_open_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>opened</b>.') % (
                self.case_get_note_msg_prefix(cr, uid, id, context=context)
            )
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True

    def case_close_send_note(self, cr, uid, ids, context=None):
        for id in ids:
            msg = _('%s has been <b>closed</b>.') % (
                self.case_get_note_msg_prefix(cr, uid, id, context=context)
            )
            self.message_post(cr, uid, [id], body=msg, context=context)
        return True
