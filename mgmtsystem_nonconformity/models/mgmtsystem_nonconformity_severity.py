# -*- coding: utf-8 -*-
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

from openerp import models, fields


class MgmtsystemNonconformitySeverity(models.Model):

    """Nonconformity Severity - Critical, Major, Minor, Invalid, ..."""

    _name = "mgmtsystem.nonconformity.severity"
    _description = "Severity of Complaints and Nonconformities"

    name = fields.Char("Title", required=True, translate=True)
    sequence = fields.Integer('Sequence')
    description = fields.Text('Description', translate=True)
    active = fields.Boolean('Active?', default=True)
