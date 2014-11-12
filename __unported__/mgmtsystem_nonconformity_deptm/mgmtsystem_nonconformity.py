# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Daniel Reis
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

from openerp.osv import fields, orm


class mgmtsystem_nonconformity(orm.Model):
    _inherit = "mgmtsystem.nonconformity"
    _columns = {
        'department_id': fields.many2one(
            'hr.department',
            'Department',
            required=True,
        ),
        'superior_user_id': fields.many2one(
            'res.users',
            'Top Manager',
            required=True,
        ),
    }

    def onchange_department_id(self, cr, uid, ids, new_id, context=None):
        result = {}
        if new_id:
            deptm = self.pool['hr.department'].browse(
                cr, uid, new_id, context=context
            )
            if deptm.manager_id and deptm.manager_id.user_id:
                result['manager_user_id'] = deptm.manager_id.user_id.id
            parent_deptm = deptm.parent_id
            if (parent_deptm
                    and parent_deptm.manager_id
                    and parent_deptm.manager_id.user_id):
                result['superior_user_id'] = parent_deptm.manager_id.user_id.id
        return {'value': result}

    def message_auto_subscribe(
            self, cr, uid, ids, updated_fields, context=None, values=None):
        """Add the Top Manager to OpenChatter follow list."""
        o = self.browse(cr, uid, ids, context=context)[0]
        user_ids = [o.superior_user_id.id]
        self.message_subscribe_users(
            cr, uid, ids, user_ids=user_ids, subtype_ids=None, context=context)
        return super(mgmtsystem_nonconformity, self).message_auto_subscribe(
            cr, uid, ids, updated_fields=updated_fields, context=context,
            values=values
        )
