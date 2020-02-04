# -*- coding: utf-8 -*-

from odoo import fields,models

class MgmtsystemAction(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action']

    partner_ids = fields.Many2many('res.partner','mgmtsystem_action_partner_rel','mgmtsystem_action_id','res_partner_id','Partner Ids')