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
{
    'name': 'Management System - Claims and Nonconformities',
    'version': '1.0',
    'author': 'Daniel Reis',
    'category': 'Management System',
    'description': """\
Extends the Nonconformity form so it can also represent NC candidates and other  types of feedback, such as complaints, measurements, suggestions, etc.

The "type" field identifies if the feedback corresponds to a nonconformity, or to other type of record, such as "best practice", "suggestion", etc.

This module purpose overlaps with "mgmtsystem_claim" module, so you should use either one or the other.
It will fit best to your uses cases requiring:
  * a common numbering sequence for complaints and nonconformities;
  * a single point-of-entry for all management system related occurrences.
""",
    'depends': ['mgmtsystem_nonconformity'],
    'data': [
        'security/ir.model.access.csv',
        'mgmtsystem_nonconformity.xml',
        'mgmtsystem_nonconformity_data.xml',
    ],
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
