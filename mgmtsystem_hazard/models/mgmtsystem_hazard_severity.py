# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardSeverity(orm.Model):

    _name = "mgmtsystem.hazard.severity"
    _description = "Severity of hazard"
    _columns = {
        'name': fields.char('Severity', size=50, required=True,
                            translate=True),
        'value': fields.integer('Value', required=True),
        'description': fields.text('Description')
    }
