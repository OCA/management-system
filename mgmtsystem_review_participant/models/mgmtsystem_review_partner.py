# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MgmtsystemReviewPartner(models.Model):
    _name = "mgmtsystem.review.partner"
    _description = "Review Partner Relation"

    review_id = fields.Many2one('mgmtsystem.review','review')
    partner_id = fields.Many2one('res.partner','partner')
    presence = fields.Boolean('presence', default=False)