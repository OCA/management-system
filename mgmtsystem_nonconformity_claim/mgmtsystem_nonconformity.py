# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2012 Daniel Reis
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


class mgmtsystem_nonconformity_type(orm.Model):
    """Claim Type: Nonconformity, Good Practice, Improvement Opportunity, Observation, ..."""
    _name = "mgmtsystem.nonconformity.type"
    _description = "Claim Type"
    _columns = {
        'name': fields.char('Title', size=50, required=True, translate=True),
        'description': fields.text('Description', translate=True),
        'active': fields.boolean('Active?'),
    }
    _defaults = {
        'active': True,
    }


class mgmtsystem_nonconformity(orm.Model):
    _name = "mgmtsystem.nonconformity"
    _inherit = "mgmtsystem.nonconformity"
    _description = "Feedback and Nonconformities"
    _columns = {
        'type_id': fields.many2one('mgmtsystem.nonconformity.type', 'Type'),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
