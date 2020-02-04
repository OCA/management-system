# -*- coding: utf-8 -*-

from odoo import models, fields


class MgmtsystemReviewType(models.Model):
    _name = "mgmtsystem.review.type"
    _description = "Review Type"

    name = fields.Char("Type", required=True, translate=True)
    sequence = fields.Integer('Sequence')
    description = fields.Text('Description', translate=True)
    active = fields.Boolean('Active?', default=True)