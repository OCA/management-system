# -*- coding: utf-8 -*-

from openerp import models, fields


class MgmtSystemManual(models.Model):

    _inherit = 'mgmtsystem.system'
    _description = 'Manual'
    manual = fields.Many2one('document.page', string='Manual')
