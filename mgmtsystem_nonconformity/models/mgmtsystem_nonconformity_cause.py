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

from openerp import models, fields, api
from openerp.osv import osv


class mgmtsystem_nonconformity_cause(models.Model):
    """
    Cause of the nonconformity of the management system
    """
    _name = "mgmtsystem.nonconformity.cause"
    _description = "Cause of the nonconformity of the management system"
    _order = 'parent_id, sequence'

    name = fields.Char('Cause', required=True, translate=True)
    description = fields.Text('Description')
    sequence = fields.Integer(
        'Sequence',
        help="Defines the order to present items",
    )

    _parent_store = True
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)

    parent_id = fields.Many2one('mgmtsystem.nonconformity.cause', 'Group')
    child_ids = fields.One2many(
        'mgmtsystem.nonconformity.cause',
        'parent_id',
        'Child Causes',
    )
    ref_code = fields.Char('Reference Code')

    @api.multi
    def name_get(self):
        res = []
        for obj in self:
            name = obj.name
            if obj.parent_id:
                name = obj.parent_id.name + ' / ' + name
            res.append((obj.id, name))
        return res

    _constraints = [
        (
            osv.osv._check_recursion,
            "Error! Cannot create recursive cycle.",
            ['parent_id']
        )
    ]
