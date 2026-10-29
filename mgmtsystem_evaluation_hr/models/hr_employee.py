# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = ["hr.employee", "mgmtsystem.evaluation.abstract"]

    def _get_mgmtsystem_evaluation_user(self):
        return self.user_id
