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
from .mgmtsystem_security_event import _default_system_id


class ThreatScenario(orm.Model):

    """Threat Scenario."""

    _name = "mgmtsystem.security.threat.scenario"
    _description = "Threat Scenario"

    _columns = {
        'name': fields.char("Name"),
        'description': fields.text("Description"),
        'underlying_asset_ids': fields.many2many(
            "mgmtsystem.security.assets.underlying",
            "mgmtststem_security_assets_underlying_rel",
            "threat_scenario_id",
            "underlying_asset_id",
            "Underlying Assets"
        ),
        'original_probability_id': fields.many2one(
            "mgmtsystem.probability", "Original Probability",
            help="Probability without any security measures"
        ),
        'original_severity_id': fields.many2one(
            "mgmtsystem.severity", "Original Severity",
            help="Probability without any security measures"
        ),
        'current_probability_id': fields.many2one(
            "mgmtsystem.probability", "Current Probability",
            help="Probability with existing security measures"
        ),
        'current_severity_id': fields.many2one(
            "mgmtsystem.severity", "Current Severity",
            help="Severity with existing security measures"
        ),
        'residual_probability_id': fields.many2one(
            "mgmtsystem.probability", "Residual Probability",
            help="Probability after remediation"
        ),
        'residual_severity_id': fields.many2one(
            "mgmtsystem.severity", "Residual Severity",
            help="Severity after remediation"
        ),
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
    }

    _defaults = {
        'system_id': _default_system_id,
    }
