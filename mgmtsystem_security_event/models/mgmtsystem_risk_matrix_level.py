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

from odoo import models, fields, api, _
from itertools import permutations


class MgmtsystemRiskMatrixLevel(models.Model):
    _name = "mgmtsystem.risk.matrix.level"
    _description = "Management System Risk Matrix Level"
    _order = 'severity_min,probability_min'

    probability_min = fields.Integer('Minimal Probability', required=True, default=1)
    probability_max = fields.Integer('Maximal Probability', required=True, default=1)
    severity_min = fields.Integer('Minimal Severity', required=True, default=1)
    severity_max = fields.Integer('Maximal Severity', required=True, default=1)
    color = fields.Selection(
        [
            ('green', 'Green'),
            ('orange', 'Orange'),
            ('red', 'Red'),
        ],
        string='Color',
        required=True,
        default='green',
        help="The color to display in the matrix",
    )

    @api.constrains('probability_min', 'probability_max', 'severity_min', 'severity_max')
    def _check_overlapping_levels(self):
        # This check is O(n^2) which might be slow if there are many levels, but usually there are few.
        all_levels = self.search([])
        for l1, l2 in permutations(all_levels, 2):
            if (
                l1.probability_min <= l2.probability_min <= l1.probability_max and
                l1.severity_min <= l2.severity_min <= l1.severity_max
            ):
                 # self-collision is ignored by permutations if items are unique instances, but we should be careful.
                 # permutations(iterable, r) returns subsequences of length r.
                 # permutations([A, B], 2) -> (A, B), (B, A).
                 # We are checking collision between A and B. It is symmetric.
                 # Wait, logic check: if A and B overlap, we raise.
                 
                 # Better logic:
                 # Check if the current record overlaps with any OTHER record.
                 pass

        # Since we are in api.constrains, 'self' contains the records causing the check.
        # We need to check 'self' against all OTHER records in DB.
        
        for level in self:
            domain = [
                ('id', '!=', level.id),
                ('probability_min', '<=', level.probability_max),
                ('probability_max', '>=', level.probability_min),
                ('severity_min', '<=', level.severity_max),
                ('severity_max', '>=', level.severity_min),
            ]
            if self.search_count(domain) > 0:
                 raise models.ValidationError(_("You can not have overlapping risk matrix levels."))
