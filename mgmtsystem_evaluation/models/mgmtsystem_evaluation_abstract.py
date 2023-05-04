# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemEvaluationAbstract(models.AbstractModel):
    _name = "mgmtsystem.evaluation.abstract"
    _description = "Abstract model to inherit by objects that can be evaluated"

    mgmtsystem_evaluation_ids = fields.One2many(
        "mgmtsystem.evaluation",
        inverse_name="res_id",
        domain=lambda r: [("model", "=", r._name)],
    )
    mgmtsystem_evaluation_count = fields.Integer(
        compute="_compute_mgmtsystem_evaluation_count"
    )

    @api.depends("mgmtsystem_evaluation_ids")
    def _compute_mgmtsystem_evaluation_count(self):
        for record in self:
            record.mgmtsystem_evaluation_count = len(record.mgmtsystem_evaluation_ids)

    def _get_mgmtsystem_evaluation_user(self):
        return self.env["res.user"]
