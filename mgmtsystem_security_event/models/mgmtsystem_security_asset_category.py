# -*- coding: utf-8 -*-
from odoo import models, fields

class CategoryAsset(models.Model):
    """Category of Assets."""
    _name = "mgmtsystem.security.asset.category"
    _description = "Asset Categories"

    name = fields.Char("Name", required=True)
