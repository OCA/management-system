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

from openerp import models, api, fields, exceptions, _

from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
    DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT,
)

import time


class MgmtsystemNonconformity(models.Model):

    _name = "mgmtsystem.nonconformity"
    _description = "Nonconformity"
    _rec_name = "description"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = "create_date desc"
    _track = {
        'field': {
            'mgmtsystem_nonconformity.subtype_analysis': (
                lambda s, o: o["state"] == "analysis"
            ),
            'mgmtsystem_nonconformity.subtype_pending': (
                lambda s, o: o["state"] == "pending"
            ),
        },
    }

    _STATES = [
        ('draft', _('Draft')),
        ('analysis', _('Analysis')),
        ('pending', _('Pending Approval')),
        ('open', _('In Progress')),
        ('done', _('Closed')),
        ('cancel', _('Cancelled')),
    ]
    _STATES_DICT = dict(_STATES)

    name = fields.Char('Name')

    # 1. Description
    ref = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default="NEW"
    )

    # Compute data
    number_of_nonconformities = fields.Integer(
        '# of nonconformities', readonly=True, default=1)
    age = fields.Integer('Age', readonly=True,
                         compute='_compute_age', store=True)
    number_of_days_to_analyse = fields.Integer(
        '# of days to analyse', compute='_compute_number_of_days_to_analyse',
        store=True, readonly=True)
    number_of_days_to_plan = fields.Integer(
        '# of days to plan', compute='_compute_number_of_days_to_plan',
        store=True, readonly=True)
    number_of_days_to_execute = fields.Integer(
        '# of days to execute', compute='_compute_number_of_days_to_execute',
        store=True, readonly=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close', compute='_compute_number_of_days_to_execute',
        store=True, readonly=True)

    create_date = fields.Date(
        'Creation Date',
        required=True,
        default=lambda *a: time.strftime(DATE_FORMAT)
    )
    closing_date = fields.Datetime('Closing Date', readonly=True)
    cancel_date = fields.Datetime('Cancel Date', readonly=True)

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    reference = fields.Char('Related to')
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
        track_visibility="onchange"
    )
    manager_user_id = fields.Many2one(
        'res.users',
        'Manager',
        required=True,
        track_visibility="onchange"
    )
    author_user_id = fields.Many2one(
        'res.users',
        'Filled in by',
        required=True,
        default=lambda self: self.env.user.id,
        track_visibility="onchange"
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

    def _compute_age(self):
        return self._elapsed_days(
            self.create_date, time.strftime(DATETIME_FORMAT))

    @api.depends('analysis_date', 'create_date')
    def _compute_number_of_days_to_analyse(self):
        for nc in self:
            nc.number_of_days_to_close_open = nc._elapsed_days(
                nc.create_date,
                nc.analysis_date)

    @api.depends('closing_date', 'create_date')
    def _compute_number_of_days_to_close(self):
        for nc in self:
            nc.number_of_days_to_close_open = nc._elapsed_days(
                nc.create_date,
                nc.closing_date)

    @api.depends('actions_date', 'analysis_date')
    def _compute_number_of_days_to_plan(self):
        for nc in self:
            nc.number_of_days_to_close_open = nc._elapsed_days(
                nc.analysis_date,
                nc.actions_date)

    @api.depends('evaluation_date', 'actions_date')
    def _compute_number_of_days_to_execute(self):
        for nc in self:
            nc.number_of_days_to_close_open = nc._elapsed_days(
                nc.actions_date,
                nc.evaluation_date)

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = self._STATES_DICT.get(o.state, o.state)
        return res

    @property
    @api.multi
    def verbose_name(self):
        return self.env['ir.model'].search([('model', '=', self._name)]).name

    @api.model
    def create(self, vals):
        vals.update({
            'ref': self.env['ir.sequence'].next_by_code(
                'mgmtsystem.nonconformity')
        })

        return super(MgmtsystemNonconformity, self).create(vals)

    @api.multi
    def message_auto_subscribe(self, updated_fields, values=None):
        """
        Add the responsible, manager and author to the OpenChatter follow list
        """
        self.ensure_one()

        # user_ids = [
        #    self.responsible_user_id._uid,
        #    self.manager_user_id._uid,
        #    self.author_user_id._uid,
        # ]
        # self.message_subscribe_users(user_ids=user_ids)

        return super(MgmtsystemNonconformity, self).message_auto_subscribe(
            updated_fields=updated_fields,
            values=values
        )

    @api.multi
    def write(self, vals):
        """Update user data."""
        if vals.get('state'):
            if vals.get('state') == "analysis":
                vals.update(self.do_analysis())
            if vals.get('state') == "pending":
                vals.update(self.do_review())
            if vals.get('state') == "open":
                vals.update(self.do_open())
            if vals.get('state') == "done":
                vals.update(self.do_close())
            if vals.get('state') == "cancel":
                vals.update(self.do_cancel())
            if vals.get('state') == "draft":
                vals.update(self.case_reset())

        result = super(MgmtsystemNonconformity, self).write(vals)
        return result

    def check_closed_or_cancelled(self):
        if self.cancel_date or self.closing_date:
            raise exceptions.ValidationError(
                _('Please reset the process to draft, to perform it again')
            )

    def do_analysis(self):
        """Change state from draft to analysis."""
        self.check_closed_or_cancelled()
        return {
            'state': 'analysis',
            'analysis_date': None,
            'analysis_user_id': None,
            'actions_date': None,
            'actions_user_id': None}

    @api.multi
    def do_review(self):
        """Change state from analysis to pending approval"""
        self.check_closed_or_cancelled()
        for o in self:
            if not o.analysis_date:
                raise exceptions.ValidationError(
                    _('Analysis must be performed before submitting to '
                      'approval.')
                )
        return {
            'state': 'pending',
            'actions_date': None,
            'actions_user_id': None}

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
            'analysis_user_id': self._uid
        })
        self.message_post(
            body='%s <b>%s</b>' % (self.verbose_name, _('Analysis Approved'))
        )
        return True

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
    def do_open(self):
        """Change state from pending approval to in progress, and Open
        the related actions
        """
        self.ensure_one()
        self.check_closed_or_cancelled()
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
        return {
            'state': 'open',
            'evaluation_date': False,
            'evaluation_user_id': False,
        }

    @api.multi
    def action_sign_evaluation(self):
        """Sign-off the effectiveness evaluation"""
        self.ensure_one()
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

    def do_cancel(self):
        """Change state to cancel."""
        if self.closing_date:
            raise exceptions.ValidationError(
                _('A close process cannot be cancelled')
            )
        return {'state': 'cancel',
                'cancel_date': time.strftime(DATETIME_FORMAT)}

    @api.multi
    def do_close(self):
        """Change state from in progress to closed"""
        self.ensure_one()

        if (not self.env.ref('mgmtsystem.group_mgmtsystem_manager') in
            self.env.user.groups_id and
            not self.env.ref('mgmtsystem.group_mgmtsystem_auditor') in
                self.env.user.groups_id):
            raise exceptions.ValidationError(
                _("You don't have the right to close a non conformity.")
            )

        if self.cancel_date:
            raise exceptions.ValidationError(
                _('A cancel process cannot be closed')
            )
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

        return {
            'state': 'done',
            'closing_date': time.strftime(DATETIME_FORMAT),
        }

    def case_reset(self):
        """Reset to Draft."""
        if not self.cancel_date and not self.closing_date:
            raise exceptions.ValidationError(
                _('Only a close or cancel process can be reset')
            )
        return {
            'state': 'draft',
            'closing_date': None, 'cancel_date': None,
            'analysis_date': None, 'analysis_user_id': None,
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
            'number_of_days_to_close': None, 'number_of_days_to_analyse': None,
            'number_of_days_to_plan': None, 'number_of_days_to_execute': None,
        }

    @api.model
    def state_groups(self, present_ids, domain, **kwargs):
        folded = {key: (key in self._state_name()) for key, _ in self._STATES}
        # Need to copy state_name list before returning it,
        # because odoo modifies the list it gets,
        # emptying it in the process. Bad odoo!
        return self._STATES[:], folded

    _group_by_full = {
        'state': state_groups
    }

    def _read_group_fill_results(self, cr, uid, domain, groupby,
                                 remaining_groupbys, aggregated_fields,
                                 count_field, read_group_result,
                                 read_group_order=None, context=None):
        """
        The method seems to support grouping using m2o fields only,
        while we want to group by a simple status field.
        Hence the code below - it replaces simple status values
        with (value, name) tuples.
        """
        if groupby == 'state':
            STATES_DICT = dict(self._STATES)
            for result in read_group_result:
                state = result['state']
                result['state'] = (state, STATES_DICT.get(state))

        return super(MgmtsystemNonconformity, self)._read_group_fill_results(
            cr, uid, domain, groupby, remaining_groupbys, aggregated_fields,
            count_field, read_group_result, read_group_order, context
        )
