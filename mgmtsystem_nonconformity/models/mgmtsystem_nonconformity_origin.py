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

from openerp import fields, models, api


class MgmtsystemNonconformityOrigin(models.Model):

    _name = "mgmtsystem.nonconformity.origin"
    _description = "Origin of nonconformity of the management system"
    _order = 'parent_id, sequence'
    _parent_store = True

    name = fields.Char('Origin', required=True, translate=True)
    description = fields.Text('Description')
    sequence = fields.Integer(
        'Sequence',
        help="Defines the order to present items",
    )
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    parent_id = fields.Many2one(
        'mgmtsystem.nonconformity.origin',
        'Group',
        ondelete='restrict'
    )
    child_ids = fields.One2many(
        'mgmtsystem.nonconformity.origin',
        'parent_id',
        'Childs',
    )
    ref_code = fields.Char('Reference Code')

    @api.multi
    def name_get(self):
        res = []
        for obj in self:
            name = obj.name
            if obj.parent_id:
                name = obj.parent_id.name_get()[0][1] + ' / ' + name
            res.append((obj.id, name))
        return res
