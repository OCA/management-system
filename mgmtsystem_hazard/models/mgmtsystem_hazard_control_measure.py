# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardHazard(orm.Model):

    _name = "mgmtsystem.hazard.hazard"
    _description = "Hazard"
    _columns = {
        'name': fields.char('Hazard', size=50, required=True, translate=True),
        'description': fields.text('Description'),
    }
