# -*- encoding: utf-8 -*-
from osv import fields, osv

class mgmtsystem_nonconformity(osv.osv):
    _inherit = "mgmtsystem.nonconformity"
    _columns = {
        'department_id': fields.many2one('hr.department', 'Department', required=True),
    }

    def onchange_department_id(self, cr, uid, ids, new_id, context=None):
        result = {}
        if new_id:
            deptm = self.pool.get('hr.department').browse(cr, uid, new_id, context=context)
            if deptm.manager_id and deptm.manager_id.user_id:
                result['responsible_user_id'] = deptm.manager_id.user_id.id
            if deptm.parent_id and deptm.parent_id.manager_id and deptm.parent_id.manager_id.user_id:
                result['manager_user_id'] = deptm.parent_id.manager_id.user_id.id
        return {'value': result}

mgmtsystem_nonconformity()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
