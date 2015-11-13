# -*- coding: utf-8 -*-


from openerp.osv import fields, orm


class MgmtSystemHazardOrigin(orm.Model):

    _name = "mgmtsystem.hazard.origin"
    _description = "Origin of hazard"
    _columns = {
        'name': fields.char('Origin', size=50, required=True, translate=True),
        'description': fields.text('Description')
    }
