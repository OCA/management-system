# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MgmtsystemReviewEmployee(models.Model):
    _name = "mgmtsystem.review.employee"
    _description = "Review Employee Relation"

    review_id = fields.Many2one('mgmtsystem.review','review')
    employee_id = fields.Many2one('hr.employee','employee')
    presence = fields.Boolean('presence', default=False)