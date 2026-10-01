# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 - Present
#    Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
from .mgmtsystem_security_event import FearedEvents

class Vector(models.Model):
    """Vector."""
    _name = "mgmtsystem.security.vector"
    _description = "Vector"

    name = fields.Char("Name")
    description = fields.Text("Description")
    supporting_asset_ids = fields.Many2many(
        "mgmtsystem.security.asset.supporting",
        "mgmtststem_security_asset_supporting_rel",
        "vector_id",
        "supporting_asset_id",
        string="Supporting Assets"
    )
    original_probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability",
        string="Original Probability",
        help="Probability without any control"
    )
    original_severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity",
        string="Original Severity",
        help="Probability without any control"
    )
    current_probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability",
        string="Current Probability",
        help="Probability with existing controls"
    )
    current_severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity",
        string="Current Severity",
        help="Severity with existing controls"
    )
    residual_probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability",
        string="Residual Probability",
        help="Probability after remediation"
    )
    residual_severity_id = fields.Many2one(
        "mgmtsystem.hazard.severity",
        string="Residual Severity",
        help="Severity after remediation"
    )
    
    @api.model
    def _default_system_id(self):
        return self.env['mgmtsystem.system'].search([
            ('company_id', '=', self.env.company.id),
        ], limit=1)

    system_id = fields.Many2one(
        'mgmtsystem.system',
        'System',
        required=True,
        default=_default_system_id,
    )
    company_id = fields.Many2one(
        'res.company',
        related='system_id.company_id',
        string='Company',
        readonly=True,
        store=True,
    )
