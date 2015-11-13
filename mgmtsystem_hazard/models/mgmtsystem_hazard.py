# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


def _parse_risk_formula(formula, a, b, c):
    """Calculate the risk replacing the variables A, B, C into the formula."""
    f = formula.replace('A', str(a)).replace('B', str(b)).replace('C', str(c))
    return eval(f)


class MgmtSystemHazard(orm.Model):

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
