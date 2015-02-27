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


class MgmtsystemVerificationLine(orm.Model):
    _name = "mgmtsystem.verification.line"
    _description = "Verification Line"
    _columns = {
        'name': fields.char('Question', size=300, required=True),
        'audit_id': fields.many2one(
            'mgmtsystem.audit',
            'Audit',
            ondelete='cascade',
            select=True,
        ),
        'procedure_id': fields.many2one(
            'document.page',
            'Procedure',
            ondelete='cascade',
            select=True,
        ),
        'is_conformed': fields.boolean('Is conformed'),
        'comments': fields.text('Comments'),
        'seq': fields.integer('Sequence'),
        'company_id': fields.many2one('res.company', 'Company')
    }

    _order = "seq"
    _defaults = {
        'company_id': (
            lambda self, cr, uid, c:
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id
        ),
        'is_conformed': False
    }
