# -*- coding: utf-8 -*-
#    Copyright (C) 2017 Eugen Don (<http://www.don-systems.de>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, netsvc, exceptions, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from odoo.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
)
import time

class MgmtsystemNonconformity(models.Model):

    _inherit = ['mgmtsystem.nonconformity']

    analysis_user_id = fields.Many2one(
        'res.users',
        'Analysis by',
        readonly=True,
        track_visibility='onchange',
    )
    analysis_date = fields.Datetime(
        'Analysis Date',
        readonly=True,
        track_visibility='onchange',
    )
    actions_date = fields.Datetime('Action Plan Date', readonly=True)
    actions_user_id = fields.Many2one(
        'res.users',
        'Action Plan by',
        readonly=True,
    )
    # 4. Effectiveness Evaluation
    evaluation_date = fields.Datetime('Evaluation Date', readonly=True)
    evaluation_user_id = fields.Many2one(
        'res.users',
        'Evaluation by',
        readonly=True,
    )

    @api.model
    def _default_stage(self):
        """Return the default stage."""
        return (
            self.env.ref('mgmtsystem_nonconformity.stage_draft', False) or
            self.env['mgmtsystem.nonconformity.stage'].search(
                [('is_starting', '=', True)],
                limit=1))

    @api.onchange('state')
    def _onchange_state_analysis(self, force_send=True):
        for nc in self:
            if nc.state == 'analysis':
                self.stage_id = self.env.ref('mgmtsystem_nonconformity.stage_analysis')

    @api.constrains('stage_id')
    def _check_pending_action_plan_approval(self):
        for nc in self:
            if nc.state == 'open' and not nc.actions_date:
                raise models.ValidationError(
                    _("The Actionplan needs to be approved by a Manager"
                      "."))

    @api.constrains('stage_id')
    def _check_pending_approval(self):
        for nc in self:
            if nc.state == 'pending' and not nc.analysis_date:
                raise models.ValidationError(
                    _("Approve Analysis first"
                      "."))

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
    def wkf_planing(self):
        """Change state from analysis to pending approval"""
        for o in self:
            if not o.analysis_date:
                raise exceptions.ValidationError(
                    _('Analysis must be approved first.')
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
    def wkf_open(self):
        """Change state from pending approval to in progress, and Open
        the related actions
        """
        self.ensure_one()
        if not self.actions_date:
            raise exceptions.ValidationError(
                _('Action plan must be approved first.')
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
    def case_reset(self):
        """Reset to Draft and restart the workflow"""
        wf_service = netsvc.LocalService("workflow")
        for nc in self:
            wf_service.trg_create(self._uid, self._name, nc.id, self._cr)
        return self.write({
            'state': 'draft',
            'stage_id': self._default_stage(),
            'analysis_date': None, 'analysis_user_id': None,
            'actions_date': None, 'actions_user_id': None,
            'evaluation_date': None, 'evaluation_user_id': None,
        })
