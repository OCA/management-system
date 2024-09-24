# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemNonconformityOrigin(models.Model):
    _name = "mgmtsystem.nonconformity.origin"
    _description = "Origin of nonconformity of the management system"
    _order = "parent_id, sequence"
    _parent_store = True

    name = fields.Char("Origin", required=True, translate=True)
    description = fields.Text()
    sequence = fields.Integer(help="Defines the order to present items")
    parent_path = fields.Char(index=True, unaccent=False)
    parent_id = fields.Many2one(
        "mgmtsystem.nonconformity.origin", "Group", ondelete="restrict"
    )
    child_ids = fields.One2many(
        "mgmtsystem.nonconformity.origin", "parent_id", "Childs"
    )
    ref_code = fields.Char("Reference Code")

    active = fields.Boolean(default=True)

    @api.depends("name", "parent_id.name")
    def _compute_display_name(self):
        for obj in self:
            name = obj.name
            if obj.parent_id:
                name = f"{obj.parent_id.display_name} / {name}"
            obj.display_name = name
