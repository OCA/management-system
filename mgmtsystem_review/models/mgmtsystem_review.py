# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemReview(models.Model):
    _name = "mgmtsystem.review"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Review"

    name = fields.Char(size=50, required=True)
    reference = fields.Char(size=64, required=True, default="NEW")
    date = fields.Datetime(required=True)
    system_id = fields.Many2one("mgmtsystem.system")
    user_ids = fields.Many2many(
        "res.users",
        "mgmtsystem_review_user_rel",
        "user_id",
        "mgmtsystem_review_id",
        "Participants",
    )
    policy = fields.Html()
    changes = fields.Html()
    line_ids = fields.One2many("mgmtsystem.review.line", "review_id", "Lines")
    kpi_history_ids = fields.Many2many(
        "kpi.history",
        "mgmtsystem_review_kpi_history_rel",
        "review_id",
        "kpi_history_id",
        "KPI History",
    )
    conclusion = fields.Html()
    state = fields.Selection(
        [("open", "Open"), ("done", "Closed")],
        default="open",
        tracking=True,
    )

    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )

    def _default_kpi_history_ids(self):
        kpis = self.env["kpi"].search([("active", "=", True)])
        latest = self.env["kpi.history"]
        for kpi in kpis:
            if kpi.history_ids:
                latest |= kpi.history_ids[0]
        return latest

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["reference"] = self.env["ir.sequence"].next_by_code(
                "mgmtsystem.review"
            )
            if not vals.get("kpi_history_ids"):
                latest = self._default_kpi_history_ids()
                vals["kpi_history_ids"] = [fields.Command.set(latest.ids)]
        return super().create(vals_list)

    def button_update_kpi_history(self):
        for review in self:
            histories = self.env["kpi.history"].search(
                [("date", "<=", review.date)],
                order="kpi_id, date desc",
            )
            latest = self.env["kpi.history"]
            seen = set()
            for h in histories:
                if h.kpi_id.id not in seen:
                    seen.add(h.kpi_id.id)
                    latest |= h
            review.kpi_history_ids = latest

    def button_close(self):
        return self.write({"state": "done"})
