# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemEvaluation(models.Model):
    _name = "mgmtsystem.evaluation"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]
    _description = "Evaluation"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    model = fields.Char(
        index=True, compute="_compute_template_fields", store=True, readonly=False
    )
    model_id = fields.Many2one(
        "ir.model", compute="_compute_template_fields", store=True, readonly=False
    )
    res_id = fields.Many2oneReference(index=True, model_field="model")
    user_id = fields.Many2one("res.users", readonly=True, copy=False)
    result_id = fields.Many2one(
        "mgmtsystem.evaluation.result",
        readonly=True,
        states={"progress": [("readonly", False)]},
    )
    result_ids = fields.Many2many(
        related="template_id.result_ids", string="Possible results"
    )
    resource = fields.Reference(
        selection=lambda r: r._get_ref_selection(),
        inverse="_inverse_resource",
        compute="_compute_resource",
        readonly=True,
        states={"draft": [("readonly", False)]},
        required=True,
    )
    template_id = fields.Many2one(
        "mgmtsystem.evaluation.template",
        required=True,
        ondelete="cascade",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("progress", "In progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        tracking=True,
        default="draft",
        required=True,
    )
    date = fields.Date(string="Evaluation date", readonly=True)
    manager_ids = fields.Many2many(
        "res.users",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    active = fields.Boolean(default=True)
    feedback = fields.Html(
        readonly=False,
        states={"done": [("readonly", True)]},
        compute="_compute_template_fields",
        store=True,
    )
    note = fields.Html(
        readonly=False,
        states={"done": [("readonly", True)]},
        compute="_compute_template_fields",
        store=True,
    )
    passed = fields.Boolean(readonly=True)
    is_user = fields.Boolean(compute="_compute_filter_views")
    is_manager = fields.Boolean(compute="_compute_filter_views")
    next_evaluation_date = fields.Date(readonly=True)
    next_evaluation_generated = fields.Boolean(readonly=True)

    @api.depends_context("uid")
    @api.depends("user_id", "manager_ids")
    def _compute_filter_views(self):
        for record in self:
            record.is_user = record._get_is_user()
            record.is_manager = record._get_is_manager()

    def _get_is_manager(self):
        return self.env.user in self.manager_ids or (
            self.template_id.group_id
            and self.env.user in self.template_id.group_id.users
        )

    def _get_is_user(self):
        return self.env.user == self.user_id

    @api.model
    def _get_ref_selection(self):
        models = self.env["ir.model"].sudo().search([])
        return [(model.model, model.name) for model in models]

    @api.depends("template_id", "res_id", "model")
    def _compute_resource(self):
        for record in self:
            if record.model:
                record.resource = "{},{}".format(record.model, record.res_id)
            else:
                record.resource = False

    def _inverse_resource(self):
        for record in self:
            record.res_id = record.resource

    @api.depends("template_id")
    def _compute_template_fields(self):
        for record in self:
            if record.template_id and (
                not record.model or record.template_id.model != record.model
            ):
                record.res_id = False
                record.model = record.template_id.model
                record.model_id = record.template_id.model_id
            if not record.feedback:
                record.feedback = record.template_id.feedback
            if not record.note:
                record.note = record.template_id.note

    @api.depends("template_id")
    def _compute_name(self):
        for record in self:
            record.name = record.template_id.name

    def draft2progress(self):
        self.ensure_one()
        self.write(self._draft2progress_vals())
        if self.template_id.user_activity_type_id and self.user_id:
            self.activity_schedule(
                activity_type_id=self.template_id.user_activity_type_id.id,
                user_id=self.user_id.id,
            )
        if self.template_id.manager_activity_type_id:
            for manager in self.manager_ids:
                self.activity_schedule(
                    activity_type_id=self.template_id.manager_activity_type_id.id,
                    user_id=manager.id,
                )

    def _draft2progress_vals(self):
        return {
            "state": "progress",
            "user_id": self.resource._get_mgmtsystem_evaluation_user().id,
        }

    def progress2done(self):
        for record in self:
            record.write(record._progress2done_vals())

    def _progress2done_vals(self):
        next_date = False
        if self.template_id.recurrence_type and self.template_id.recurrence_period:
            next_date = fields.Date.today() + self.template_id._get_recurrence_type()[
                self.template_id.recurrence_type
            ][1](self.template_id.recurrence_period)
        return {
            "state": "done",
            "date": fields.Date.today(),
            "passed": self.result_id.passed,
            "next_evaluation_date": next_date,
            "next_evaluation_generated": not next_date,
        }

    def cancel(self):
        self.write(self._cancel_vals())

    def _cancel_vals(self):
        return {"state": "cancel", "next_evaluation_date": False}

    def back_to_draft(self):
        self.write(self._back_to_draft_vals())

    def _back_to_draft_vals(self):
        return {"state": "draft", "next_evaluation_date": False, "user_id": False}

    def _generate_new_evaluation(self):
        if not self.template_id.active:
            return
        resource = self.resource
        if "active" in resource._fields and not resource.active:
            return
        return self.create(self._generate_new_evaluation_vals())

    def _generate_new_evaluation_vals(self):
        return {
            "model": self.model,
            "res_id": self.res_id,
            "template_id": self.template_id.id,
            "user_id": self.user_id.id,
            "manager_ids": [(6, 0, self.manager_ids.ids)],
            "feedback": self.template_id.feedback,
            "note": self.template_id.note,
        }

    def _cron_new_evaluation(self):
        for evaluation in self.search(
            [
                ("next_evaluation_date", "<=", fields.Date.today()),
                ("next_evaluation_generated", "=", False),
                ("state", "=", "done"),
            ]
        ):
            evaluation._generate_new_evaluation()
            evaluation.next_evaluation_generated = True
