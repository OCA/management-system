# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from .common import _parse_risk_formula


class MgmtsystemHazardResidualRisk(models.Model):
    _name = "mgmtsystem.hazard.residual_risk"
    _description = "Residual Risks of hazard"

    name = fields.Char(required=True, translate=True)
    probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability", "Probability", required=True
    )
    severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity", "Severity", required=True
    )
    usage_id = fields.Many2one("mgmtsystem.hazard.usage", "Occupation / Usage")
    acceptability = fields.Boolean()
    justification = fields.Text()
    hazard_id = fields.Many2one(
        "mgmtsystem.hazard", "Hazard", ondelete="cascade", index=True
    )

    @api.depends("probability_id", "severity_id", "usage_id")
    def _compute_risk(self):
        for record in self:
            if record.probability_id and record.severity_id and record.usage_id:
                record.risk = _parse_risk_formula(
                    record.env.company.risk_computation_id.name,
                    record.probability_id.value,
                    record.severity_id.value,
                    record.usage_id.value,
                )
            else:
                record.risk = False

    risk = fields.Integer(compute=_compute_risk)
