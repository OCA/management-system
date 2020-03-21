# -*- coding: utf-8 -*-

from openerp import fields, models, api
from datetime import datetime, timedelta


class MgmtSystemAction(models.Model):
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
        default=_default_stage)

    @api.model
    def _stage_groups(self, present_ids, domain, **kwargs):
        """This method is used by Kanban view to show empty stages."""
        # perform search
        stage_ids = self.env['mgmtsystem.action.stage']._search([])
        result = stage_ids.name_get()
        # restore order of the search
        result.sort(lambda x, y: cmp(
            stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, None

    _group_by_full = {
        'stage_id': _stage_groups
    }

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

    @api.multi
    def case_open(self):
        """ Opens case """
        for case in self:
            case.write({
                'active': True,
                'stage_id': case._get_stage_open.id})
        return True

    @api.model
    def create(self, vals):
        """Creation of Action."""
        Sequence = self.env['ir.sequence']
        vals['reference'] = Sequence.next_by_code('mgmtsystem.action')
        action = super(MgmtSystemAction, self).create(vals)
        action.send_mail_for_action()
        return action

    @api.multi
    def write(self, vals):
        """Update user data."""
        stage_open = self._get_stage_open()
        stage_close = self._get_stage_close()
        if vals['stage_id'] == stage_open.id:
            vals['opening_date'] = fields.Datetime.now()
            vals['date_closed'] = None
        if vals['stage_id'] == stage_close.id:
            vals['date_closed'] = fields.Datetime.now()
        return super(MgmtSystemAction, self).write(vals)

    def send_mail_for_action(self, action, force_send=True):
        """Set a document state as draft and notified the reviewers."""
        template = self.env.ref(
            'mgmtsystem_action.email_template_new_action_reminder')
        for action in self:
            template.send_mail(action, force_send=force_send)
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
            template.send_mail(action.id, force_send=True)
        return True
