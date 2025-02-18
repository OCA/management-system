# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class MgmtsytemEvaluationTemplate(models.Model):
    _name = "mgmtsystem.evaluation.template"
    _description = "Evaluation Template"

    name = fields.Char(required=True)
    model_id = fields.Many2one(
        "ir.model",
        domain=[("is_mgmtsystem_evaluation", "=", True)],
        required=True,
        ondelete="cascade",
    )
    active = fields.Boolean(default=True)
    model = fields.Char(
        store=True, related="model_id.model", string="Model technical name"
    )
    result_ids = fields.Many2many("mgmtsystem.evaluation.result")
    feedback = fields.Html()
    user_activity_type_id = fields.Many2one(
        "mail.activity.type",
        string="Activity for user",
        domain=lambda self: [
            "|",
            ("res_model_id", "=", False),
            (
                "res_model_id",
                "=",
                self.env["ir.model"]._get("mgmtsystem.evaluation").id,
            ),
        ],
        ondelete="set null",
        help="""Automatically schedule this activity to the user
        (if exists) once the evaluation is started""",
    )
    manager_activity_type_id = fields.Many2one(
        "mail.activity.type",
        string="Activity for manager",
        domain=lambda self: [
            "|",
            ("res_model_id", "=", False),
            (
                "res_model_id",
                "=",
                self.env["ir.model"]._get("mgmtsystem.evaluation").id,
            ),
        ],
        ondelete="set null",
        help="""Automatically schedule this activity to the Manager
        once the evaluation is started""",
    )
    note = fields.Html()
    group_id = fields.Many2one("res.groups")
    recurrence_type = fields.Selection(
        lambda self: [
            (key, value[0]) for key, value in self._get_recurrence_type().items()
        ]
    )
    recurrence_period = fields.Integer()

    @api.model
    def _get_recurrence_type(self):
        return {
            "daily": ("Daily", lambda r: relativedelta(days=r)),
            "weekly": ("Weekly", lambda r: relativedelta(weeks=r)),
            "monthly": ("Monthly", lambda r: relativedelta(months=r)),
            "quarterly": ("Quarterly", lambda r: relativedelta(months=3 * r)),
            "semesterly": ("Semesterly", lambda r: relativedelta(months=6 * r)),
            "yearly": ("Yearly", lambda r: relativedelta(years=r)),
        }
