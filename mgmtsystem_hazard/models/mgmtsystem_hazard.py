# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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


class mgmtsystem_hazard(orm.Model):

    _name = "mgmtsystem.hazard"
    _description = "Hazards of the health and safety management system"

    _columns = {
        'name': fields.char('Name', size=50, required=True, translate=True),
        'type_id': fields.many2one(
            'mgmtsystem.hazard.type',
            'Type',
            required=True,
        ),
        'hazard_id': fields.many2one(
            'mgmtsystem.hazard.hazard',
            'Hazard',
            required=True,
        ),
        'origin_id': fields.many2one(
            'mgmtsystem.hazard.origin',
            'Origin',
            required=True,
        ),
        'department_id': fields.many2one(
            'hr.department',
            'Department',
            required=True,
        ),
        'responsible_user_id': fields.many2one(
            'res.users',
            'Responsible',
            required=True,
        ),
        'analysis_date': fields.date(
            'Date',
            required=True,
        ),
        'probability_id': fields.many2one(
            'mgmtsystem.hazard.probability',
            'Probability',
        ),
        'severity_id': fields.many2one(
            'mgmtsystem.hazard.severity',
            'Severity',
        ),
        'usage_id': fields.many2one(
            'mgmtsystem.hazard.usage',
            'Occupation / Usage',
        ),
        'acceptability': fields.boolean('Acceptability'),
        'justification': fields.text('Justification'),
        'control_measure_ids': fields.one2many(
            'mgmtsystem.hazard.control_measure',
            'hazard_id',
            'Control Measures',
        ),
        'test_ids': fields.one2many(
            'mgmtsystem.hazard.test',
            'hazard_id',
            'Implementation Tests',
        ),
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c:
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id),
    }
