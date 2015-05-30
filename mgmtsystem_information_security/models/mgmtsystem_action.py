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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from tools.translate import _
from urllib import urlencode
from urlparse import urljoin
from openerp.osv import fields, orm


class mgmtsystem_action(orm.Model):
    _inherit = "mgmtsystem.action"
    _columns = {
        'control_ids': fields.many2many(
            'mgmtsystem.security.measure',
            'mgmtsystem_control_action_rel',
            'action_id',
            'control_id',
            'Controls',
        ),
    }
