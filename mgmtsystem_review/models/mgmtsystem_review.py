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

from openerp import api, fields, models


class MgmtsystemReview(models.Model):
    _name = "mgmtsystem.review"
    _description = "Review"

    name = fields.Char('Name', size=50, required=True)
    reference = fields.Char(
        'Reference',
        size=64,
        required=True,
        readonly=True,
        default='NEW')
    date = fields.Datetime(
        'Date',
        required=True)
    user_ids = fields.Many2many(
        'res.users',
        'mgmtsystem_review_user_rel',
        'user_id',
        'mgmtsystem_review_id',
        'Participants')
    response_ids = fields.Many2many(
        'survey.user_input',
        'mgmtsystem_review_response_rel',
        'response_id',
        'mgmtsystem_review_id',
        'Survey Answers')
    policy = fields.Text('Policy')
    changes = fields.Text('Changes')
    line_ids = fields.One2many(
        'mgmtsystem.review.line',
        'review_id',
        'Lines')
    conclusion = fields.Text('Conclusion')
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('done', 'Closed'),
        ],
        'State',
        readonly=True,
        default="open",
        track_visibility='onchange')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        vals.update({
            'reference': self.env['ir.sequence'].get('mgmtsystem.review')
        })
        return super(MgmtsystemReview, self).create(vals)

    @api.multi
    def button_close(self):
        return self.write({'state': 'done'})


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
