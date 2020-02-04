# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemAction(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action']
         
    def _compute_purchase_order_count(self):
        for mgmtsystem_action in self:
            mgmtsystem_action.purchase_order_count = len(mgmtsystem_action.purchase_order_ids)

    purchase_order_ids = fields.Many2many('purchase.order','mgmtsystem_action_purchase_order_rel','mgmtsystem_action_id','purchase_order_id','Purchase Order Ids')
    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count', string="Number of purchase order")
    
class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order']

    def _compute_mgmtsystem_action_count(self):
        for purchase_order in self:
            purchase_order.mgmtsystem_action_count = len(purchase_order.mgmtsystem_action_ids)
    
    mgmtsystem_action_ids = fields.Many2many('mgmtsystem.action','mgmtsystem_action_purchase_order_rel','purchase_order_id','mgmtsystem_action_id','Action Ids')
    mgmtsystem_action_count = fields.Integer(compute='_compute_mgmtsystem_action_count', string="Number of action")