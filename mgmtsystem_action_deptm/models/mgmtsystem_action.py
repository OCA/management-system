# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemAction(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action']

    department_id = fields.Many2one('hr.department', string='Department')