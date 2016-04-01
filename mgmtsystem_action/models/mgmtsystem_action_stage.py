# -*- coding: utf-8 -*-

from openerp import models, fields


class MgmtsystemActionStage(models.Model):

    _name = 'mgmtsystem.action.stage'
    _inherit = 'crm.claim.stage'
    _order = 'sequence'

    is_starting = fields.Boolean('Starting stage')
    is_ending = fields.Boolean('Ending stage')
    color = fields.Char(
        string="Color",
        help="Choose your color",
        size=7
    )
