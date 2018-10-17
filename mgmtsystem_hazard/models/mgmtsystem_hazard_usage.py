# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MgmtsystemHazardUsage(models.Model):

    _name = "mgmtsystem.hazard.usage"
    _description = "Usage of hazard"
    name = fields.Char(
        'Occupation / Usage',
        required=True,
        translate=True,
    )
    value = fields.Integer('Value', required=True)
    description = fields.Text('Description')
