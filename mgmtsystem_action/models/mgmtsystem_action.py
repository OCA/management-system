# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import _, api, exceptions, fields, models


class MgmtsystemAction(models.Model):
    _name = "mgmtsystem.action"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Action"
    _order = "priority desc, sequence, id desc"

    name = fields.Char("Subject", required=True)
    system_id = fields.Many2one("mgmtsystem.system", "System")
    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )
    active = fields.Boolean("Active", default=True)
    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal")], default="0", index=True, string="Priority"
    )
    sequence = fields.Integer(
        "Sequence",
        index=True,
        default=10,
        help="Gives the sequence order when displaying a list of actions.",
    )
    date_deadline = fields.Date("Deadline")
    date_open = fields.Datetime("Opening Date", readonly=True)
    date_closed = fields.Datetime("Closed Date", readonly=True)
    number_of_days_to_open = fields.Integer(
        "# of days to open", compute="_compute_number_of_days_to_open", store=True
    )
    number_of_days_to_close = fields.Integer(
        "# of days to close", compute="_compute_number_of_days_to_close", store=True
    )
    reference = fields.Char(
        "Reference", required=True, readonly=True, default=lambda self: _("New")
    )
    user_id = fields.Many2one(
        "res.users",
        "Responsible",
        default=lambda self: self._default_owner(),
        required=True,
    )
    description = fields.Html("Description")
    type_action = fields.Selection(
        [
            ("immediate", "Immediate Action"),
            ("correction", "Corrective Action"),
            ("prevention", "Preventive Action"),
            ("improvement", "Improvement Opportunity"),
        ],
        "Response Type",
        required=True,
    )
    stage_id = fields.Many2one(
        "mgmtsystem.action.stage",
        "Stage",
        track_visibility="onchange",
        index=True,
        copy=False,
        default=lambda self: self._default_stage(),
        group_expand="_stage_groups",
    )
    tag_ids = fields.Many2many("mgmtsystem.action.tag", string="Tags")

    def _default_owner(self):
        return self.env.user

    def _default_stage(self):
        return self.env["mgmtsystem.action.stage"].search(
            [("is_starting", "=", True)], limit=1
        )

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            res = (dt1_text - dt2_text).days
        return res

    @api.depends("date_open", "create_date")
    def _compute_number_of_days_to_open(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date, action.date_open
            )

    @api.depends("date_closed", "create_date")
    def _compute_number_of_days_to_close(self):
        for action in self:
            action.number_of_days_to_close_open = action._elapsed_days(
                action.create_date, action.date_closed
            )

    @api.model
    def _stage_groups(self, stages=None, domain=None, order=None):
        return self.env["mgmtsystem.action.stage"].search([], order=order)

    @api.model_create_multi
    def create(self, vals_list):
        for one_vals in vals_list:
            if one_vals.get("reference", _("New")) == _("New"):
                Sequence = self.env["ir.sequence"]
                one_vals["reference"] = Sequence.next_by_code("mgmtsystem.action")
        actions = super().create(vals_list)
        actions.send_mail_for_action()
        return actions

    @api.constrains("stage_id")
    def _check_stage_id(self):
        for rec in self:
            # Do not allow to bring back actions to draft
            if rec.date_open and rec.stage_id.is_starting:
                raise exceptions.ValidationError(
                    _("We cannot bring back the action to draft stage")
                )
            # If stage is changed, the action is opened
            if not rec.date_open and not rec.stage_id.is_starting:
                rec.date_open = fields.Datetime.now()
            # If stage is ending, set closed date
            if not rec.date_closed and rec.stage_id.is_ending:
                rec.date_closed = fields.Datetime.now()

    def send_mail_for_action(self, force_send=True):
        template = self.env.ref("mgmtsystem_action.email_template_new_action_reminder")
        for action in self:
            template.send_mail(action.id, force_send=force_send)
        return True

    def get_action_url(self):
        """Return action url to be used in email templates."""
        base_url = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("web.base.url", default="http://localhost:8069")
        )
        url = ("{}/web#db={}&id={}&model={}").format(
            base_url, self.env.cr.dbname, self.id, self._name
        )
        return url

    @api.model
    def process_reminder_queue(self, reminder_days=10):
        """Notify user when we are 10 days close to a deadline."""
        cur_date = datetime.now().date() + timedelta(days=reminder_days)
        stage_close = self.env.ref("mgmtsystem_action.stage_close")
        actions = self.search(
            [("stage_id", "!=", stage_close.id), ("date_deadline", "=", cur_date)]
        )
        if actions:
            template = self.env.ref(
                "mgmtsystem_action.action_email_template_reminder_action"
            )
            for action in actions:
                template.send_mail(action.id)
            return True
        return False

    @api.model
    def _get_stage_open(self):
        return self.env.ref("mgmtsystem_action.stage_open")

    def case_open(self):
        """Opens case."""
        # TODO smk: is this used?
        return self.write({"active": True, "stage_id": self._get_stage_open().id})
