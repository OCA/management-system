# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PrimaryAsset(models.Model):
    _name = "mgmtsystem.security.asset.primary"
    _description = "Primary Assets"

    name = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one("res.users")

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
