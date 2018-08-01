# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MgmtsystemHazardTest(models.Model):

    _name = "mgmtsystem.hazard.test"
    _description = "Implementation Tests of hazard"

    name = fields.Char('Test', required=True, translate=True)
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
    )
    review_date = fields.Date('Review Date', required=True)
    executed = fields.Boolean('Executed')
    hazard_id = fields.Many2one(
        'mgmtsystem.hazard',
        'Hazard',
        ondelete='cascade',
        required=False,
        index=True,
    )
