# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class mgmtsystem_hazard_control_measure(orm.Model):

    _name = "mgmtsystem.hazard.control_measure"
    _description = "Control Measure of hazard"
    _columns = {
        'name': fields.char('Control Measure', size=50, required=True,
                            translate=True),
        'responsible_user_id': fields.many2one('res.users', 'Responsible',
                                               required=True),
        'comments': fields.text('Comments'),
        'hazard_id': fields.many2one('mgmtsystem.hazard', 'Hazard',
                                     ondelete='cascade', select=True),
    }
