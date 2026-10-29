# -*- coding: utf-8 -*-
from odoo import models, fields, api

class FearedEvents(models.Model):
    _name = "mgmtsystem.security.event"
    _inherits = {'document.page': 'document_page_id'}
    _description = "Feared Events"

    document_page_id = fields.Many2one('document.page', required=True, ondelete='cascade')
    
    system_id = fields.Many2one(
        'mgmtsystem.system',
        string='System',
        required=True,
        default=lambda self: self._default_system_id()
    )
    company_id = fields.Many2one(
        'res.company',
        related='system_id.company_id',
        string='Company',
        readonly=True,
        store=True,
    )
    
    severity_id = fields.Many2one("mgmtsystem.hazard.severity", string="Severity")
    
    scenario_ids = fields.One2many(
        "mgmtsystem.security.event.scenario",
        "security_event_id",
        string="Scenarios",
    )
    control_ids = fields.One2many(
        "mgmtsystem.security.event.control",
        "security_event_id",
        string="Controls",
    )
    
    confidentiality = fields.Boolean('Confidentiality')
    integrity = fields.Boolean('Integrity')
    availability = fields.Boolean('Availability')

    # Security ratings (Computed)
    original_probability_id = fields.Many2one('mgmtsystem.hazard.probability', compute='_compute_ratings', store=True, string='Original Probability')
    original_severity_id = fields.Many2one('mgmtsystem.hazard.severity', compute='_compute_ratings', store=True, string='Original Severity')
    current_probability_id = fields.Many2one('mgmtsystem.hazard.probability', compute='_compute_ratings', store=True, string='Current Probability')
    current_severity_id = fields.Many2one('mgmtsystem.hazard.severity', compute='_compute_ratings', store=True, string='Current Severity')
    residual_probability_id = fields.Many2one('mgmtsystem.hazard.probability', compute='_compute_ratings', store=True, string='Residual Probability')
    residual_severity_id = fields.Many2one('mgmtsystem.hazard.severity', compute='_compute_ratings', store=True, string='Residual Severity')

    @api.model
    def _default_system_id(self):
        # Simplified default logic
        return self.env['mgmtsystem.system'].search([
            ('company_id', '=', self.env.company.id),
            # ('type', '=', 'information_security'), # Check if type field exists in 18
        ], limit=1).id

    @api.depends('scenario_ids') # Add deeper dependencies if needed
    def _compute_ratings(self):
        for event in self:
            # Placeholder logic to avoid crash if scenario model is not ready
            # In v7 code it iterated scenarios and picked max values
            # We implemented a safe default for now
            event.original_probability_id = False
            event.original_severity_id = False
            event.current_probability_id = False
            event.current_severity_id = False
            event.residual_probability_id = False
            event.residual_severity_id = False
