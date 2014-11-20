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

<<<<<<< c9a3eba175d74c79a93a10ed28643b85214dc452
from osv import fields, orm


class mgmtsystem_system(orm.Model):
=======
from openerp import models, fields

own_company = lambda self: self.env.user.company_id.id


class mgmtsystem_system(models.Model):
>>>>>>> Ported mgmtsystem

    _name = 'mgmtsystem.system'
    description = 'System'

<<<<<<< 5e60e0b3b06575444d36910bf02a9da94dde574c
<<<<<<< 0432e9c08747eb002779bcbf4a681c45f4c9ae47
<<<<<<< c9a3eba175d74c79a93a10ed28643b85214dc452
    _columns = {
<<<<<<< 246504adbebf5957ae9fe262cb1b09aa7213ab41
        'name': fields.char('System', size=30, required=True, translate=True),
        'manual': fields.many2one('wiki.wiki', 'Manual'),
=======
        'name': fields.char('System', size=30, required=True),
        'manual': fields.many2one('document.page', 'Manual'),
>>>>>>> [IMP] Update hooks with addons modules from v7
        'company_id': fields.many2one('res.company', 'Company')
    }

    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
    name = fields.Char('System', size=30, require=True, translate=True)
    manual = fields.Many2one('document.page', 'Manual')
    company_id = fields.Many2one('res.company', 'Company',
                     	  default=lambda self: self.env.user.company_id.id)
>>>>>>> Ported mgmtsystem
=======
    name = fields.Char('System', size=30, required=True, translate=True)
=======
    name = fields.Char('System', required=True, translate=True)
>>>>>>> Removed vim lines and size=30 on attribute name
    manual = fields.Many2one('document.page', 'Manual')
    company_id = fields.Many2one('res.company', 'Company', default=own_company)
>>>>>>> Fix some issues with pep8 and typo for attribute required
