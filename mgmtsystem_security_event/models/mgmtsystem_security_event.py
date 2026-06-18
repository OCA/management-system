# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

RATING_FIELDS = [
    "original_probability_id",
    "original_severity_id",
    "current_probability_id",
    "current_severity_id",
    "residual_probability_id",
    "residual_severity_id",
]


class FearedEvents(models.Model):
    _name = "mgmtsystem.security.event"
    _inherits = {"document.page": "document_page_id"}
    _description = "Feared Events"

    document_page_id = fields.Many2one(
        "document.page", required=True, ondelete="cascade"
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
    severity_id = fields.Many2one("mgmtsystem.hazard.severity")
    scenario_ids = fields.One2many(
        "mgmtsystem.security.event.scenario",
        "security_event_id",
    )
    control_ids = fields.One2many(
        "mgmtsystem.security.event.control",
        "security_event_id",
    )
    confidentiality = fields.Boolean()
    integrity = fields.Boolean()
    availability = fields.Boolean()
    original_probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability",
        compute="_compute_ratings",
        store=True,
    )
    original_severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity",
        compute="_compute_ratings",
        store=True,
    )
    current_probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability",
        compute="_compute_ratings",
        store=True,
    )
    current_severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity",
        compute="_compute_ratings",
        store=True,
    )
    residual_probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability",
        compute="_compute_ratings",
        store=True,
    )
    residual_severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity",
        compute="_compute_ratings",
        store=True,
    )

    @api.model
    def _default_system_id(self):
        return self.env["mgmtsystem.system"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )

    @api.depends(
        "scenario_ids",
        "scenario_ids.vector_id",
        "scenario_ids.vector_id.original_probability_id",
        "scenario_ids.vector_id.original_severity_id",
        "scenario_ids.vector_id.current_probability_id",
        "scenario_ids.vector_id.current_severity_id",
        "scenario_ids.vector_id.residual_probability_id",
        "scenario_ids.vector_id.residual_severity_id",
    )
    def _compute_ratings(self):
        for event in self:
            vectors = event.scenario_ids.mapped("vector_id")
            for field_name in RATING_FIELDS:
                max_value = 0
                selected = self.env[event._fields[field_name].comodel_name]
                for vector in vectors:
                    record = vector[field_name]
                    # Strict > keeps the first vector seen when values tie,
                    # which is deterministic because scenario_ids is ordered by id.
                    if record and record.value > max_value:
                        max_value = record.value
                        selected = record
                event[field_name] = selected
