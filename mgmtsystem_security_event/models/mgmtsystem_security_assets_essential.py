# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 - Present
#    Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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
from .mgmtsystem_security_event import _default_system_id


class EssentialAssets(orm.Model):

    """Essential assets."""

    _name = "mgmtsystem.security.assets.essential"
    _description = "Essential Assets"

    _columns = {
        'name': fields.char("Name"),
        'description': fields.text("Description"),
        'responsible_id': fields.many2one("res.users", "Responsible"),
        'system_id': fields.many2one(
            'mgmtsystem.system', 'Management System',
            required=True,
        ),
        'company_id': fields.related(
            'system_id',
            'company_id',
            string='Company',
            readonly=True,
            type='many2one',
            relation='res.company',
            store=True,
        ),
    }

    _defaults = {
        'system_id': _default_system_id,
    }
