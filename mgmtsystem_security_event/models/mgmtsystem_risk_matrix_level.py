# Copyright (C) 2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MgmtsystemRiskMatrixLevel(models.Model):
    _name = "mgmtsystem.risk.matrix.level"
    _description = "Management System Risk Matrix Level"
    _order = "severity_min,probability_min"

    probability_min = fields.Integer(required=True, default=1)
    probability_max = fields.Integer(required=True, default=1)
    severity_min = fields.Integer(required=True, default=1)
    severity_max = fields.Integer(required=True, default=1)
    color = fields.Selection(
        selection=[
            ("green", "Green"),
            ("orange", "Orange"),
            ("red", "Red"),
        ],
        required=True,
        default="green",
        help="The color to display in the matrix",
    )

    @api.constrains(
        "probability_min",
        "probability_max",
        "severity_min",
        "severity_max",
    )
    def _check_overlapping_levels(self):
        for level in self:
            domain = [
                ("id", "!=", level.id),
                ("probability_min", "<=", level.probability_max),
                ("probability_max", ">=", level.probability_min),
                ("severity_min", "<=", level.severity_max),
                ("severity_max", ">=", level.severity_min),
            ]
            if self.search_count(domain):
                raise ValidationError(
                    self.env._("You can not have overlapping risk matrix levels.")
                )
