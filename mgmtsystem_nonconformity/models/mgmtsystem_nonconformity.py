# -*- coding: utf-8 -*-
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

from openerp import models, api, fields, netsvc, exceptions, _

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


class MgmtsystemNonconformity(models.Model):

    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity"
    _rec_name = "description"
    _inherit = ['mail.thread']
    _order = "date desc"
    _track = {
        'field': {
            'mgmtsystem_nonconformity.subtype_analysis': (
                lambda s, c, u, o, ctx=None: o["state"] == "analysis"
            ),
            'mgmtsystem_nonconformity.subtype_pending': (
                lambda s, c, u, o, ctx=None: o["state"] == "pending"
            ),
        },
    }

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res

    name = fields.Char('Name')

    # 1. Description
    ref = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default="NEW"
    )
    date = fields.Date(
        'Date',
        required=True,
        default=lambda *a: time.strftime(DATE_FORMAT)
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    reference = fields.Char('Related to')
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
        default=lambda self: self.env.user.id
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
    state = fields.Selection(
        _STATES,
        'State',
        readonly=True,
        default="draft",
        track_visibility='onchange',
    )
    state_name = fields.Char(
        compute='_state_name',
        string='State Description',
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
        domain="[('nonconformity_ids', '=', id)]",
    )
    analysis_date = fields.Datetime(
        'Analysis Date',
        readonly=True,
        track_visibility='onchange',
    )
    analysis_user_id = fields.Many2one(
        'res.users',
        'Analysis by',
        readonly=True,
        track_visibility='onchange',
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
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id)

    # Demo data missing fields...
    corrective_action_id = fields.Many2one(
        'mgmtsystem.action',
        'Corrective action',
        domain="[('nonconformity_id', '=', id)]",
    )
    preventive_action_id = fields.Many2one(
        'mgmtsystem.action',
        'Preventive action',
        domain="[('nonconformity_id', '=', id)]",
    )

    @property
    @api.multi
    def verbose_name(self):
        return self.env['ir.model'].search([('model', '=', self._name)]).name

    @api.model
    def create(self, vals):
        vals.update({
            'ref': self.env['ir.sequence'].get('mgmtsystem.nonconformity')
        })
        return super(MgmtsystemNonconformity, self).create(vals)

    @api.multi
    def message_auto_subscribe(self, updated_fields, values=None):
        """Add the responsible, manager and OpenChatter follow list."""
        self.ensure_one()
        user_ids = [
            self.responsible_user_id.id,
            self.manager_user_id.id,
            self.author_user_id.id,
        ]
        self.message_subscribe_users(user_ids=user_ids, subtype_ids=None)
        return super(MgmtsystemNonconformity, self).message_auto_subscribe(
            updated_fields=updated_fields,
            values=values
        )

    @api.multi
    def wkf_analysis(self):
        """Change state from draft to analysis"""
        return self.write({
            'state': 'analysis',
            'analysis_date': None,
            'analysis_user_id': None}
        )

    @api.multi
    def action_sign_analysis(self):
        """Sign-off the analysis"""
        self.ensure_one()
        if self.state != 'analysis':
            raise exceptions.ValidationError(
                _('This action can only be done in the Analysis state.')
            )
        if self.analysis_date:
            raise exceptions.ValidationError(
                _('Analysis is already approved.')
            )
        if not self.analysis:
            raise exceptions.ValidationError(
                _('Please provide an analysis before approving.')
            )
        self.write({
            'analysis_date': time.strftime(DATETIME_FORMAT),
            'analysis_user_id': self._uid,
        })
        self.message_post(
            body='%s <b>%s</b>' % (self.verbose_name, _('Analysis Approved'))
        )
        return True

    @api.multi
    def wkf_review(self):
        """Change state from analysis to pending approval"""
        for o in self:
            if not o.analysis_date:
                raise exceptions.ValidationError(
                    _('Analysis must be performed before submitting to '
                      'approval.')
                )
        return self.write({
            'state': 'pending',
            'actions_date': None,
            'actions_user_id': None}
        )

    @api.multi
    def action_sign_actions(self):
        """Sign-off the action plan"""
        self.ensure_one()
        if self.state != 'pending':
            raise exceptions.ValidationError(
                _('This action can only be done in the Pending for Approval '
                  'state.')
            )
        if self.actions_date:
            raise exceptions.ValidationError(
                _('Action plan is already approved.')
            )
        if not self.analysis_date:
            raise exceptions.ValidationError(
                _('Analysis approved before the review confirmation.')
            )
        self.write({
            'actions_date': time.strftime(DATETIME_FORMAT),
            'actions_user_id': self._uid,
        })
        self.message_post(
            body='%s <b>%s</b>' % (
                self.verbose_name, _('Action Plan Approved')
            )
        )
        return True

    @api.multi
    def wkf_open(self):
        """Change state from pending approval to in progress, and Open
        the related actions
        """
        self.ensure_one()
        if not self.actions_date:
            raise exceptions.ValidationError(
                _('Action plan must be approved before opening.')
            )
        if (self.immediate_action_id and
                self.immediate_action_id.stage_id.is_starting):
            self.immediate_action_id.case_open()
        for action in self.action_ids:
            if action.stage_id.is_starting:
                action.case_open()
        return self.write({
            'state': 'open',
            'evaluation_date': False,
            'evaluation_user_id': False,
        })

    @api.one
    def action_sign_evaluation(self):
        """Sign-off the effectiveness evaluation"""
        if self.state != 'open':
            raise exceptions.ValidationError(
                _('This action can only be done in the In Progress state.')
            )
        self.write({
            'evaluation_date': time.strftime(DATETIME_FORMAT),
            'evaluation_user_id': self._uid,
        })
        self.message_post(
            body='%s <b>%s</b>' % (
                self.verbose_name, _('Effectiveness Evaluation Approved')
            )
        )

    @api.multi
    def wkf_cancel(self):
        """Change state to cancel"""
        return self.write({'state': 'cancel'})

    @api.multi
    def wkf_close(self):
        """Change state from in progress to closed"""
        self.ensure_one()

        if (self.immediate_action_id and
                not self.immediate_action_id.stage_id.is_ending):
            raise exceptions.ValidationError(
                _('Immediate action from analysis has not been closed.')
            )
        if any(i for i in self.action_ids if not i.stage_id.is_ending):
            raise exceptions.ValidationError(
                _('Not all actions have been closed.')
            )
        if not self.evaluation_date:
            raise exceptions.ValidationError(
                _('Effectiveness evaluation must be performed before closing.')
            )
        return self.write({'state': 'done'})

    @api.multi
    def case_reset(self):
        """Reset to Draft and restart the workflow"""
        wf_service = netsvc.LocalService("workflow")
        for nc in self:
            wf_service.trg_create(self._uid, self._name, nc.id, self._cr)
        return self.write({
            'state': 'draft',
            'analysis_date': None, 'analysis_user_id': None,
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
        })
