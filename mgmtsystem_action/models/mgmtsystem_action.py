# -*- coding: utf-8 -*-

from openerp import fields, models, api
from datetime import datetime, timedelta


def own_company(self):
    """Return the user company id."""
    return self.env.user.company_id.id


class MgmtSystemAction(models.Model):
    """Model class that manage action."""

    _name = "mgmtsystem.action"
    _description = "Action"
    _inherit = "crm.claim"

    opening_date = fields.Datetime('Opening Date', readonly=True)
    reference = fields.Char('Reference', required=True,
                            readonly=True, default="NEW")
    type_action = fields.Selection([
                                   ('immediate', 'Immediate Action'),
                                   ('correction', 'Corrective Action'),
                                   ('prevention', 'Preventive Action'),
                                   ('improvement', 'Improvement Opportunity')
                                   ], 'Response Type')

    system_id = fields.Many2one('mgmtsystem.system', 'System')
    company_id = fields.Many2one('res.company', 'System', default=own_company)

    stage_id = fields.Many2one(
        'mgmtsystem.action.stage',
        'Stage',
        default=lambda self: self.get_default_stage()
    )

    @api.model
    def get_default_stage(self):
        """Return the default stage."""
        return self.env['mgmtsystem.action.stage'].search([
            ('is_starting', '=', True)
        ]).id

    @api.model
    def create(self, vals):
        """Creation of Action."""
        vals.update({
            'reference': self.env['ir.sequence'].get('mgmtsystem.action')
        })
        if self.opening_date in vals:
            vals['opening_date'] = None
        template = self.env.ref(
            'mgmtsystem_action.email_template_new_action_reminder')
        action = super(MgmtSystemAction, self).create(vals)
        template.send_mail(action.id, force_send=True)
        return action

    @api.multi
    def write(self, vals):
        """Update user data."""
        stage_open = self.env.ref('mgmtsystem_action.stage_open')
        stage_close = self.env.ref('mgmtsystem_action.stage_close')
        if vals.get('stage_id'):
            if vals['stage_id'] == stage_open.id:
                vals['opening_date'] = datetime.now()
            if vals['stage_id'] == stage_close.id:
                vals['date_closed'] = datetime.now()

        result = super(MgmtSystemAction, self).write(vals)
        return result

    def send_mail_for_action(self, action):
        """Set a document state as draft and notified the reviewers."""
        template = self.env.ref(
            'mgmtsystem_action.email_template_new_action_reminder')

        template.send_mail(action.id, force_send=True)
        return True

#    @api.multi
#    def message_auto_subscribe(self, updated_fields, values=None):
#        """Automatically add the responsible user to the follow list."""
#        for o in self:
#            self.message_subscribe_users(user_ids=[o.user_id.id],
#                                         subtype_ids=None)
#
#        base = super(MgmtSystemAction, self)
#        return base.message_auto_subscribe(updated_fields, values=values)

    @api.multi
    def case_open(self):
        """Open case."""
        for case in self:
            values = {'active': True}

            stages = self.env['mgmtsystem.action.stage']
            values['stage_id'] = stages.search([
                ['is_ending', '=', False],
                ['is_starting', '=', False]
            ]).id

            case.write(values)

        return True

    def get_action_url(self):
        """Return action url."""
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
        stage_obj = self.env['mgmtsystem.action.stage']

        # perform search
        stage_ids = stage_obj._search([])
        result = stage_obj.search([]).name_get()
        # restore order of the search
        result.sort(lambda x, y: cmp(
            stage_ids.index(x[0]), stage_ids.index(y[0])))

        fold = {}
        for stage in stage_obj.browse(stage_ids):
            fold[stage.id] = True
        return result, None

    @api.model
    def process_reminder_queue(self):
        """Notify user when we are 10 days close to a deadline."""
        cur_date = datetime.now().date() + timedelta(days=10)
        stage_close = self.env.ref('mgmtsystem_action.stage_close')
        action_obj = self.pool.get("mgmtsystem.action")
        action_ids = self.pool.get("mgmtsystem.action").search(
            self.env.cr, self.env.uid, ["&", ("stage_id", "!=", stage_close.id), ("date_deadline", "=", cur_date)])

        for action_id in action_ids:
            action = action_obj.browse(
                self.env.cr, self.env.uid, action_id, context=self.env.context)
            template = self.env.ref(
                'mgmtsystem_action.action_email_template_reminder_action')
            template.send_mail(action.id, force_send=True)

    _group_by_full = {
        'stage_id': _stage_groups
    }
