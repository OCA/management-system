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

<<<<<<< fdc5aa91e5e5e37a018d952a2dd7355266e54a36
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
from tools.translate import _
from urllib import urlencode
from urlparse import urljoin
from openerp.osv import fields, orm


class mgmtsystem_action(orm.Model):
    _name = "mgmtsystem.action"
    _description = "Action"
    _inherit = "crm.claim"
    _columns = {
        'reference': fields.char('Reference', size=64, required=True, readonly=True),
        'type_action': fields.selection([('immediate', 'Immediate Action'),
                                         ('correction', 'Corrective Action'),
                                         ('prevention', 'Preventive Action'),
                                         ('improvement', 'Improvement Opportunity')],
                                        'Response Type'),
<<<<<<< d983079c898ad179110ee539b2abb8fbf5517b48
        'message_ids': fields.one2many('mail.message',
                                       'res_id',
                                       'Messages',
                                       domain=[('model', '=', _name)]),
=======
>>>>>>> Adapted actions to openchatter, added autosubscribing and action closing posts
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
        'reference': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'reference': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.action')
        }, context=context)
        return super(mgmtsystem_action, self).create(cr, uid, vals, context=context)

    def message_auto_subscribe(self, cr, uid, ids, updated_fields, context=None, values=None):
        """Automatically add the responsible user to the follow list."""
        for o in self.browse(cr, uid, ids, context=context):
            self.message_subscribe_users(cr, uid, ids, user_ids=[o.user_id.id], subtype_ids=None, context=context)
        return super(mgmtsystem_action, self).message_auto_subscribe(cr, uid, ids, updated_fields, context=context, values=values)
=======
from openerp.tools.translate import _
=======
>>>>>>> Fix typo and pep8
from urllib import urlencode
from urlparse import urljoin
from openerp import fields, models, api

own_company = lambda self: self.env.user.company_id.id


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

            if not case.user_id:
                values['user_id'] = self.env.uid

            values['stage_id'] = self.stage_find(
                self, None, [('name', '=', 'In Progress')]
            )

            case.write(values)

        return True
>>>>>>> Ported mgmtsystem_action

    @api.multi
    def case_close(self):
        """When Action is closed, post a message on the related NC's chatter"""
<<<<<<< b276dff2f5e1c5caacf2291cbcd863d2a2e2fd84

<<<<<<< 22ac775a1ed32d9a73fa3338a4b6c15d7e7b3d41
        for o in self.browse(cr, uid, ids, context=context):
            for nc in o.nonconformity_ids:
                nc.case_send_note(_('Action "%s" was closed.' % o.name))
<<<<<<< e9712c2728b304ca591e2db163b1c6710aa9a773
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
        return super(mgmtsystem_action, self).case_close(cr, uid, ids, context=context)

    def get_action_url(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        action = self.browse(cr, uid, ids[0], context=context)
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url', default='http://localhost:8069', context=context)
        query = {'db': cr.dbname}
        fragment = {'id': action.id, 'model': self._name}
        return urljoin(base_url, "?%s#%s" % (urlencode(query), urlencode(fragment)))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
=======

>>>>>>> Removed comments and commented code
        return super(mgmtsystem_action, self).case_close(
            cr, uid, ids, context=context
        )
=======
        for o in self:
            if hasattr(o, 'nonconformity_ids'):
                for nc in o.nonconformity_ids:
                    nc.case_send_note(_('Action "%s" was closed.' % o.name))
>>>>>>> Added tests and updated code to v8

=======
        # for o in self:
        #     if hasattr(o, 'nonconformity_ids'):
        #         for nc in o.nonconformity_ids:
        #             nc.case_send_note(_('Action "%s" was closed.' % o.name))
>>>>>>> Updated according to reviews
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
>>>>>>> Ported mgmtsystem_action
