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

from openerp import fields, models


class MgmtsystemReviewLine(models.Model):
    _name = "mgmtsystem.review.line"
    _description = "Review Line"

    name = fields.Char('Title', size=300, required=True)
    type = fields.Selection(
        [
            ('action', 'Action'),
            ('nonconformity', 'Nonconformity'),
        ],
        'Type')
    action_id = fields.Many2one(
        'mgmtsystem.action',
        'Action',
        select=True)
    nonconformity_id = fields.Many2one(
        'mgmtsystem.nonconformity',
        'Nonconformity',
        select=True)
    decision = fields.Text('Decision')
    review_id = fields.Many2one(
        'mgmtsystem.review',
        'Review',
        ondelete='cascade',
        select=True)
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id)
