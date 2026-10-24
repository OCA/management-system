# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemReviewLine(models.Model):
    _name = "mgmtsystem.review.line"
    _description = "Review Line"

    name = fields.Char("Title", size=300, required=True)
    type = fields.Selection([("action", "Action"), ("nonconformity", "Nonconformity")])
    action_id = fields.Many2one("mgmtsystem.action", index=True)
    nonconformity_id = fields.Many2one("mgmtsystem.nonconformity", index=True)
    decision = fields.Text()
    review_id = fields.Many2one("mgmtsystem.review", ondelete="cascade", index=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
