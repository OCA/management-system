# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MgmtsystemHazard(models.Model):
    """Hazards of the health and safety management system"""""

    _name = "mgmtsystem.hazard"
    _description = __doc__
    _inherit = ['mail.thread']

    name = fields.Char('Name', required=True, translate=True)
    type_id = fields.Many2one(
        'mgmtsystem.hazard.type',
        'Type',
        required=True,
    )
    hazard_id = fields.Many2one(
        'mgmtsystem.hazard.hazard',
        'Hazard',
        required=True,
    )
    origin_id = fields.Many2one(
        'mgmtsystem.hazard.origin',
        'Origin',
        required=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        'Department',
        required=True,
    )
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
    )
    analysis_date = fields.Date(
        'Date',
        required=True,
    )
    probability_id = fields.Many2one(
        'mgmtsystem.hazard.probability',
        'Probability',
    )
    severity_id = fields.Many2one(
        'mgmtsystem.hazard.severity',
        'Severity',
    )
    usage_id = fields.Many2one(
        'mgmtsystem.hazard.usage',
        'Occupation / Usage',
    )
    acceptability = fields.Boolean('Acceptability')
    justification = fields.Text('Justification')
    control_measure_ids = fields.One2many(
        'mgmtsystem.hazard.control_measure',
        'hazard_id',
        'Control Measures',
    )
    test_ids = fields.One2many(
        'mgmtsystem.hazard.test',
        'hazard_id',
        'Implementation Tests',
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda s: s.env.user.company_id,
    )
