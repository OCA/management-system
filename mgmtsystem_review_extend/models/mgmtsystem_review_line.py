# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MgmtsystemReviewLine(models.Model):
    _name = "mgmtsystem.review.line"
    _inherit = ['mgmtsystem.review.line']

    origin_ids = fields.Many2many(
        'mgmtsystem.nonconformity.origin',
        'mgmtsystem_review_nonconformity_origin_rel',
        'review_line_id',
        'origin_id',
        'Origin',
    )
    
    @api.onchange('nonconformity_id')
    def compute_nonconformity(self):
        
        if self.nonconformity_id :
            self.origin_ids = self.nonconformity_id.origin_ids
            self.name = self.nonconformity_id.name
            self.decision = self.nonconformity_id.description
            
    @api.onchange('action_id')
    def compute_action(self):

        if self.action_id :        
            self.name = self.action_id.name
            self.decision = self.action_id.description  