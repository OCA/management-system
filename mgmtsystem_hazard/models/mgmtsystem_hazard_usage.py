# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardUsage(orm.Model):

    _name = "mgmtsystem.hazard.usage"
    _description = "Usage of hazard"
    _columns = {
        'name': fields.char('Occupation / Usage', size=50, required=True,
                            translate=True),
        'value': fields.integer('Value', required=True),
        'description': fields.text('Description')
    }
