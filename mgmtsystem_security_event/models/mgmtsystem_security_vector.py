# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Vector(models.Model):
    _name = "mgmtsystem.security.vector"
    _description = "Vector"

    name = fields.Char(required=True)
    description = fields.Text()
    supporting_asset_ids = fields.Many2many(
        "mgmtsystem.security.asset.supporting",
        "mgmtsystem_security_asset_supporting_rel",
        "vector_id",
        "supporting_asset_id",
    )
    original_probability_id = fields.Many2one(
        "mgmtsystem.risk.probability",
        help="Probability without any control",
    )
    original_severity_id = fields.Many2one(
        "mgmtsystem.risk.severity",
        help="Severity without any control",
    )
    current_probability_id = fields.Many2one(
        "mgmtsystem.risk.probability",
        help="Probability with existing controls",
    )
    current_severity_id = fields.Many2one(
        "mgmtsystem.risk.severity",
        help="Severity with existing controls",
    )
    residual_probability_id = fields.Many2one(
        "mgmtsystem.risk.probability",
        help="Probability after remediation",
    )
    residual_severity_id = fields.Many2one(
        "mgmtsystem.risk.severity",
        help="Severity after remediation",
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
