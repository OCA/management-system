# -*- coding: utf-8 -*-

from urllib import urlencode
from urlparse import urljoin
from openerp import fields, models, api


def own_company(self):
    return self.env.user.company_id.id


class mgmtsystem_action(models.Model):
    _name = "mgmtsystem.action"
    _description = "Action"
    _inherit = "crm.claim"

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
        vals.update({
            'reference': self.env['ir.sequence'].get('mgmtsystem.action')
        })
        return super(mgmtsystem_action, self).create(vals)

    @api.multi
    def message_auto_subscribe(self, updated_fields, values=None):
        """Automatically add the responsible user to the follow list."""
        for o in self:
            self.message_subscribe_users(user_ids=[o.user_id.id],
                                         subtype_ids=None)

        base = super(mgmtsystem_action, self)
        return base.message_auto_subscribe(updated_fields, values=values)

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

    @api.one
    def get_action_url(self):
        config_parameter = self.env['ir.config_parameter']
        base_url = config_parameter.get_param('web.base_url',
                                              default='http://localhost:8069')

        query = {'db': self.env.cr.dbname}
        fragment = {'id': self.id, 'model': self._name}

        return urljoin(base_url, "?%s#%s" % (
            urlencode(query), urlencode(fragment)
        ))
