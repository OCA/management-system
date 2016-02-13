# -*- coding: utf-8 -*-

from urllib import urlencode
from urlparse import urljoin
from openerp import fields, models, api
import datetime


def own_company(self):
    return self.env.user.company_id.id


class MgmtSystemAction(models.Model):
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
        return self.env['mgmtsystem.action.stage'].search([
            ('is_starting', '=', True)
        ]).id

    @api.model
    def create(self, vals):
        """Creation of Action."""
        vals.update({
            'reference': self.env['ir.sequence'].get('mgmtsystem.action')
        })
        return super(MgmtSystemAction, self).create(vals)

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
            if values['stage_id'].name == 'In Progress':
                values['opening_date'] = datetime.now()
            case.write(values)

        return True

    @api.multi
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

    def create(self, cr, uid, vals, context=None):
        if opening_date in vals:
            vals['opening_date'] = None
        return super(MgmtSystemAction, self).create(cr, uid, vals, context)
