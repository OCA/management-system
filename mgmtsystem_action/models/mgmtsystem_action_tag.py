# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemActionTag(models.Model):
    _name = "mgmtsystem.action.tag"
    _description = "Action Tags"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color Index", default=10)

    _name_uniq = models.Constraint(
        "unique(name)",
        "Tag name already exists !",
    )
