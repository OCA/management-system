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


def _parse_risk_formula(formula, a, b, c):
    """Calculate the risk replacing the variables A, B, C into the formula."""
    f = formula.replace('A', str(a)).replace('B', str(b)).replace('C', str(c))
    return eval(f)


class mgmtsystem_hazard_type(orm.Model):

    _name = "mgmtsystem.hazard.type"
    _description = "Type of hazard"
    _columns = {
        'name': fields.char('Type', size=50, required=True, translate=True),
        'description': fields.text('Description'),
    }


class mgmtsystem_hazard_risk_computation(orm.Model):

    _name = "mgmtsystem.hazard.risk.computation"
    _description = "Computation Risk"
    _columns = {
        'name': fields.char('Computation Risk', size=50, required=True),
        'description': fields.text('Description'),
    }


class res_company(orm.Model):
    _inherit = "res.company"
    _columns = {
        'risk_computation_id': fields.many2one(
            'mgmtsystem.hazard.risk.computation',
            'Risk Computation',
            required=True,
        ),
    }

    def _get_formula(self, cr, uid, context=None):
        ids = self.pool.get('mgmtsystem.hazard.risk.computation').search(
            cr, uid, [('name', '=', 'A * B * C')], context=context
        )
        return ids and ids[0] or False

    _defaults = {
        'risk_computation_id': _get_formula
    }


class mgmtsystem_hazard_risk_type(orm.Model):

    _name = "mgmtsystem.hazard.risk.type"
    _description = "Risk type of the hazard"
    _columns = {
        'name': fields.char('Risk Type', size=50, required=True,
                            translate=True),
        'description': fields.text('Description'),
    }


class mgmtsystem_hazard_origin(orm.Model):

    _name = "mgmtsystem.hazard.origin"
    _description = "Origin of hazard"
    _columns = {
        'name': fields.char('Origin', size=50, required=True, translate=True),
        'description': fields.text('Description')
    }


class mgmtsystem_hazard_hazard(orm.Model):

    _name = "mgmtsystem.hazard.hazard"
    _description = "Hazard"
    _columns = {
        'name': fields.char('Hazard', size=50, required=True, translate=True),
        'description': fields.text('Description'),
    }


class mgmtsystem_hazard_probability(orm.Model):

    _name = "mgmtsystem.hazard.probability"
    _description = "Probability of hazard"
    _columns = {
        'name': fields.char('Probability', size=50, required=True,
                            translate=True),
        'value': fields.integer('Value', required=True),
        'description': fields.text('Description')
    }


class mgmtsystem_hazard_severity(orm.Model):

    _name = "mgmtsystem.hazard.severity"
    _description = "Severity of hazard"
    _columns = {
        'name': fields.char('Severity', size=50, required=True,
                            translate=True),
        'value': fields.integer('Value', required=True),
        'description': fields.text('Description')
    }


class mgmtsystem_hazard_usage(orm.Model):

    _name = "mgmtsystem.hazard.usage"
    _description = "Usage of hazard"
    _columns = {
        'name': fields.char('Occupation / Usage', size=50, required=True,
                            translate=True),
        'value': fields.integer('Value', required=True),
        'description': fields.text('Description')
    }


class mgmtsystem_hazard_control_measure(orm.Model):

    _name = "mgmtsystem.hazard.control_measure"
    _description = "Control Measure of hazard"
    _columns = {
        'name': fields.char('Control Measure', size=50, required=True,
                            translate=True),
        'responsible_user_id': fields.many2one('res.users', 'Responsible',
                                               required=True),
        'comments': fields.text('Comments'),
        'hazard_id': fields.many2one('mgmtsystem.hazard', 'Hazard',
                                     ondelete='cascade', select=True),
    }


class mgmtsystem_hazard_test(orm.Model):

    _name = "mgmtsystem.hazard.test"
    _description = "Implementation Tests of hazard"
    _columns = {
        'name': fields.char('Test', size=50, required=True, translate=True),
        'responsible_user_id': fields.many2one('res.users', 'Responsible',
                                               required=True),
        'review_date': fields.date('Review Date', required=True),
        'executed': fields.boolean('Executed'),
        'hazard_id': fields.many2one('mgmtsystem.hazard', 'Hazard',
                                     ondelete='cascade', select=True),
    }


class mgmtsystem_hazard_residual_risk(orm.Model):

    _name = "mgmtsystem.hazard.residual_risk"
    _description = "Residual Risks of hazard"

    def _compute_risk(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        mycompany = user.company_id

        for obj in self.browse(cr, uid, ids, context=context):
            if obj.probability_id and obj.severity_id and obj.usage_id:
                result[obj.id] = _parse_risk_formula(
                    mycompany.risk_computation_id.name,
                    obj.probability_id.value,
                    obj.severity_id.value,
                    obj.usage_id.value,
                )
            else:
                result[obj.id] = False

        return result

    _columns = {
        'name': fields.char('Name', size=50, required=True, translate=True),
        'probability_id': fields.many2one(
            'mgmtsystem.hazard.probability',
            'Probability',
            required=True,
        ),
        'severity_id': fields.many2one(
            'mgmtsystem.hazard.severity',
            'Severity',
            required=True,
        ),
        'usage_id': fields.many2one(
            'mgmtsystem.hazard.usage',
            'Occupation / Usage',
        ),
        'risk': fields.function(_compute_risk, string='Risk', type='integer'),
        'acceptability': fields.boolean('Acceptability'),
        'justification': fields.text('Justification'),
        'hazard_id': fields.many2one(
            'mgmtsystem.hazard',
            'Hazard',
            ondelete='cascade',
            select=True,
        ),
    }


class mgmtsystem_hazard(orm.Model):

    _name = "mgmtsystem.hazard"
    _description = "Hazards of the health and safety management system"

    def _compute_risk(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        mycompany = user.company_id

        for obj in self.browse(cr, uid, ids, context=context):
            if obj.probability_id and obj.severity_id and obj.usage_id:
                result[obj.id] = _parse_risk_formula(
                    mycompany.risk_computation_id.name,
                    obj.probability_id.value,
                    obj.severity_id.value,
                    obj.usage_id.value
                )
            else:
                result[obj.id] = False

        return result

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
        'risk_type_id': fields.many2one(
            'mgmtsystem.hazard.risk.type',
            'Risk Type',
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
        'risk': fields.function(_compute_risk, string='Risk', type='integer'),
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
        'residual_risk_ids': fields.one2many(
            'mgmtsystem.hazard.residual_risk',
            'hazard_id',
            'Residual Risk Evaluations',
        ),
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': (
            lambda self, cr, uid, c:
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id),
    }
