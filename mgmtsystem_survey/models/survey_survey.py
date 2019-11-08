# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Survey(models.Model):
    _inherit = "survey.survey"

    state = fields.Selection(selection_add=[("management_system", "Management System")])
