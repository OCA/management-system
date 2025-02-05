# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class MgmtsystemSystem(models.Model):
    _inherit = "project.task"

    mgmtsystem_action_id = fields.Many2one("mgmtsystem.action", string="Management System Action")
