# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MgmtsystemEvent(models.Model):
    _name = "mgmtsystem.event"
    _description = "Event"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    @api.model
    def _stage_groups(self, stages, domain):
        stage_ids = self.env["mgmtsystem.event.stage"].search([])
        return stage_ids

    # 1. Description
    name = fields.Char(required=True, tracking=True)
    ref = fields.Char("Reference", required=True, default="NEW")
    # Compute data
    number_of_events = fields.Integer("# of events", default=1)
    opened_date = fields.Datetime("Date Opened", readonly=True, tracking=True)
    deadline_date = fields.Datetime(
        "Deadline", help="Deadline to handle and close event", tracking=True
    )
    closed_date = fields.Datetime("Date Closed", readonly=True, tracking=True)
    days_since_updated = fields.Integer(
        compute="_compute_days_since_updated", store=True
    )
    number_of_days_to_open = fields.Integer(
        "# of days to open", compute="_compute_number_of_days_to_open", store=True
    )
    number_of_days_to_close = fields.Integer(
        "# of days to close",
        compute="_compute_number_of_days_to_close",
        store=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        "Partner",
        required=True,
        default=lambda self: self.env.company,
        tracking=True,
    )
    reference = fields.Char(
        "Related to", default=lambda self: self._default_reference(), tracking=True
    )
    event_type = fields.Selection(
        [
            ("improvement", "Improvement"),
            ("prevention", "Preventive"),
            ("correction", "Corrective"),
            ("immediate", "Immediate"),
        ],
        "Type",
        required=True,
        default="improvement",
        tracking=True,
    )
    responsible_user_id = fields.Many2one("res.users", "Responsible", tracking=True)
    manager_user_id = fields.Many2one("res.users", "Manager", tracking=True)
    user_id = fields.Many2one(
        "res.users",
        "Filled in by",
        required=True,
        default=lambda self: self.env.user,
        tracking=True,
    )
    origin_ids = fields.Many2many(
        "mgmtsystem.event.origin",
        "mgmtsystem_event_origin_rel",
        "event_id",
        "origin_id",
        "Origin",
        tracking=True,
    )
    procedure_ids = fields.Many2many(
        "document.page",
        "mgmtsystem_event_procedure_rel",
        "event_id",
        "procedure_id",
        "Procedure",
    )
    description = fields.Text(required=True)
    system_id = fields.Many2one("mgmtsystem.system", "System")
    stage_id = fields.Many2one(
        "mgmtsystem.event.stage",
        "Stage",
        tracking=True,
        copy=False,
        default=lambda self: self._default_stage(),
        group_expand="_stage_groups",
    )
    state = fields.Selection(related="stage_id.state", store=True)
    kanban_state = fields.Selection(
        [
            ("normal", "In Progress"),
            ("done", "Ready for next stage"),
            ("blocked", "Blocked"),
        ],
        default="normal",
        tracking=True,
        help="A kanban state indicates special situations affecting it:\n"
        " * Normal is the default situation\n"
        " * Blocked indicates something is preventing"
        " the progress of this task\n"
        " * Ready for next stage indicates the"
        " task is ready to be pulled to the next stage",
        required=True,
        copy=False,
    )

    # 2. Root Cause Analysis
    cause_ids = fields.Many2many(
        "mgmtsystem.event.cause",
        "mgmtsystem_event_cause_rel",
        "event_id",
        "cause_id",
        "Cause",
    )
    severity_id = fields.Many2one("mgmtsystem.event.severity", "Severity")
    analysis = fields.Text()
    immediate_action_id = fields.Many2one(
        "mgmtsystem.action",
        domain="[('event_ids', '=', id)]",
    )

    # 3. Action Plan
    action_ids = fields.Many2many(
        "mgmtsystem.action",
        "mgmtsystem_event_action_rel",
        "event_id",
        "action_id",
        "Actions",
    )
    action_comments = fields.Text(
        "Action Plan Comments", help="Comments on the action plan."
    )

    # 4. Effectiveness Evaluation
    evaluation_comments = fields.Text(
        help="Conclusions from the last effectiveness evaluation.",
    )

    # Multi-company
    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )
    res_model = fields.Char(index=True)
    res_id = fields.Integer(index=True)
    res_ref = fields.Reference(
        string="Related Record",
        selection="_referenceable_models",
        compute="_compute_res_ref",
    )
    tag_ids = fields.Many2many("mgmtsystem.event.tag", string="Tags")

    @api.model
    def _default_stage(self):
        """Return the default stage."""
        return self.env.ref("mgmtsystem_event.stage_draft", False) or self.env[
            "mgmtsystem.event.stage"
        ].search([("is_starting", "=", True)], limit=1)

    @api.model
    def _referenceable_models(self):
        return [
            (x.model, f"{x.name} ({x.model})")
            for x in self.env["ir.model"]
            .sudo()
            .search(
                [
                    ("model", "!=", "mail.thread"),
                    ("model", "not ilike", "ir."),
                    ("transient", "=", False),
                ],
                order="name",
            )
        ]

    @api.model
    def _default_reference(self):
        if self.env.context.get("mgmtsystem_event") and self.env.context.get("id"):
            return (
                self.env[self.env.context["mgmtsystem_event"]]
                .browse(self.env.context.get("id"))
                .exists()
                .display_name
            )
        return ""

    def _get_all_actions(self):
        self.ensure_one()
        return self.action_ids + self.immediate_action_id

    @api.constrains("stage_id")
    def _check_open_with_action_comments(self):
        for nc in self:
            if nc.state == "open" and not nc.action_comments:
                raise models.ValidationError(
                    self.env._(
                        "Action plan  comments are required "
                        "in order to put a event In Progress."
                    )
                )

    @api.constrains("stage_id")
    def _check_close_with_evaluation(self):
        for nc in self:
            if nc.state == "done":
                if not nc.evaluation_comments:
                    raise models.ValidationError(
                        self.env._(
                            "Evaluation Comments are required "
                            "in order to close a Event."
                        )
                    )
                actions_are_closed = nc._get_all_actions().mapped("stage_id.is_ending")
                if not all(actions_are_closed):
                    raise models.ValidationError(
                        self.env._(
                            "All actions must be done " "before closing a Event."
                        )
                    )

    @api.model
    def _elapsed_days(self, dt1, dt2):
        return (dt2 - dt1).days if dt1 and dt2 else 0

    @api.depends("create_date", "opened_date")
    def _compute_number_of_days_to_open(self):
        for event in self:
            event.number_of_days_to_open = self._elapsed_days(
                event.create_date, event.opened_date
            )

    @api.depends("opened_date", "closed_date")
    def _compute_number_of_days_to_close(self):
        for event in self:
            event.number_of_days_to_close = self._elapsed_days(
                event.opened_date, event.closed_date
            )

    @api.depends("write_date")
    def _compute_days_since_updated(self):
        for nc in self:
            nc.days_since_updated = self._elapsed_days(nc.create_date, nc.write_date)

    @api.depends("res_model", "res_id")
    def _compute_res_ref(self):
        for rec in self:
            if rec.res_model and rec.res_id:
                rec.res_ref = f"{rec.res_model},{rec.res_id}"
            else:
                rec.res_ref = False

    @api.model_create_multi
    def create(self, vals):
        for value in vals:
            value.update(
                {"ref": self.env["ir.sequence"].next_by_code("mgmtsystem.event")}
            )
        return super().create(vals)

    def write(self, vals):
        is_writing = self.env.context.get("is_writing", False)
        is_state_change = "stage_id" in vals or "state" in vals
        # Reset Kanban State on Stage change
        if is_state_change:
            was_not_open = {
                x.id: x.state in ("draft", "analysis", "pending") for x in self
            }
            if any(self.filtered(lambda x: x.kanban_state != "normal")):
                vals["kanban_state"] = "normal"

        result = super().write(vals)

        # Set/reset the closing date
        if not is_writing and is_state_change:
            for nc in self.with_context(is_writing=True):
                # On Close set Closing Date
                if nc.state == "done" and not nc.closed_date:
                    nc.closed_date = fields.Datetime.now()
                # On reopen resete Closing Date
                elif nc.state != "done" and nc.closed_date:
                    nc.closed_date = None
                # On action plan approval, Open the Actions
                if nc.state == "open" and was_not_open[nc.id]:
                    for action in nc._get_all_actions():
                        if action.stage_id.is_starting:
                            action.case_open()

        # Update followers
        if "responsible_user_id" in vals:
            for record in self:
                if record.responsible_user_id and record.responsible_user_id.partner_id:
                    record.message_subscribe(
                        partner_ids=[record.responsible_user_id.partner_id.id]
                    )
        if "manager_user_id" in vals:
            for record in self:
                if record.manager_user_id and record.manager_user_id.partner_id:
                    record.message_subscribe(
                        partner_ids=[record.manager_user_id.partner_id.id]
                    )

        return result
