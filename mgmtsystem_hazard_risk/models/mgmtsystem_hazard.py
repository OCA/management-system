# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from .common import _parse_risk_formula


class MgmtsystemHazard(models.Model):
    _inherit = "mgmtsystem.hazard"
    risk_type_id = fields.Many2one(
        "mgmtsystem.hazard.risk.type", "Risk Type", required=True
    )
    risk = fields.Integer(compute="_compute_risk", string="Risk")
    residual_risk_ids = fields.One2many(
        "mgmtsystem.hazard.residual_risk", "hazard_id", "Residual Risk Evaluations"
    )

    @api.depends("probability_id", "severity_id", "usage_id")
    def _compute_risk(self):
        for hazard in self:
            if hazard.probability_id and hazard.severity_id and hazard.usage_id:
                hazard.risk = _parse_risk_formula(
                    self.env.company.risk_computation_id.name,
                    hazard.probability_id.value,
                    hazard.severity_id.value,
                    hazard.usage_id.value,
                )
            else:
                hazard.risk = False
