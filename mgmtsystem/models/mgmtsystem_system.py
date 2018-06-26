# -*- coding: utf-8 -*-
# Copyright 2012 Savoir-faire Linux <http://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtSystemSystem(models.Model):
    _name = 'mgmtsystem.system'
    _description = 'Management system'
    _inherit = "mail.thread"

    name = fields.Char(
        'System',
        required=True,
        translate=True,
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self._default_company_id(),
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id
