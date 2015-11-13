# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardType(orm.Model):

    _name = "mgmtsystem.hazard.type"
    _description = "Type of hazard"
    _columns = {
        'name': fields.char('Type', size=50, required=True, translate=True),
        'description': fields.text('Description'),
    }
