# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SupportingAsset(models.Model):
    _name = "mgmtsystem.security.asset.supporting"
    _description = "Supporting Assets"

    name = fields.Char(required=True)
    category_id = fields.Many2one("mgmtsystem.security.asset.category")
    primary_asset_ids = fields.Many2many(
        "mgmtsystem.security.asset.primary",
        "mgmtsystem_security_asset_primary_rel",
        "supporting_asset_id",
        "primary_asset_id",
    )

    @api.model
    def _default_system_id(self):
        return self.env["mgmtsystem.system"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )

    system_id = fields.Many2one(
        "mgmtsystem.system",
        required=True,
        default=lambda self: self._default_system_id(),
    )
    company_id = fields.Many2one(
        related="system_id.company_id",
        readonly=True,
        store=True,
    )
