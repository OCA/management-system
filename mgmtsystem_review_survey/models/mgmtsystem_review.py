# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemReview(models.Model):
    _inherit = "mgmtsystem.review"

    response_ids = fields.Many2many(
        "survey.user_input",
        "mgmtsystem_review_response_rel",
        "response_id",
        "mgmtsystem_review_id",
        "Survey Answers",
    )
