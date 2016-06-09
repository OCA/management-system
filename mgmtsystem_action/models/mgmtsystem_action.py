# -*- coding: utf-8 -*-

from openerp import fields, models, api
from datetime import datetime, timedelta


def _own_company(self):
    """Return the user company id."""
    return self.env.user.company_id.id


def _owner(self):
    """Return the user."""
    return self.env.user


class MgmtSystemAction(models.Model):
    """Model class that manage action."""

    _name = "mgmtsystem.action"
    _description = "Action"
    # _inherit = "crm.claim"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char('Subject', required=True)
    active = fields.Boolean('Active', default=True)
    opening_date = fields.Datetime('Opening Date', readonly=True)
    create_date = fields.Datetime('Creation Date', readonly=True)
    date_deadline = fields.Date('Deadline')
    date_closed = fields.Datetime('Closed', readonly=True)
    date = fields.Date('Action Date', default=fields.datetime.now(),
                       select=True)
    number_of_days_to_open = fields.Integer(
        '# of days to open', readonly=True, default=0)
    number_of_days_to_close = fields.Integer(
        '# of days to close', readonly=True, default=0)
    reference = fields.Char('Reference', required=True,
                            readonly=True, default="NEW")
    user_id = fields.Many2one(
        'res.users', 'Responsible', default=_owner, required=True)
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
        'res.company', 'Company', default=_own_company)

    stage_id = fields.Many2one(
        'mgmtsystem.action.stage',
        'Stage',
        default=lambda self: self._get_default_stage()
    )

    @api.model
    def _get_default_stage(self):
        """Return the default stage."""
        return self.env['mgmtsystem.action.stage'].search([
            ('is_starting', '=', True)
        ]).id

    @api.multi
    def case_open(self):
        """ Opens case """

        for case in self:
            values = {'active': True}

            stages = self.env['mgmtsystem.action.stage']
            values['stage_id'] = stages.search([
                ['is_ending', '=', False],
                ['is_starting', '=', False]
            ]).id

            case.write(values)

        return True

    @api.model
    def create(self, vals):
        """Creation of Action."""
        vals.update({
            'reference': self.env['ir.sequence'].next_by_code(
                'mgmtsystem.action'
            )
        })
        if vals.get('opening_date'):
            vals['opening_date'] = None
        action = super(MgmtSystemAction, self).create(vals)
        self.send_mail_for_action(action)
        return action

    @api.multi
    def write(self, vals):
        """Update user data."""
        if vals.get('stage_id'):
            stage_open = self.env.ref('mgmtsystem_action.stage_open')
            stage_close = self.env.ref('mgmtsystem_action.stage_close')
            if vals['stage_id'] == stage_open.id:
                vals['opening_date'] = datetime.now()
                vals['date_closed'] = None
                self.number_of_days_to_open = (
                    datetime.now() - datetime.strptime(self.create_date,
                                                       "%Y-%m-%d %H:%M:%S")
                ).days
                self.number_of_days_to_close = 0
            if vals['stage_id'] == stage_close.id:
                vals['date_closed'] = datetime.now()
                self.number_of_days_to_close = (
                    datetime.now() - datetime.strptime(self.create_date,
                                                       "%Y-%m-%d %H:%M:%S")
                ).days
        result = super(MgmtSystemAction, self).write(vals)
        return result

    def send_mail_for_action(self, action):
        """Set a document state as draft and notified the reviewers."""
        template = self.env.ref(
            'mgmtsystem_action.email_template_new_action_reminder')

        template.send_mail(action.id, force_send=True)
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
    def _stage_groups(self, present_ids, domain, **kwargs):
        """This method is used by KanBan view to show empty stages."""
        stage_obj = self.env['mgmtsystem.action.stage']

        # perform search
        stage_ids = stage_obj._search([])
        result = stage_obj.search([]).name_get()
        # restore order of the search
        result.sort(lambda x, y: cmp(
            stage_ids.index(x[0]), stage_ids.index(y[0])))

        return result, None

    @api.model
    def process_reminder_queue(self):
        """Notify user when we are 10 days close to a deadline."""
        cur_date = datetime.now().date() + timedelta(days=10)
        stage_close = self.env.ref('mgmtsystem_action.stage_close')
        action_obj = self.pool.get("mgmtsystem.action")
        action_ids = self.pool.get("mgmtsystem.action").search(
            self.env.cr, self.env.uid, [
                "&",
                ("stage_id", "!=", stage_close.id),
                ("date_deadline", "=", cur_date)]
        )

        if action_ids:
            for action_id in action_ids:
                action = action_obj.browse(
                    self.env.cr, self.env.uid,
                    action_id, context=self.env.context
                )
                template = self.env.ref(
                    'mgmtsystem_action.action_email_template_reminder_action')
                template.send_mail(action.id, force_send=True)
            return True

    _group_by_full = {
        'stage_id': _stage_groups
    }
