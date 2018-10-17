# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MgmtsystemHazardType(models.Model):

    _name = "mgmtsystem.hazard.type"
    _description = "Type of Hazard"

    name = fields.Char('Type', required=True, translate=True)
    description = fields.Text('Description')
