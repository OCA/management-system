# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardRiskComputation(orm.Model):

    _name = "mgmtsystem.hazard.risk.computation"
    _description = "Computation Risk"
    _columns = {
        'name': fields.char('Computation Risk', size=50, required=True),
        'description': fields.text('Description'),
    }
