# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from osv import fields, osv
from tools.translate import _

class mgmtsystem_review(osv.osv):
    _name = "mgmtsystem.review"
    _description = "Review"
    _columns = {
        'name': fields.char('Name', size=50, required=True),
        'reference': fields.char('Reference', size=64, required=True, readonly=True),
        'date': fields.datetime('Date', required=True),
	'user_ids': fields.many2many('res.users','mgmtsystem_review_user_rel','user_id','mgmtsystem_review_id','Participants'),
	'response_ids': fields.many2many('survey.response','mgmtsystem_review_response_rel','response_id','mgmtsystem_review_id','Survey Answers'),
        'policy': fields.text('Policy'),
        'changes': fields.text('Changes'),
        'line_ids': fields.one2many('mgmtsystem.review.line','review_id','Lines'),
        'conclusion': fields.text('Conclusion'),
        'state': fields.selection([('o','Open'),('c','Closed')], 'State')
    }

    _defaults = {
        'reference': 'NEW', 
        'state': 'o'
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'reference': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.review')
        })
        return super(mgmtsystem_review, self).create(cr, uid, vals, context)

    def button_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'c'})

mgmtsystem_review()

class mgmtsystem_review_line(osv.osv):
    _name = "mgmtsystem.review.line"
    _description = "Review Line"
    _columns = {
	'name': fields.char('Title',size=300, required=True),
        'type': fields.selection((('action','Action'), ('nonconformity','Noncomformity')),'Type'),
        'action_id': fields.many2one('mgmtsystem.action', 'Action', select=True),
        'nonconformity_id': fields.many2one('mgmtsystem.nonconformity', 'Nonconformity', select=True),
        'decision': fields.text('Decision'),
        'review_id': fields.many2one('mgmtsystem.review', 'Review', ondelete='cascade', select=True),
    }

mgmtsystem_review_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
