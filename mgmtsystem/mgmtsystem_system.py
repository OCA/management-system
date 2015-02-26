# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm


def get_company(self, cr, uid, c):
    """Call the class method _get_company"""
    return self._get_company(cr, uid, c)


class mgmtsystem_system(orm.Model):

    _name = 'mgmtsystem.system'
    description = 'System'

    _columns = {
        'name': fields.char('System', size=30, required=True, translate=True),
        'manual': fields.many2one('document.page', 'Manual'),
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': get_company,
    }

    def _get_company(self, cr, uid, context):
        """
        Get the company for the current user.

        Can be overriden by subclasses.
        """
        user_model = self.pool.get('res.users')
        return user_model.browse(cr, uid, uid, context).company_id.id
