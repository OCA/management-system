
from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta


class MgmtsystemAction(models.Model):
    _name = "mgmtsystem.action"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Action"
    _order = "priority desc, sequence, id desc"

    def _default_company(self):
        return self.env.user.company_id

    def _default_owner(self):
        return self.env.user

    def _default_stage(self):
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

    @api.depends('date_open', 'create_date')
    def _compute_number_of_days_to_open(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date,
                action.date_open)

    @api.depends('date_closed', 'create_date')
    def _compute_number_of_days_to_close(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date,
                action.date_closed)

    name = fields.Char('Subject', required=True)
    active = fields.Boolean('Active', default=True)

    priority = fields.Selection(
        [
            ('0', 'Low'),
            ('1', 'Normal'),
        ], default='0', index=True, string="Priority")

    sequence = fields.Integer(
        'Sequence',
        index=True, default=10,
        help="Gives the sequence order when displaying a list of actions."
    )

    date_deadline = fields.Date('Deadline')

    date_open = fields.Datetime(
        'Opening Date',
        readonly=True, oldname='opening_date'
    )

    date_closed = fields.Datetime('Closed Date', readonly=True)

    number_of_days_to_open = fields.Integer(
        '# of days to open',
        compute=_compute_number_of_days_to_open,
        store=True)
    number_of_days_to_close = fields.Integer(
        '# of days to close',
        compute=_compute_number_of_days_to_close,
        store=True)

    reference = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default=lambda self: _('New'))

    user_id = fields.Many2one(
        'res.users',
        'Responsible',
        default=_default_owner,
        required=True,
    )

    description = fields.Html('Description')

    type_action = fields.Selection(
        [
            ('immediate', 'Immediate Action'),
            ('correction', 'Corrective Action'),
            ('prevention', 'Preventive Action'),
            ('improvement', 'Improvement Opportunity')
        ], 'Response Type', required=True)

    system_id = fields.Many2one('mgmtsystem.system', 'System')

    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=_default_company,
    )

    stage_id = fields.Many2one(
        'mgmtsystem.action.stage',
        'Stage',
        track_visibility='onchange', index=True,
        copy=False,
        default=_default_stage, group_expand='_stage_groups',
    )

    tag_ids = fields.Many2many('mgmtsystem.action.tag', string='Tags')

    @api.model
    def _stage_groups(self, stages=None, domain=None, order=None):
        return self.env['mgmtsystem.action.stage'].search([], order=order)

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            Sequence = self.env['ir.sequence']
            vals['reference'] = Sequence.next_by_code('mgmtsystem.action')
        action = super(MgmtsystemAction, self).create(vals)
        self.send_mail_for_action(action)
        return action

    @api.constrains('stage_id')
    def _check_stage_id(self):
        for rec in self:
            # Do not allow to bring back actions to draft
            if rec.date_open and rec.stage_id.is_starting:
                raise exceptions.ValidationError(
                    _('We cannot bring back the action to draft stage'))
            # If stage is changed, the action is opened
            if not rec.date_open and not rec.stage_id.is_starting:
                rec.date_open = fields.Datetime.now()
            # If stage is ending, set closed date
            if not rec.date_closed and rec.stage_id.is_ending:
                rec.date_closed = fields.Datetime.now()

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

    @api.model
    def _get_stage_open(self):
        return self.env.ref('mgmtsystem_action.stage_open')

    @api.multi
    def case_open(self):
        """ Opens case """
        for case in self:
            case.write({
                'active': True,
                'stage_id': case._get_stage_open().id})
        return True
