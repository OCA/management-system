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

from osv import fields, orm


class mgmtsystem_claim(orm.Model):
    _name = "mgmtsystem.claim"
    _description = "Claim"
    _inherit = "crm.claim"
    _columns = {
        'reference': fields.char(
            'Reference',
            size=64,
            required=True,
            readonly=True,
        ),
        'message_ids': fields.one2many(
            'mail.message',
            'res_id',
            'Messages',
            domain=[('model', '=', _name)],
        ),
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c:
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id),
        'reference': 'NEW',
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'reference': self.pool.get('ir.sequence').get(
                cr, uid, 'mgmtsystem.claim'
            )
        })
        return super(mgmtsystem_claim, self).create(cr, uid, vals, context)
