# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemNonconformityCause(models.Model):

    """Cause of the nonconformity of the management system."""

    _name = "mgmtsystem.nonconformity.cause"
    _description = "Cause of the nonconformity of the management system"
    _order = "parent_id, sequence"
    _parent_store = True

    name = fields.Char("Cause", required=True, translate=True)
    description = fields.Text()
    sequence = fields.Integer(help="Defines the order to present items")
    parent_path = fields.Char(index=True, unaccent=False)
    parent_id = fields.Many2one(
        "mgmtsystem.nonconformity.cause", "Group", ondelete="restrict"
    )
    child_ids = fields.One2many(
        "mgmtsystem.nonconformity.cause", "parent_id", "Child Causes"
    )
    ref_code = fields.Char("Reference Code")
    display_name = fields.Char(compute="_compute_display_name", recursive=True)

    @api.depends("name", "parent_id.display_name")
    def _compute_display_name(self):
        for obj in self:
            if obj.parent_id:
                obj.display_name = f"{obj.parent_id.display_name} / {obj.name}"
            else:
                obj.display_name = obj.name
