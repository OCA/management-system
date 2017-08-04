# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta


class MgmtsystemAction(models.Model):
    """Model class that manage action."""

    _name = "mgmtsystem.action"
    _description = "Action"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    def _default_company(self):
        """Return the user company id."""
        return self.env.user.company_id

    def _default_owner(self):
        """Return the user."""
        return self.env.user

    def _default_stage(self):
        """Return the default stage."""
        return self.env['mgmtsystem.action.stage'].search(
            [('is_starting', '=', True)],
            limit=1)

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

    name = fields.Char('Subject', required=True)
    active = fields.Boolean('Active', default=True)
    date_deadline = fields.Date('Deadline')

    create_date = fields.Datetime('Create Date', readonly=True)
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
    reference = fields.Char('Reference', required=True,
                            readonly=True, default="NEW")
    user_id = fields.Many2one(
        'res.users', 'Responsible', default=_default_owner, required=True)
    description = fields.Text('Description')
    type_action = fields.Selection(
        [
            ('immediate', 'Immediate Action'),
            ('correction', 'Corrective Action'),
            ('prevention', 'Preventive Action'),
            ('improvement', 'Improvement Opportunity')
        ], 'Response Type', required=True)

    system_id = fields.Many2one('mgmtsystem.system', 'System')
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=_default_company)
    stage_id = fields.Many2one(
        'mgmtsystem.action.stage',
        'Stage',
        track_visibility='onchange', index=True,
        copy=False,
        default=_default_stage, group_expand='_stage_groups')

    @api.model
    def _stage_groups(self, stages, domain, order):
        stage_ids = self.env['mgmtsystem.action.stage'].search([])
        return stage_ids

    @api.model
    def _get_stage_new(self):
        return self.env['mgmtsystem.action.stage'].search(
            [('is_starting', '=', True)],
            limit=1)

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
        vals['reference'] = Sequence.next_by_code('mgmtsystem.action')
        action = super(MgmtsystemAction, self).create(vals)
        self.send_mail_for_action(action)
        return action

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

    @api.model
    def send_mail_for_action(self, action, force_send=True):
        template = self.env.ref(
            'mgmtsystem_action.email_template_new_action_reminder')
        template.send_mail(action.id, force_send=force_send)
        return True

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
            template.send_mail(action.id)
        return True
