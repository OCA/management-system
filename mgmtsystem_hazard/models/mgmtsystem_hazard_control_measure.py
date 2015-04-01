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
