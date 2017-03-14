# -*- coding: utf-8 -*-

from odoo import models, fields


class MgmtsystemActionStage(models.Model):
    """This object is used to defined different stage for actions."""

    _name = 'mgmtsystem.action.stage'
    _description = "Action stages"
    _order = 'sequence'

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Used to order stages. Lower is better.", default=100)
    case_default = fields.Boolean(
        'Common to All Teams', help="If you check this field, \
        this stage will be proposed by default on each sales team. \
        It will not assign this stage to existing teams.")
    is_starting = fields.Boolean('Starting stage')
    is_ending = fields.Boolean('Ending stage')
