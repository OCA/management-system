# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemReview(models.Model):
    _name = "mgmtsystem.review"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Review"

    name = fields.Char("Name", size=50, required=True)
    reference = fields.Char(
        "Reference", size=64, required=True, readonly=True, default="NEW"
    )
    date = fields.Datetime("Date", required=True)
    user_ids = fields.Many2many(
        "res.users",
        "mgmtsystem_review_user_rel",
        "user_id",
        "mgmtsystem_review_id",
        "Participants",
    )
    response_ids = fields.Many2many(
        "survey.user_input",
        "mgmtsystem_review_response_rel",
        "response_id",
        "mgmtsystem_review_id",
        "Survey Answers",
    )
    policy = fields.Html("Policy")
    changes = fields.Html("Changes")
    line_ids = fields.One2many("mgmtsystem.review.line", "review_id", "Lines")
    conclusion = fields.Html("Conclusion")
    state = fields.Selection(
        [("open", "Open"), ("done", "Closed")],
        "State",
        readonly=True,
        default="open",
        track_visibility="onchange",
    )

    company_id = fields.Many2one(
        "res.company", "Company", default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["reference"] = self.env["ir.sequence"].next_by_code(
                "mgmtsystem.review"
            )
        return super().create(vals_list)

    def button_close(self):
        return self.write({"state": "done"})
