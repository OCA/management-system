# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2015
#       Savoir-faire Linux (http://www.savoirfairelinux.com)
#       Odoo Community Association (OCA)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Information Security Management System',
    'version': '0.1',
    'author': 'Savoir-faire Linux, Odoo Community Association (OCA)',
    'maintainer': 'Odoo Community Association (OCA)',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3 or any later version',
    'category': 'Management System',
    'summary': 'Manage your ISMS',
    'description': """
Information Security Management System
======================================

This module adds a new management system and installs all the applications
required to deploy and manage your Information Security Management System
(ISMS), compliant with ISO 27001 standard
""",

    'depends': [
        'mgmtsystem_security_event',
        'information_security_manual',
        'mgmtsystem_audit',
        'mgmtsystem_review',
    ],
    'external_dependencies': {
        'python': [],
    },

    'data': [
    ],
    'demo': [
    ],

    'js': [],
    'css': [],
    'qweb': [],

    'installable': True,
    'auto_install': False,
    'application': True,
}
