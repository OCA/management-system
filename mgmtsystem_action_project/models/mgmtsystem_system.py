# Copyright (C) 2025 Open2bizz BV www.open2bizz.nl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class MgmtsystemSystem(models.Model):
    _inherits = "mgmtsystem.system"

    project_id = fields.Many2one("project.project", string="Project")
