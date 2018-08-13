# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MgmtsystemHazardControlMeasure(models.Model):

    _name = "mgmtsystem.hazard.control_measure"
    _description = "Control Measure of hazard"

    name = fields.Char(
        'Control Measure',
        required=True,
        translate=True,
    )
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
    )
    comments = fields.Text('Comments')
    hazard_id = fields.Many2one(
        'mgmtsystem.hazard',
        'Hazard',
        ondelete='cascade',
        required=False,
        index=True,
    )
