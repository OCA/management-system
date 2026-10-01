# -*- coding: utf-8 -*-
from odoo import models, fields, api
from .mgmtsystem_security_event import FearedEvents

class SupportingAsset(models.Model):
    """Supporting Assets."""
    _name = "mgmtsystem.security.asset.supporting"
    _description = "Supporting Assets"

    name = fields.Char("Name", required=True)
    category_id = fields.Many2one(
        "mgmtsystem.security.asset.category",
        string="Category",
    )
    primary_asset_ids = fields.Many2many(
        "mgmtsystem.security.asset.primary",
        "mgmtsystem_security_asset_primary_rel",
        "supporting_asset_id",
        "primary_asset_id",
        string="Primary Assets",
    )
    
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
