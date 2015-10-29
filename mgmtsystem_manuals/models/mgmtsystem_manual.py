# -*- encoding: utf-8 -*-

from openerp import models, fields


class MgmtsystemManual(models.Model):

    _inherited = 'mgmtsystem.system'
    _description = 'Manual'

    manual = fields.Many2one('document.page', string='Manual')
