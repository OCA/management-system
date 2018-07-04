# -*- coding: utf-8 -*-
# Copyright 2012 Savoir-faire Linux <http://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


def own_company(self):
    return self.env.user.company_id.id


class MgmtSystemSystem(models.Model):

    _name = 'mgmtsystem.system'
    _description = _('System')

    name = fields.Char('System', required=True)
    company_id = fields.Many2one('res.company', 'Company',
                                 default=own_company)
