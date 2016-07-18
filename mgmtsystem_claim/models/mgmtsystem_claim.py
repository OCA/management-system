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


class MgmtsystemClaim(models.Model):
    _name = "mgmtsystem.claim"
    _description = "Claim"
    _inherit = "crm.claim"

    reference = fields.Char(
        'Reference',
        required=True,
        readonly=True,
        default='NEW'
    )

    message_ids = fields.One2many(
        'mail.message',
        'res_id',
        'Messages',
        domain=[('model', '=', _name)]
    )

    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id
    )

    stage_id = fields.Many2one(
        'mgmtsystem.claim.stage',
        'Stage',
        default=lambda self: self.get_default_stage()
    )

    @api.model
    def get_default_stage(self):
        return self.env['mgmtsystem.claim.stage'].search([])[0].id

    @api.model
    def create(self, vals):
        vals.update({
            'reference':
                self.env['ir.sequence'].next_by_code('mgmtsystem.claim')
        })
        return super(MgmtsystemClaim, self).create(vals)
