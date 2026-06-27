# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EventScenarioLines(models.Model):
    _name = "mgmtsystem.security.event.scenario"
    _description = "Security Event - Scenario Lines"

    description = fields.Text()
    vector_id = fields.Many2one("mgmtsystem.security.vector")
    source_id = fields.Many2one("mgmtsystem.security.threat.source")
    probability_id = fields.Many2one("mgmtsystem.risk.probability")
    security_event_id = fields.Many2one("mgmtsystem.security.event")
    system_id = fields.Many2one(
        related="security_event_id.system_id",
        readonly=True,
        store=True,
    )

    @api.depends("vector_id.name", "source_id.name")
    def _compute_display_name(self):
        for record in self:
            parts = [
                record.env._("Events"),
                record.vector_id.name or "",
                record.source_id.name or "",
            ]
            record.display_name = " - ".join(part for part in parts if part)
