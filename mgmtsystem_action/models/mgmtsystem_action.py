# -*- coding: utf-8 -*-
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

from urllib import urlencode
from urlparse import urljoin

from openerp.tools.translate import _
from openerp.osv import fields, orm
from openerp.addons.crm import crm


class MgmtsystemAction(orm.Model):
    _name = "mgmtsystem.action"
    _description = "Action"
    _inherit = "crm.claim"
    _columns = {
        'reference': fields.char(
            'Reference',
            size=64,
            required=True,
            readonly=True,
        ),
        'type_action': fields.selection(
            [
                ('immediate', 'Immediate Action'),
                ('correction', 'Corrective Action'),
                ('prevention', 'Preventive Action'),
                ('improvement', 'Improvement Opportunity')
            ],
            'Response Type',
        ),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        'company_id': fields.many2one('res.company', 'Company'),
        # Override state fields by adding the track_visibility option that
        # allow to add the changes in the chatter
        'state': fields.related(
            'stage_id', 'state', type="selection", store=True,
            track_visibility='onchange',
            selection=crm.AVAILABLE_STATES, string="Status", readonly=True,
            help="The status is set to 'Draft', when a case is created.\
                If the case is in progress the status is set to 'Open'.\
                When the case is over, the status is set to 'Done'.\
                If the case needs to be reviewed then the status is \
                set to 'Pending'."),
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c:
            self.pool['res.users'].browse(cr, uid, uid, c).company_id.id),
        'reference': 'NEW',
        'state': 'draft',
    }

    def create(self, cr, uid, vals, context=None):
        sequence_pool = self.pool['ir.sequence']
        vals.update(reference=sequence_pool.get(cr, uid, 'mgmtsystem.action'))
        return super(MgmtsystemAction, self).create(
            cr, uid, vals, context=context
        )

    def message_auto_subscribe(
            self, cr, uid, ids, updated_fields, context=None, values=None):
        """Automatically add the responsible user to the follow list."""
        for o in self.browse(cr, uid, ids, context=context):
            self.message_subscribe_users(
                cr, uid, ids, user_ids=[o.user_id.id], subtype_ids=None,
                context=context
            )
        return super(MgmtsystemAction, self).message_auto_subscribe(
            cr, uid, ids, updated_fields, context=context, values=values
        )

    def do_close(self, cr, uid, ids, context=None):
        """When Action is closed, post a message on the related NC's chatter"""
        for o in self.browse(cr, uid, ids, context=context):
            for nc in o.nonconformity_ids:
                nc.case_send_note(_('Action "%s" was closed.' % o.name))
        return super(MgmtsystemAction, self).case_close(
            cr, uid, ids, context=context
        )

    def do_pending(self, cr, uid, ids, context=None):
        """Marks case as pending"""
        return self.write(cr, uid, ids, {'state': 'pending'}, context=context)

    def do_cancel(self, cr, uid, ids, context=None):
        """ Cancels case """
        self.write(cr, uid, ids, {
            'state': 'cancel', 'active': True}, context=context)
        return True

    def do_open(self, cr, uid, ids, context=None):
        """ Opens case """
        cases = self.browse(cr, uid, ids, context=context)
        for case in cases:
            data = {'active': True}
            if not case.user_id:
                data['user_id'] = uid
            data['state'] = 'open'
            self.write(cr, uid, ids, data, context=context)
        return True

    def get_action_url(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        action = self.browse(cr, uid, ids[0], context=context)
        base_url = self.pool['ir.config_parameter'].get_param(
            cr, uid, 'web.base.url', default='http://localhost:8069',
            context=context,
        )
        query = {'db': cr.dbname}
        fragment = {'id': action.id, 'model': self._name}
        return urljoin(base_url, "?%s#%s" % (
            urlencode(query), urlencode(fragment)
        ))
