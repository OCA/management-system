# -*- encoding: utf-8 -*-
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

from openerp.osv import fields, orm


def get_events_from_scenario_ids(self, cr, uid, ids, context=None):
    scenario_ids = self.pool['mgmtsystem.security.event.scenario'].search(
        cr, uid, [('scenario_id', 'in', ids)], context=context)

    return self.pool['mgmtsystem.security.event'].search(
        cr, uid, [('scenario_ids', 'in', scenario_ids)], context=context)


def get_events_from_event_scenario_ids(self, cr, uid, ids, context=None):
    return self.pool['mgmtsystem.security.event'].search(
        cr, uid, [('scenario_ids', 'in', ids)], context=context)


def _default_system_id(self, cr, uid, context=None):
    user = self.pool['res.users'].browse(
        cr, uid, uid, context=context)

    company = user.company_id

    system_ids = self.pool['mgmtsystem.system'].search(
        cr, uid, [
            ('company_id', '=', company.id),
            ('type', '=', 'information_security'),
        ],
        limit=1, context=context)

    return system_ids and system_ids[0]


MULTI_FIELDS = {
    'method': True,
    'type': 'many2one',
    'multi': True,
    'store': {
        'mgmtsystem.security.threat.scenario': (
            get_events_from_scenario_ids, [
                'original_probability_id',
                'original_severity_id',
                'current_probability_id',
                'current_severity_id',
                'residual_probability_id',
                'residual_severity_id',
            ], 10),
        'mgmtsystem.security.event.scenario': (
            get_events_from_event_scenario_ids, [
                'scenario_id'
            ], 10),
        'mgmtsystem.security.event': (
            lambda self, cr, uid, ids, c={}: ids, [
                'scenario_ids'
            ], 10),
    }
}


class SecurityEvents(orm.Model):

    """Security Events."""

    _name = "mgmtsystem.security.event"
    _inherits = {'document.page': 'document_page_id'}
    _description = "Security Events"

    def _compute_severity_and_probability(
        self, cr, uid, ids, field_names, args=False, context=None
    ):
        res = {}

        for event in self.browse(cr, uid, ids, context=context):
            fields = [
                'original_probability_id',
                'original_severity_id',
                'current_probability_id',
                'current_severity_id',
                'residual_probability_id',
                'residual_severity_id',
            ]

            event_fields = {
                field: False for field in fields
            }

            scenario_ids = [s.scenario_id for s in event.scenario_ids]

            for field in fields:
                max_value = 0
                for scenario in scenario_ids:

                    record = scenario[field]

                    if record.value > max_value:
                        max_value = record.value
                        event_fields[field] = record.id

            res[event.id] = event_fields

        return res

    _columns = {
        'system_id': fields.many2one(
            'mgmtsystem.system', 'Management System',
            required=True,
        ),
        'company_id': fields.related(
            'system_id',
            'company_id',
            string='Company',
            readonly=True,
            type='many2one',
            relation='res.company',
            store=True,
        ),
        'document_page_id': fields.many2one(
            "document.page", "Description",
            ondelete='cascade', required=True,
        ),
        'severity_id': fields.many2one(
            "mgmtsystem.severity", "Severity",
        ),
        'scenario_ids': fields.one2many(
            "mgmtsystem.security.event.scenario",
            "security_event_id",
            "Scenarios",
        ),
        'measure_ids': fields.one2many(
            "mgmtsystem.security.event.measure",
            "security_event_id",
            "Measures",
        ),
        'confidentiality': fields.boolean('Confidentiality'),
        'integrity': fields.boolean('Integrity'),
        'availability': fields.boolean('Availability'),
        'original_probability_id': fields.function(
            _compute_severity_and_probability,
            string='Original Probability',
            relation='mgmtsystem.probability',
            **MULTI_FIELDS
        ),
        'original_severity_id': fields.function(
            _compute_severity_and_probability,
            string='Original Severity',
            relation='mgmtsystem.severity',
            **MULTI_FIELDS
        ),
        'current_probability_id': fields.function(
            _compute_severity_and_probability,
            string='Current Probability',
            relation='mgmtsystem.probability',
            **MULTI_FIELDS
        ),
        'current_severity_id': fields.function(
            _compute_severity_and_probability,
            string='Current Severity',
            relation='mgmtsystem.severity',
            **MULTI_FIELDS
        ),
        'residual_probability_id': fields.function(
            _compute_severity_and_probability,
            string='Residual Probability',
            relation='mgmtsystem.probability',
            **MULTI_FIELDS
        ),
        'residual_severity_id': fields.function(
            _compute_severity_and_probability,
            string='Residual Severity',
            relation='mgmtsystem.severity',
            **MULTI_FIELDS
        ),
    }

    def _default_parent_id(self, cr, uid, context=None):
        return self.pool['ir.model.data'].get_object_reference(
            cr, uid, 'mgmtsystem_security_event',
            'document_page_group_security_events')[1]

    _defaults = {
        'parent_id': _default_parent_id,
        'system_id': _default_system_id,
    }
