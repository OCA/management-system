# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm


class mgmtsystem_audit(orm.Model):
    _name = "mgmtsystem.audit"
    _description = "Audit"
    _inherit = "crm.claim"
    _columns = {
        'name': fields.char('Name', size=50),
        'reference': fields.char('Reference', size=64, required=True, readonly=True),
        'date': fields.datetime('Date'),
        'line_ids': fields.one2many('mgmtsystem.verification.line', 'audit_id', 'Verification List'),
        'auditor_user_ids': fields.many2many('res.users', 'mgmtsystem_auditor_user_rel', 'user_id', 'mgmtsystem_audit_id', 'Auditors'),
        'auditee_user_ids': fields.many2many('res.users', 'mgmtsystem_auditee_user_rel', 'user_id', 'mgmtsystem_audit_id', 'Auditees'),
        'strong_points': fields.text('Strong Points'),
        'to_improve_points': fields.text('Points To Improve'),
        'imp_opp_ids': fields.many2many('mgmtsystem.action', 'mgmtsystem_audit_imp_opp_rel', 'mgmtsystem_action_id', 'mgmtsystem_audit_id', 'Improvement Opportunities'),
        'nonconformity_ids': fields.many2many('mgmtsystem.nonconformity', string='Nonconformities'),
        'state': fields.selection([('open', 'Open'), ('done', 'Closed')], 'State'),
        'system_id': fields.many2one('mgmtsystem.system', 'System'),
        'company_id': fields.many2one('res.company', 'Company')
        }

    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
        'reference': 'NEW',
        'state': 'open'
    }

    def create(self, cr, uid, vals, context=None):
        vals.update({
            'reference': self.pool.get('ir.sequence').get(cr, uid, 'mgmtsystem.audit')
        })
        return super(mgmtsystem_audit, self).create(cr, uid, vals, context)

    def button_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'done'})

    def message_auto_subscribe(self, cr, uid, ids, updated_fields, context=None):
        """Automatically add the Auditors, Auditees and Audit Manager to the follow list"""
        for o in self.browse(cr, uid, ids, context=context):
            user_ids = [o.user_id.id]
            user_ids += [a.id for a in o.auditor_user_ids]
            user_ids += [a.id for a in o.auditee_user_ids]
            self.message_subscribe_users(cr, uid, ids, user_ids=user_ids, subtype_ids=None, context=context)
        super(mgmtsystem_audit, self).message_auto_subscribe(cr, uid, ids, updated_fields, context=context)


class mgmtsystem_verification_line(orm.Model):
    _name = "mgmtsystem.verification.line"
    _description = "Verification Line"
    _columns = {
        'name': fields.char('Question', size=300, required=True),
        'audit_id': fields.many2one('mgmtsystem.audit', 'Audit', ondelete='cascade', select=True),
<<<<<<< ad4a1d15a9393eb931e2492c91792187aaf42bd0
        'procedure_id': fields.many2one('document.page', 'Procedure', ondelete='cascade', select=True),
	'is_conformed': fields.boolean('Is conformed'),
	'comments': fields.text('Comments'),
	'seq': fields.integer('Sequence'),
=======
        'procedure_id': fields.many2one('wiki.wiki', 'Procedure', ondelete='cascade', select=True),
        'is_conformed': fields.boolean('Is conformed'),
        'comments': fields.text('Comments'),
        'seq': fields.integer('Sequence'),
<<<<<<< 3c429ddfc9b244c4efbb2c0ec723d8e20dd12278
>>>>>>> [FIX] fixes from review comments
    }
=======
        'company_id': fields.many2one('res.company', 'Company')
        }

>>>>>>> [IMP] Add company_id in views
    _order = "seq"
    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
        'is_conformed': False
    }


class mgmtsystem_nonconformity(orm.Model):
    _name = "mgmtsystem.nonconformity"
    _inherit = "mgmtsystem.nonconformity"
    _columns = {
        'audit_ids': fields.many2many(
            'mgmtsystem.audit', string='Related Audits'),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
