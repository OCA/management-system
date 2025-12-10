# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from .mgmtsystem_security_event import FearedEvents

class MgmtsystemRiskMatrix(models.TransientModel):
    """Category of Assets."""
    _name = "mgmtsystem.risk.matrix"
    _description = "Management System Risk Matrix"

    @api.model
    def _default_system_id(self):
        return self.env['mgmtsystem.system'].search([
            ('company_id', '=', self.env.company.id),
        ], limit=1)

    type = fields.Selection(
        [
            ('original', _('Before applying any control')),
            ('current', _('With current controls')),
            ('residual', _('After applying the planned controls')),
        ],
        string='Type',
        required=True,
        default='current',
    )
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

    def get_event_list(self, severity_id, probability_id):
        self.ensure_one()
        events = self.get_events()
        
        if self.type == 'original':
            return events.filtered(
                lambda e: e.original_probability_id.id == probability_id.id and 
                          e.original_severity_id.id == severity_id.id
            )
        elif self.type == 'current':
            return events.filtered(
                lambda e: e.current_probability_id.id == probability_id.id and 
                          e.current_severity_id.id == severity_id.id
            )
        else:
            return events.filtered(
                lambda e: e.residual_probability_id.id == probability_id.id and 
                          e.residual_severity_id.id == severity_id.id
            )

    def probability_name(self, probability):
        return "%s.%s" % (probability.value, probability.name)

    def severity_name(self, severity):
        return "%s.%s" % (severity.value, severity.name)

    def get_events(self):
        self.ensure_one()
        return self.env['mgmtsystem.security.event'].search([
            ('system_id', '=', self.system_id.id)
        ])

    def get_probabilities(self):
        return self.env['mgmtsystem.hazard.probability'].search(
            [],
            order='value'
        )

    def get_severities(self):
        return self.env['mgmtsystem.hazard.severity'].search(
            [],
            order='value desc'
        )
    def get_cell_color(self, severity, probability):
        level = self.env['mgmtsystem.risk.matrix.level'].search([
            ('severity_min', '<=', severity.value),
            ('severity_max', '>=', severity.value),
            ('probability_min', '<=', probability.value),
            ('probability_max', '>=', probability.value),
        ], limit=1)

        if not level:
            return '#B6D7A8'

        return {
            'green': '#B6D7A8',
            'orange': '#F9CB9C',
            'red': '#EA9999',
        }.get(level.color, '#B6D7A8')

    def print_report(self):
        return self.env.ref('mgmtsystem_security_event.risk_matrix_webkit').report_action(self)
