# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemEvaluationResult(models.Model):
    _name = "mgmtsystem.evaluation.result"
    _description = "Evaluation Result"

    name = fields.Char()
    template_ids = fields.Many2many("mgmtsystem.evaluation.template")
    sequence = fields.Integer()
    active = fields.Boolean(default=True)
    passed = fields.Boolean()
