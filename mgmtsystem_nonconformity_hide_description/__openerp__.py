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
{
    "name": "Management System - Nonconformity - Hide Description",
    "version": "0.1",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "summary": "Hide the description in the tree view of nonconformities",
    "description": """
Management System - Nonconformity - Hide Description
====================================================
The description are multi-lines and might break the tree structure.
To ease the usage and the readability of the nonconformities in the list view,
the description column is removed.

Contributors
------------
*Fonctionels:*
    * Maxime Chambreuil (maxime.chambreuil@savoirfairelinux.com)
    * Julien Roux (julien.roux@savoirfairelinux.com)

*Developpers:*
    * Jordi Riera (jordi.riera@savoirfairelinux.com)

More information
----------------
Module developed and tested with OpenERP version 7.0
For questions, please contact our support services
(support@savoirfairelinux.com)

    """,
    "depends": [
        'mgmtsystem_nonconformity',
    ],
    "data": [
        'mgmtsystem_nonconformity.xml',
    ],
    "demo": [
    ],
    "installable": True,
}
