# -*- coding: utf-8 -*-
# Copyright 2018 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    mgmtsystem_consent_ids = fields.One2many(
        "mgmtsystem.consent",
        "partner_id",
        "Management system consents",
    )
    mgmtsystem_consent_ids_count = fields.Integer(
        "Consents",
        compute="_compute_mgmtsystem_consent_ids_count",
        help="Management system consent requests amount",
    )

    @api.depends("mgmtsystem_consent_ids")
    def _compute_mgmtsystem_consent_ids_count(self):
        """Count consent requests."""
        for one in self:
            one.mgmtsystem_consent_ids_count = len(one.mgmtsystem_consent_ids)
