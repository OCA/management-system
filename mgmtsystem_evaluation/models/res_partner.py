# Copyright 2023 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "mgmtsystem.evaluation.abstract"]

    def _get_mgmtsystem_evaluation_user(self):
        return self.user_ids[:1]
