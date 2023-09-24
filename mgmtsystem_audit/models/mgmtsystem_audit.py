# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models


class MgmtsystemAudit(models.Model):
    """Model class that manage audit."""

    _name = "mgmtsystem.audit"
    _description = "Audit"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    reference = fields.Char(size=64, required=True, readonly=True, default="NEW")
    date = fields.Datetime()
    line_ids = fields.One2many(
        "mgmtsystem.verification.line", "audit_id", "Verification List"
    )
    number_of_audits = fields.Integer("# of audits", readonly=True, default=1)
    number_of_nonconformities = fields.Integer(
        store=True,
        compute="_compute_number_of_nonconformities",
    )
    number_of_questions_in_verification_list = fields.Integer(
        store=True,
        compute="_compute_number_of_questions_in_verification_list",
    )
    number_of_improvements_opportunity = fields.Integer(
        "Number of improvements Opportunities",
        store=True,
        compute="_compute_number_of_improvement_opportunities",
    )
    days_since_last_update = fields.Integer(
        store=True,
        compute="_compute_days_since_last_update",
    )
    closing_date = fields.Datetime(readonly=True)

    number_of_days_to_close = fields.Integer(
        "# of days to close",
        store=True,
        compute="_compute_number_of_days_to_close",
    )

    user_id = fields.Many2one("res.users", "Audit Manager")
    auditor_user_ids = fields.Many2many(
        "res.users",
        "mgmtsystem_auditor_user_rel",
        "user_id",
        "mgmtsystem_audit_id",
        "Auditors",
    )
    auditee_user_ids = fields.Many2many(
        "res.users",
        "mgmtsystem_auditee_user_rel",
        "user_id",
        "mgmtsystem_audit_id",
        "Auditees",
    )
    strong_points = fields.Html()
    to_improve_points = fields.Html("Points To Improve")
    imp_opp_ids = fields.Many2many(
        "mgmtsystem.action",
        "mgmtsystem_audit_imp_opp_rel",
        "mgmtsystem_action_id",
        "mgmtsystem_audit_id",
        "Improvement Opportunities",
    )

    nonconformity_ids = fields.Many2many(
        "mgmtsystem.nonconformity", string="Nonconformities"
    )
    state = fields.Selection(
        [("open", "Open"), ("done", "Closed")], default="open", required=True
    )
    system_id = fields.Many2one("mgmtsystem.system", "System")
    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )

    @api.depends("nonconformity_ids")
    def _compute_number_of_nonconformities(self):
        """Count number of nonconformities."""
        for audit in self:
            audit.number_of_nonconformities = len(audit.nonconformity_ids)

    @api.depends("imp_opp_ids")
    def _compute_number_of_improvement_opportunities(self):
        """Count number of improvements Opportunities."""
        for audit in self:
            audit.number_of_improvements_opportunity = len(audit.imp_opp_ids)

    @api.depends("line_ids")
    def _compute_number_of_questions_in_verification_list(self):
        for audit in self:
            audit.number_of_questions_in_verification_list = len(audit.line_ids)

    @api.depends("write_date")
    def _compute_days_since_last_update(self):
        for audit in self:
            audit.days_since_last_update = audit._elapsed_days(
                audit.create_date, audit.write_date
            )

    @api.depends("closing_date")
    def _compute_number_of_days_to_close(self):
        for audit in self:
            audit.number_of_days_to_close = audit._elapsed_days(
                audit.create_date, audit.closing_date
            )

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.model_create_multi
    def create(self, vals):
        """Audit creation."""
        for value in vals:
            value.update(
                {"reference": self.env["ir.sequence"].next_by_code("mgmtsystem.audit")}
            )
        audit_id = super(MgmtsystemAudit, self).create(vals)
        return audit_id

    def button_close(self):
        """When Audit is closed, post a message to followers' chatter."""
        self.message_post(body=_("Audit closed"))
        return self.write({"state": "done", "closing_date": fields.Datetime.now()})

    def get_action_url(self):
        """
        Return a short link to the audit form view
        eg. http://localhost:8069/?db=prod#id=1&model=mgmtsystem.audit
        """

        base_url = self.env["ir.config_parameter"].get_param(
            "web.base.url", default="http://localhost:8069"
        )
        url = ("{}/web#db={}&id={}&model={}").format(
            base_url, self.env.cr.dbname, self.id, self._name
        )
        return url

    def get_lines_by_procedure(self):
        p = []
        for line in self.line_ids:
            if line.procedure_id.id:
                procedure_name = line.procedure_id.name
            else:
                procedure_name = _("Undefined")

            p.append(
                {
                    "id": line.id,
                    "procedure": procedure_name,
                    "name": line.name,
                    "yes_no": "Yes / No",
                }
            )
        p = sorted(p, key=lambda k: k["procedure"])
        proc_line = False
        q = []
        proc_name = ""
        for i in range(len(p)):
            if proc_name != p[i]["procedure"]:
                proc_line = True
            if proc_line:
                q.append(
                    {
                        "id": p[i]["id"],
                        "procedure": p[i]["procedure"],
                        "name": "",
                        "yes_no": "",
                    }
                )
                proc_line = False
                proc_name = p[i]["procedure"]
            q.append(
                {
                    "id": p[i]["id"],
                    "procedure": "",
                    "name": p[i]["name"],
                    "yes_no": "Yes / No",
                }
            )
        return q
