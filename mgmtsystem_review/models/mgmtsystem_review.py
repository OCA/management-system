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
    conclusion = fields.Html()
    state = fields.Selection(
        [("open", "Open"), ("done", "Closed")],
        default="open",
        tracking=True,
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
