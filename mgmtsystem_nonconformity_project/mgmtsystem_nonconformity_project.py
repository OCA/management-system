# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from osv import fields, osv

class mgmtsystem_action(osv.osv):
    _inherit = "mgmtsystem.action"

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        res = dict()
        for t in self.name_get(cr, uid, ids, context=context):
            res[t[0]] = t[1]
        return res
    
    _columns = {
        'action_type': fields.selection([('a','Action'), ('p','Project')]
            , 'Action Type', required=True),
        'project_id': fields.many2one('project.project', 'Project'),
        'complete_name': fields.function(_complete_name, string='Complete Name', type='char', size=250),
        #modified
        'name': fields.char('Claim Subject', size=128, required=False),
}
    
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return list()
        res = list()
        project_model = self.pool.get('project.project')
        for o in self.browse(cr, uid, ids, context=context):
            r = (o.id, o.name)
            if o.action_type == 'p' and o.project_id:
                r = (o.id, o.project_id.name)
            res.append(r)
        return res
    
    def _init_install(self, cr, uid):
        """Initialize current data in inherited modules."""
        cr.execute("update mgmtsystem_action set action_type='a' where action_type is null")
        return  True

mgmtsystem_action()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
