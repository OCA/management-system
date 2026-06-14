# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventControlLine(models.Model):
    _name = "mgmtsystem.security.event.control"
    _description = "Feared Events - Control Lines"

    control_id = fields.Many2one("mgmtsystem.security.control")
    supporting_asset_id = fields.Many2one("mgmtsystem.security.asset.supporting")
    security_event_id = fields.Many2one("mgmtsystem.security.event")
    prevention = fields.Boolean()
    protection = fields.Boolean()
    recovery = fields.Boolean()
    system_id = fields.Many2one(
        related="security_event_id.system_id",
        readonly=True,
        store=True,
    )

    @api.depends("control_id.name", "supporting_asset_id.name")
    def _compute_display_name(self):
        for record in self:
            parts = [record.env._("Events")]
            if record.control_id.name:
                parts.append(record.control_id.name)
            if record.supporting_asset_id.name:
                parts.append(record.supporting_asset_id.name)
            record.display_name = " - ".join(parts)
