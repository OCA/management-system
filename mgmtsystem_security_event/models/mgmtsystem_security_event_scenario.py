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


class EventScenarioLines(models.Model):

    """
    Event Scenario Lines.

    The event scenario lines are used inside the event model.
    """

    _name = "mgmtsystem.security.event.scenario"
    _description = "Security Event - Scenario Lines"

    description = fields.Text('Description')
    vector_id = fields.Many2one(
        "mgmtsystem.security.vector",
        string="Vector"
    )
    source_id = fields.Many2one(
        "mgmtsystem.security.threat.source",
        string="Source"
    )
    probability_id = fields.Many2one(
        "mgmtsystem.hazard.probability", string="Probability"
    )
    security_event_id = fields.Many2one(
        "mgmtsystem.security.event", string="Feared Event"
    )
    system_id = fields.Many2one(
        'mgmtsystem.system',
        related='security_event_id.system_id',
        string='System',
        readonly=True,
        store=True,
    )

    @api.depends('vector_id.name', 'source_id.name')
    def _compute_display_name(self):
        for record in self:
            parts = [_("Events"),
                     record.vector_id.name or "",
                     record.source_id.name or ""]
            record.display_name = " - ".join(part for part in parts if part)
