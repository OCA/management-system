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

from tools.translate import _
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

    def message_auto_subscribe(self, cr, uid, ids, updated_fields, context=None):
        """Automatically add the responsible user to the follow list."""
        for o in self.browse(cr, uid, ids, context=context):
            self.message_subscribe_users(cr, uid, ids, user_ids=[o.user_id.id], subtype_ids=None, context=context)
        return super(mgmtsystem_action, self).message_auto_subscribe(cr, uid, ids, updated_fields, context=context)

    def case_close(self, cr, uid, ids, context=None):
        """When Action is closed, post a message on the related NC's chatter"""
        for o in self.browse(cr, uid, ids, context=context):
            for nc in o.nonconformity_ids:
                nc.case_send_note(_('Action "%s" was closed.' % o.name))
        return super(mgmtsystem_action, self).case_close(cr, uid, ids, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
