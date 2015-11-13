# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardRiskType(orm.Model):

    _name = "mgmtsystem.hazard.risk.type"
    _description = "Risk type of the hazard"
    _columns = {
        'name': fields.char('Risk Type', size=50, required=True,
                            translate=True),
        'description': fields.text('Description'),
    }
