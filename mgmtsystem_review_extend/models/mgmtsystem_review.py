# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MgmtsystemReview(models.Model):
    _name = "mgmtsystem.review"
    _inherit = ['mgmtsystem.review']
    
    type_id = fields.Many2one(
        'mgmtsystem.review.type',
        'Type')