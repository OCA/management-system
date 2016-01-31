# -*- coding: utf-8 -*-
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
from itertools import permutations


class MgmtsystemRiskMatrixLevel(orm.Model):
    _name = "mgmtsystem.risk.matrix.level"
    _description = "Management System Risk Matrix Level"

    _columns = {
        'probability_min': fields.integer(
            'Minimal Probability', required=True
        ),
        'probability_max': fields.integer(
            'Maximal Probability', required=True
        ),
        'severity_min': fields.integer(
            'Minimal Severity', required=True
        ),
        'severity_max': fields.integer(
            'Maximal Severity', required=True
        ),
        'color': fields.selection(
            [
                ('green', 'Green'),
                ('orange', 'Orange'),
                ('red', 'Red'),
            ],
            'Color', required=True, type='char',
            help="The color to display in the matrix",
        ),
    }

    _order = 'severity_min,probability_min'

    _defaults = {
        'probability_min': 1,
        'probability_max': 1,
        'severity_min': 1,
        'severity_max': 1,
        'color': 'green',
    }

    def _check_overlapping_levels(self, cr, uid, ids, context=None):
        all_level_ids = self.search(cr, uid, [], context=context)
        all_levels = self.browse(cr, uid, all_level_ids, context=context)
        for l1, l2 in permutations(all_levels, 2):
            if (
                l1.probability_min <= l2.probability_min <=
                l1.probability_max and
                l1.severity_min <= l2.severity_min <=
                l1.severity_max
            ):
                return False
        return True

    _constraints = [
        (
            _check_overlapping_levels,
            "You can not have overlapping risk matrix levels.", [
                'probability_min',
                'probability_max',
                'severity_min',
                'severity_max',
            ]
        ),
    ]
