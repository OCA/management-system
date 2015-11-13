# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardProbability(orm.Model):

    _name = "mgmtsystem.hazard.probability"
    _description = "Probability of hazard"
    _columns = {
        'name': fields.char('Probability', size=50, required=True,
                            translate=True),
        'value': fields.integer('Value', required=True),
        'description': fields.text('Description')
    }
