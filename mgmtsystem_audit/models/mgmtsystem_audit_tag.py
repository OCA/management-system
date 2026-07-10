# Copyright (C) 2026 Miquel Rosell
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import random

from odoo import fields, models


class MgmtsystemAuditTag(models.Model):
    _name = "mgmtsystem.audit.tag"
    _description = "Audit tag"

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(
        string="Color index",
        default=lambda self: random.randint(1, 11),
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists!"),
    ]
