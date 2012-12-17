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
        'department_id': fields.many2one('hr.department', 'Department', required=True),
        'superior_user_id': fields.many2one('res.users','Superior', required=True),
    }

    def onchange_department_id(self, cr, uid, ids, new_id, context=None):
        result = {}
        if new_id:
            deptm = self.pool.get('hr.department').browse(cr, uid, new_id, context=context)
            if deptm.manager_id and deptm.manager_id.user_id:
                result['manager_user_id'] = deptm.manager_id.user_id.id
            if deptm.parent_id and deptm.parent_id.manager_id and deptm.parent_id.manager_id.user_id:
                result['superior_user_id'] = deptm.parent_id.manager_id.user_id.id
        return {'value': result}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
