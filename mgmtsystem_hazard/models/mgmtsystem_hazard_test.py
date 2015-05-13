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

from openerp import models, fields


class MgmtsystemHazardTest(models.Model):

    _name = "mgmtsystem.hazard.test"
    _description = "Implementation Tests of hazard"

    name = fields.Char('Test', size=50, required=True, translate=True)
    responsible_user_id = fields.Many2one(
        'res.users',
        'Responsible',
        required=True,
    )
    review_date = fields.Date('Review Date', required=True)
    executed = fields.Boolean('Executed')
    hazard_id = fields.Many2one(
        'mgmtsystem.hazard',
        'Hazard',
        ondelete='cascade',
        required=False,
        select=True,
    )
