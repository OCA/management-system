# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from .mgmtsystem_security_event import FearedEvents

class ThreatSource(models.Model):
    """Threat Source."""
    _name = "mgmtsystem.security.threat.source"
    _description = "Threat Source"

    name = fields.Char("Name")
    
    @api.model
    def _default_system_id(self):
        return self.env['mgmtsystem.system'].search([
            ('company_id', '=', self.env.company.id),
        ], limit=1)

    system_id = fields.Many2one(
        'mgmtsystem.system', 'System',
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
