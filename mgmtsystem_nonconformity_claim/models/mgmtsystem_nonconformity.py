# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemNonconformity(models.Model):
    _name = 'mgmtsystem.nonconformity'
    _inherit = ['mgmtsystem.nonconformity']
         
    def _compute_mgmtsystem_claim_count(self):
        for mgmtsystem_nonconformity in self:
            mgmtsystem_nonconformity.mgmtsystem_claim_count = len(mgmtsystem_nonconformity.mgmtsystem_claim_ids)
    
    mgmtsystem_claim_ids = fields.Many2many('mgmtsystem.claim','mgmtsystem_nonconformity_mgmtsystem_claim_rel','mgmtsystem_nonconformity_id','mgmtsystem_claim_id','Claim Ids')
    mgmtsystem_claim_count = fields.Integer(compute='_compute_mgmtsystem_claim_count', string="Number of claim")
    
class MgmtsystemClaim(models.Model):
    _name = 'mgmtsystem.claim'
    _inherit = ['mgmtsystem.claim']

    def _compute_mgmtsystem_nonconformity_count(self):
        for mgmtsystem_claim in self:
            mgmtsystem_claim.mgmtsystem_nonconforimity_count = len(mgmtsystem_claim.mgmtsystem_nonconformity_ids)
    
    mgmtsystem_nonconformity_ids = fields.Many2many('mgmtsystem.nonconformity','mgmtsystem_nonconformity_mgmtsystem_claim_rel','mgmtsystem_claim_id','mgmtsystem_nonconformity_id','Non Conformity Ids')
    mgmtsystem_nonconformity_count = fields.Integer(compute='_compute_mgmtsystem_nonconformity_count', string="Number of nonconformity")