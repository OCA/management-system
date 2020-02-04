# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemNonconformity(models.Model):
    _name = 'mgmtsystem.nonconformity'
    _inherit = ['mgmtsystem.nonconformity']

    create_date = fields.Datetime(readonly=False)