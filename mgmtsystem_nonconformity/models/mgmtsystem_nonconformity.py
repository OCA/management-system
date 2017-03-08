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

from odoo import models, api, fields, netsvc, exceptions, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime, timedelta
from odoo.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT,
)
import time
import pytz
import re
import logging
import pdb

_logger = logging.getLogger(__name__)


class MgmtsystemNonconformity(models.Model):

    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity"
    _rec_name = "name"
    _inherit = ['mail.thread']
    _order = "create_date desc"
    _track = {
        'field': {
            'mgmtsystem_nonconformity.subtype_analysis': (
                lambda s, c, u, o, ctx=None: o["stage_id"] == "mgmtsystem_nonconformity.stage_draft"
            ),
            'mgmtsystem_nonconformity.subtype_pending': (
                lambda s, c, u, o, ctx=None: o["stage_id"] == "mgmtsystem_nonconformity.stage_pending"
            ),
        },
    }

    # @api.model
    # def _get_stage_new(self):
        # return self.env['mgmtsystem.nonconformity.stage'].search(
            # [('is_starting', '=', True)],
            # limit=1)

    def _default_stage(self):
        """Return the default stage."""
        return self.env.ref('mgmtsystem_nonconformity.stage_draft')


    @api.model
    def _stage_groups(self,stages,domain,order):
        stage_ids = self.env['mgmtsystem.nonconformity.stage'].search([])
        return stage_ids


    name = fields.Char('Name')
    number_of_nonconformities = fields.Integer(
        '# of nonconformities', readonly=True, default=1)
    ref = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default="NEW"
    )
    date_deadline = fields.Datetime('Deadline', readonly=False,
                                  default=fields.Datetime.now())
    create_date = fields.Datetime('Create Date', readonly=True,
                                  default=fields.Datetime.now())

    number_of_nonconformities = fields.Integer(
        '# of nonconformities', readonly=True, default=1)
    days_since_updated = fields.Integer(
        readonly=True,
        compute='_compute_days_since_updated',
        store=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close',
        compute='_compute_number_of_days_to_close',
        store=True,
        readonly=True)
    closing_date = fields.Datetime('Closing Date', readonly=True, default=lambda self: fields.Datetime.now())

    cancel_date = fields.Datetime('Cancel Date', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=False)
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
    user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user,
        track_visibility=True,
    )
    author_user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user,
        track_visibility=True
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

    system_id = fields.Many2one('mgmtsystem.system', 'System')

    stage_id = fields.Many2one(
        'mgmtsystem.nonconformity.stage',
        'Stage',
        track_visibility='onchange', index=True,
        copy=False,
        default=_default_stage, group_expand='_stage_groups')

    state = fields.Selection(
        related='stage_id.state',
        store=True,
    )
    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
         ('done', 'Ready for next stage'),
         ('blocked', 'Blocked')],
        'Kanban State',
        default='normal',
        track_visibility='onchange', index=True,
        help="A kanban state indicates special situations affecting it:\n"
        " * Normal is the default situation\n"
        " * Blocked indicates something is preventing"
        " the progress of this task\n"
        " * Ready for next stage indicates the"
        " task is ready to be pulled to the next stage",
        required=True, copy=False)

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
    priority = fields.Selection([
            ('0','Low'),
            ('1','Normal'),
            ('2','High')
        ], default='0', index=True)

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

    @api.multi
    def _track_template(self, tracking):
        self.ensure_one()
        res = super(MgmtsystemNonconformity, self)._track_template(tracking)
        changes, dummy = tracking[self.id]
        if 'stage_id' in changes and self.stage_id.mail_template_id:
            res['stage_id'] = (self.stage_id.mail_template_id, {'composition_mode': 'mass_mail'})
        return res

    @api.onchange('state')
    def _onchange_state_analysis(self, force_send=True):
        for nc in self:
            if nc.state == 'analysis':
                self.stage_id = self.env.ref('mgmtsystem_nonconformity.stage_analysis')

    @property
    @api.multi
    def verbose_name(self):
        return self.env['ir.model'].search([('model', '=', self._name)]).name

    @api.multi
    def _get_all_actions(self):
        self.ensure_one()
        return (self.action_ids +
                self.corrective_action_id +
                self.preventive_action_id)


    @api.constrains('stage_id')
    def _check_pending_approval(self):
        for nc in self:
            if nc.state == 'pending' and not nc.analysis_date:
                raise models.ValidationError(
                    _("Approve Analysis first"
                      "."))


    @api.constrains('stage_id')
    def _check_open_with_action_comments(self):
        for nc in self:
            if nc.state == 'open' and not nc.action_comments:
                raise models.ValidationError(
                    _("Action plan  comments are required "
                      "in order to put a nonconformity In Progress."))


    @api.constrains('stage_id')
    def _check_pending_action_plan_approval(self):
        for nc in self:
            if nc.state == 'open' and not nc.actions_date:
                raise models.ValidationError(
                    _("The Actionplan needs to be approved by a Manager"
                      "."))


    @api.constrains('stage_id')
    def _check_close_with_evaluation(self):
        for nc in self:
            if nc.state == 'done':
                if not nc.evaluation_comments:
                    raise models.ValidationError(
                        _("Evaluation Comments are required "
                          "in order to close a Nonconformity."))
                actions_are_closed = (
                    x.stage_id.is_ending
                    for x in nc._get_all_actions())
                if not all(actions_are_closed):
                    raise models.ValidationError(
                        _("All actions must be done "
                          "before closing a Nonconformity."))

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.depends('write_date')
    def _compute_days_since_updated(self):
        for nc in self:
            nc.days_since_updated = self._elapsed_days(
                nc.create_date,
                nc.write_date)


    @api.model
    def create(self, vals):
        nonconformity = super(MgmtsystemNonconformity, self).create(vals)
        vals.update({
            'ref': self.env['ir.sequence'].next_by_code('mgmtsystem.nonconformity')
        })
        nonconformity.message_subscribe_users(user_ids=[nonconformity.responsible_user_id.id])
        return nonconformity

    # @api.multi
    # def message_auto_subscribe(self, updated_fields, values=None):
        # """Add the responsible, manager and OpenChatter follow list."""
        # self.ensure_one()
        # users = [
            # self.responsible_user_id.id,
            # self.manager_user_id.id,
            # self.author_user_id.id,
        # ]
        # self.message_subscribe_users(user_ids=users, subtype_ids=None)
        # return super(MgmtsystemNonconformity, self).message_auto_subscribe(
            # updated_fields=updated_fields,
            # values=values
        # )

    @api.multi
    def write(self, vals):
        is_writing = 'is_writing' in self.env.context
        is_state_change = 'stage_id' in vals or 'state' in vals
        # Reset Kanban State on Stage change
        if is_state_change:
            was_not_open = {
                x.id: x.state in ('draft',
                                  'analysis', 'pending') for x in self}
            for nc in self:
                if nc.kanban_state != 'normal':
                    vals['kanban_state'] = 'normal'

        result = super(MgmtsystemNonconformity, self).write(vals)

        # Set/reset the closing date
        if not is_writing and is_state_change:
            for nc in self.with_context(is_writing=True):
                # On Close set Closing Date
                if nc.state == 'done' and not nc.closing_date:
                    nc.closing_date = fields.Datetime.now()
                # On reopen resete Closing Date
                if nc.state != 'done' and nc.closing_date:
                    nc.closing_date = None
                # On action plan approval, Open the Actions
                if nc.state == 'open' and was_not_open[nc.id]:
                    for action in nc._get_all_actions():
                        if action.stage_id.is_starting:
                            action.case_open()
        return result


    @api.multi
    def wkf_analysis(self):
        """Change state from draft to analysis"""
        return self.write({
            'state': 'analysis',
            'analysis_date': None,
            'analysis_user_id': None,
            'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_analysis').id,
            }
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
    def wkf_planing(self):
        """Change state from analysis to pending approval"""
        for o in self:
            if not o.analysis_date:
                raise exceptions.ValidationError(
                    _('Analysis must be performed before submitting to '
                      'Action planning.')
                )
        return self.write({
            'state': 'pending',
            'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_pending').id,
            'actions_date': None,
            'actions_user_id': None}
        )

    @api.multi
    def wkf_review(self):
        """Change state to review"""
        return self.write({
        'state': 'review',
        'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_review').id,
        })

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
            'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_open').id,
            'evaluation_date': False,
            'evaluation_user_id': False,
        })

    @api.one
    def action_sign_evaluation(self):
        """Sign-off the effectiveness evaluation"""
        if self.state != 'review':
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
        return self.write({
            'state': 'cancel',
            'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_cancel').id,
            })

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
        return self.write({
            'state': 'done',
            'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_done').id,
            })

    @api.multi
    def case_reset(self):
        """Reset to Draft and restart the workflow"""
        wf_service = netsvc.LocalService("workflow")
        for nc in self:
            wf_service.trg_create(self._uid, self._name, nc.id, self._cr)
        return self.write({
            'state': 'draft',
            'stage_id': self.env.ref('mgmtsystem_nonconformity.stage_draft').id,
            'analysis_date': None, 'analysis_user_id': None,
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
        })

    def get_nonconformity_url(self):
        """Return nonconformity url to be used in email templates."""
        base_url = self.env['ir.config_parameter'].get_param(
            'web.base.url',
            default='http://localhost:8069'
        )
        url = ('{}/web#db={}&id={}&model={}').format(
            base_url,
            self.env.cr.dbname,
            self.id,
            self._name
        )
        return url

    @api.model
    def process_nonconformity_reminder_queue(self, reminder_days=10):
        """Notify user when we are 10 days close to a deadline."""
        cur_date = datetime.now().date() + timedelta(days=reminder_days)
        stage_close = self.env.ref('mgmtsystem_nonconformity.stage_close')
        nonconformity_ids = self.search(
            [("stage_id", "!=", stage_close.id),
             ("action_ids.stage_id", "!=", stage_close.id),
             ("date_deadline", "=", cur_date),
             ])
        template = self.env.ref(
            'mgmtsystem_nonconformity.nonconformity_email_template_reminder')
        for nonconformity in nonconformity_ids:
            template.send_mail(nonconformity.id, force_send=True)
        return True
