# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


def _parse_risk_formula(formula, a, b, c):
    """Calculate the risk replacing the variables A, B, C into the formula."""
    f = formula.replace('A', str(a)).replace('B', str(b)).replace('C', str(c))
    return eval(f)


class MgmtSystemHazardResidualRisk(orm.Model):

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
