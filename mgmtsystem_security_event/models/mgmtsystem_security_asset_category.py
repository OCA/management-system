# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CategoryAsset(models.Model):
    _name = "mgmtsystem.security.asset.category"
    _description = "Asset Categories"

    name = fields.Char(required=True)
