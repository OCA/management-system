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

from openerp import fields, models, api


class Nonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    department_id =  fields.Many2one(
            'hr.department',
            'Department')
    superior_user_id = fields.Many2one(
            'res.users',
            'Top Manager')

    @api.onchange('responsible_user_id')
    def onchange_department_id(new_id):
        if new_id:
            deptm = self.env['hr.department'].browse(new_id)
            if deptm.manager_id.user_id:
                self.manager_user_id = deptm.manager_id.user_id
            parent_deptm = deptm.parent_id
            if parent_deptm.manager_id.user_id:
                superior_user_id = parent_deptm.manager_id.user_id

    @api.multi
    def message_auto_subscribe(updated_fields, values=None):
        """Add the Top Manager to OpenChatter follow list."""
        for nc in self:
            nc.message_subscribe_users(
                user_ids=[o.superior_user_id.id], subtype_ids=None)
        return super(Nonconformity, self).message_auto_subscribe(
            updated_fields=updated_fields, values=values)
