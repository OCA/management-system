# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtSystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    control_ids = fields.Many2many(
        comodel_name="mgmtsystem.security.control",
        relation="mgmtsystem_control_action_rel",
        column1="action_id",
        column2="control_id",
        string="Controls",
    )
