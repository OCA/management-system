# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrModel(models.Model):
    _inherit = "ir.model"

    is_mgmtsystem_evaluation = fields.Boolean(
        string="Management System Evaluation",
        default=False,
        help="Whether this model supports evaluations.",
    )

    def _reflect_model_params(self, model):
        vals = super()._reflect_model_params(model)
        vals["is_mgmtsystem_evaluation"] = (
            issubclass(type(model), self.pool["mgmtsystem.evaluation.abstract"])
            and not model._abstract
        )
        return vals
