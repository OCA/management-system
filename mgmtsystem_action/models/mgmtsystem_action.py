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

from odoo import models, api, fields, netsvc, exceptions, _
from datetime import datetime, timedelta

import logging

_logger = logging.getLogger(__name__)


_STATES = [
    ('draft', _('Draft')),
    ('analysis', _('Analysis')),
    ('pending', _('Pending Approval')),
    ('open', _('In Progress')),
    ('done', _('Closed')),
    ('cancel', _('Cancelled')),
]
_STATES_DICT = dict(_STATES)


class MgmtsystemAction(models.Model):
    """Model class that manage action."""

    _name = "mgmtsystem.action"
    _description = "Action"
    _rec_name = "name"
    _inherit = ['mail.thread']
    _order = "date_deadline desc"
    _track = {
        'field': {
            'mgmtsystem_action.subtype_immediate': (
                lambda s, c, u, o, ctx=None: o["type_action"] == "immediate"
            ),
            'mgmtsystem_action.subtype_prevention': (
                lambda s, c, u, o, ctx=None: o["type_action"] == "prevention"
            ),
        },
    }

    def _state_name(self):
        res = dict()
        for o in self:
            res[o.id] = _STATES_DICT.get(o.state, o.state)
        return res

    def _default_company(self):
        """Return the user company id."""
        return self.env.user.company_id

    def _default_owner(self):
        """Return the user."""
        return self.env.user

    def _default_stage(self):
        """Return the default stage."""
        return self.env.ref('mgmtsystem_action.stage_draft')

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.depends('opening_date', 'create_date')
    def _compute_number_of_days_to_open(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date,
                action.opening_date)

    @api.depends('date_closed', 'create_date')
    def _compute_number_of_days_to_close(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date,
                action.date_closed)

    @api.model
    def _stage_groups(self,stages,domain,order):
        stage_ids = self.env['mgmtsystem.action.stage'].search([])
        return stage_ids


    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_project_id' in self.env.context:
            search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain
        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    @api.model
    def _get_stage_new(self):
        return self.env['mgmtsystem.action.stage'].search(
            [('is_starting', '=', True)],
            limit=1)

    name = fields.Char('Subject', required=True, default="Maßnahme")
    # 1. Description
    ref = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default="NEW"
    )
    active = fields.Boolean('Active', default=True)
    date_deadline = fields.Date('Deadline')

    create_date = fields.Datetime('Create Date', readonly=True,
                                  default=fields.datetime.now())
    cancel_date = fields.Datetime('Cancel Date', readonly=True)
    opening_date = fields.Datetime('Opening Date', readonly=True)
    date_closed = fields.Datetime('Closed Date', readonly=True)
    number_of_days_to_open = fields.Integer(
        '# of days to open',
        compute=_compute_number_of_days_to_open,
        store=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close',
        compute=_compute_number_of_days_to_close,
        store=True)
    reference = fields.Char('Related to', required=False,
                            readonly=False)
    user_id = fields.Many2one(
        'res.users', 'Responsible', default=_default_owner, required=True)
    description = fields.Text('Description')
    type_action = fields.Selection(
        [
            ('immediate', 'Immediate Action'),
            ('correction', 'Corrective Action'),
            ('prevention', 'Preventive Action'),
            ('improvement', 'Improvement Opportunity')
        ], 'Response Type', required=False, default="improvement")
    system_id = fields.Many2one('mgmtsystem.system', 'System')
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=_default_company)

    stage_id = fields.Many2one(
        'mgmtsystem.action.stage',
        'Stage',
        track_visibility='onchange', index=True,
        copy=False,
        default=_get_stage_new, group_expand='_stage_groups')

    @api.model
    def _get_stage_open(self):
        return self.env.ref('mgmtsystem_action.stage_open')

    @api.model
    def _get_stage_close(self):
        return self.env.ref('mgmtsystem_action.stage_close')

    @api.model
    def _get_stage_cancel(self):
        return self.env.ref('mgmtsystem_action.stage_cancel')

    @api.multi
    def case_open(self):
        """ Opens case """
        for case in self:
            case.write({
                'active': True,
                'stage_id': case._get_stage_open().id})
        return True

    @api.model
    def create(self, vals):
        """Creation of Action."""
        Sequence = self.env['ir.sequence']
        vals['ref'] = Sequence.next_by_code('mgmtsystem.action')
        action = super(MgmtsystemAction, self).create(vals)
        return action

    @api.multi
    def _track_template(self, tracking):
        self.ensure_one()
        res = super(MgmtsystemAction, self)._track_template(tracking)
        changes, dummy = tracking[self.id]
        if 'stage_id' in changes and self.stage_id.mail_template_id:
            res['stage_id'] = (self.stage_id.mail_template_id, {'composition_mode': 'mass_mail'})
        return res

    @api.multi
    def write(self, vals):
        """Update user data."""
        if vals.get('stage_id'):
            stage_new = self._get_stage_new()
            stage_open = self._get_stage_open()
            stage_close = self._get_stage_close()
            stage_cancel = self._get_stage_cancel()
            if vals['stage_id'] == stage_new.id:
                if self.opening_date:
                    raise exceptions.ValidationError(
                        _('We cannot bring back the action to draft stage')
                    )
                vals['cancel_date'] = None
                self.message_post(
                    body=' %s ' % (_('Action back to draft stage on ') +
                                   fields.Datetime.now())
                )
            if vals['stage_id'] == stage_open.id:
                vals['opening_date'] = fields.Datetime.now()
                self.message_post(
                    body=' %s ' % (_('Action opened on ') +
                                   vals['opening_date'])
                )
                vals['date_closed'] = None
                vals['cancel_date'] = None
            if vals['stage_id'] == stage_close.id:
                if not self.opening_date or self.cancel_date:
                    raise exceptions.ValidationError(
                        _('You should first open the action')
                    )
                vals['date_closed'] = fields.Datetime.now()
                self.message_post(
                    body=' %s ' % (_('Action closed on ') +
                                   vals['date_closed'])
                )
            if vals['stage_id'] == stage_cancel.id:
                vals['date_closed'] = None
                vals['opening_date'] = None
                vals['cancel_date'] = fields.Datetime.now()
                self.message_post(
                    body=' %s ' % (_('Action cancelled on ') +
                                   fields.Datetime.now())
                )
        return super(MgmtsystemAction, self).write(vals)

    @api.multi
    def send_mail_for_action(self, action, force_send=True):
        """Set a document state as draft and notified the reviewers."""
        template = self.env.ref('mgmtsystem_action.email_template_new_action_reminder')
        self.env['mail.template'].browse(template.id).send_mail(action.id, force_send=force_send)


    def get_action_url(self):
        """Return action url to be used in email templates."""
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
    def process_reminder_queue(self, reminder_days=10):
        """Notify user when we are 10 days close to a deadline."""
        cur_date = datetime.now().date() + timedelta(days=reminder_days)
        stage_close = self.env.ref('mgmtsystem_action.stage_close')
        action_ids = self.search(
            [("stage_id", "!=", stage_close.id),
             ("date_deadline", "=", cur_date)])
        template = self.env.ref(
            'mgmtsystem_action.action_email_template_reminder_action')
        for action in action_ids:
            template.send_mail(action.id, force_send=True)
        return True
