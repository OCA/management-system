# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemAction(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action']

    create_date = fields.Datetime(readonly=False)