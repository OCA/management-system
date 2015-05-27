# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux, Odoo Community Association (OCA)
#    (http://www.savoirfairelinux.com).
#
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

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml # noqa
    # for the full list
    'category': 'Management System',
    'summary': 'Manage your ISMS',
    'description': """
Information Security Management System
======================================

This module adds a new management system and installs all the applications required to deploy and manage your Information Security Management System (ISMS), compliant with ISO 27001 standard

Installation
============

Before installing the module, you need to define the scope of your system and drive a security analysis. Method like EBIOS (http://en.wikipedia.org/wiki/EBIOS) can help you with the analysis, evaluation and action on risks relating to information systems.

Configuration
=============

To configure this module, you need to:

 * In the Configuration menu, define your Asset Categories and Threat Origins
 * In the Manuals menu, define your Assets (Essentials and Underlying), Measures, Threat Scenarios, Security Events and Work Instructions

Usage
=====

To use this module, you need to:

 * Plan Audits and Top Management Reviews
 * Manage your Nonconformities and Actions

For further information, please visit:

 * https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

 * https://github.com/OCA/management-system/issues

Credits
=======

Contributors
------------

* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

* Module exported by the Module Prototyper module for version 8.0.
* If you have any questions, please contact Savoir-faire Linux
(support@savoirfairelinux.com)
""",

    # any module necessary for this one to work correctly
    'depends': [
        'mgmtsystem_security_event',
        'information_security_manual',
        'mgmtsystem_audit',
        'mgmtsystem_review',
    ],
    'external_dependencies': {
        'python': [],
    },

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    # used for Javascript Web CLient Testing with QUnit / PhantomJS
    # https://www.odoo.com/documentation/8.0/reference/javascript.html#testing-in-odoo-web-client  # noqa
    'js': [],
    'css': [],
    'qweb': [],

    'installable': True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    'auto_install': False,
    'application': True,
}
