# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class KpiHistory(models.Model):
    _inherit = "kpi.history"

    review_ids = fields.Many2many(
        "mgmtsystem.review",
        "mgmtsystem_review_kpi_history_rel",
        "kpi_history_id",
        "review_id",
        "Reviews",
    )
