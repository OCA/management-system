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

from odoo import fields, models


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    def _compute_complete_name(self):
        for o in self:
            o.complete_name = o.name
            if o.action_type == 'project' and o.project_id:
                o.complete_name = o.project_id.name

    action_type = fields.Selection(
        [
            ('action', 'Action'),
            ('project', 'Project'),
        ], required=True, default='action')
    project_id = fields.Many2one('project.project', 'Project')
    complete_name = fields.Char(compute=_compute_complete_name)
    name = fields.Char('Claim Subject')
