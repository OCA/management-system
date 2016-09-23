# -*- coding: utf-8 -*-

from openerp import fields, models, _


class MgmtSystemSeverity(models.Model):

    """
    Define the Severity for management system.

    Allow you to manage scale of severity used across
    different modules (health and safety, information security).
    """

    _name = "mgmtsystem.severity"
    _description = "Management System Severity"

    name = fields.Char("Name", required=True, translate=True)

    description = fields.Text("Description")

    value = fields.Integer("Value", required=True)

    category = fields.Selection((
        ("hazard", _("hazard")),
        ("security", _("security")),
    ), 'Category', required=True)
