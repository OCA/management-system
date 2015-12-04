# -*- coding: utf-8 -*-

from openerp.osv import fields, orm


class MgmtSystemHazardTest(orm.Model):

    _name = "mgmtsystem.hazard.test"
    _description = "Implementation Tests of hazard"
    _columns = {
        'name': fields.char('Test', size=50, required=True, translate=True),
        'responsible_user_id': fields.many2one('res.users', 'Responsible',
                                               required=True),
        'review_date': fields.date('Review Date', required=True),
        'executed': fields.boolean('Executed'),
        'hazard_id': fields.many2one('mgmtsystem.hazard', 'Hazard',
                                     ondelete='cascade', select=True),
    }
