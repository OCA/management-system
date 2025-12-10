# -*- coding: utf-8 -*-
from odoo import models, fields, api
from .mgmtsystem_security_event import FearedEvents

class PrimaryAsset(models.Model):
    """Primary assets."""
    _name = "mgmtsystem.security.asset.primary"
    _description = "Primary Assets"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    responsible_id = fields.Many2one("res.users", string="Responsible")
    
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
