# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from .common import _parse_risk_formula


class MgmtsystemHazardResidualRisk(models.Model):
    _name = "mgmtsystem.hazard.residual_risk"
    _description = "Residual Risks of hazard"

    name = fields.Char("Name", size=50, required=True, translate=True)
    probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability", "Probability", required=True
    )
    severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity", "Severity", required=True
    )
    usage_id = fields.Many2one("mgmtsystem.hazard.usage", "Occupation / Usage")
    acceptability = fields.Boolean("Acceptability")
    justification = fields.Text("Justification")
    hazard_id = fields.Many2one(
        "mgmtsystem.hazard", "Hazard", ondelete="cascade", index=True
    )

    @api.depends("probability_id", "severity_id", "usage_id")
    def _compute_risk(self):
        if self.probability_id and self.severity_id and self.usage_id:
            self.risk = _parse_risk_formula(
                self.env.company.risk_computation_id.name,
                self.probability_id.value,
                self.severity_id.value,
                self.usage_id.value,
            )
        else:
            self.risk = False

    risk = fields.Integer("Risk", compute=_compute_risk)
