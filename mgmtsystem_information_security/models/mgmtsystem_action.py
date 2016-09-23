# -*- coding: utf-8 -*-

from openerp import fields, models


class mgmtsystem_action(models.Model):

    _inherit = "mgmtsystem.action"

    control_ids = fields.Many2many(
        'mgmtsystem.security.control',
        'mgmtsystem_control_action_rel',
        'action_id',
        'control_id',
        'Controls',
    )
