# -*- encoding: utf-8 -*-
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
{
    "name": "Management System Security Event",
    "version": "0.1",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "complexity": "normal",
    "description": """\
Management System Security Event
================================

This module allow you to manage security events.

Installation
============

To install this module, you need to:

 * Clone the project from github on your instance
    * git clone https://github.com/OCA/management-system.git
 * Start odoo with the project in the addons path

Configuration
=============

No configuration needed

Usage
=====

To use this module, you need to:

 * go to Management System > Configuration > Manuals > Security Events
 * go to Management System > Configuration > Security 

For further information, please visit:

 * https://github.com/OCA/management-system/issues

Known issues / Roadmap
======================

 None

Credits
=======

Contributors
------------

* Loïc Faure-Lacroix <loic.lacroix@savoirfairelinux.com>

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
    """,
    "depends": [
        "information_security_manual",
        "document_page_work_instructions",
        "mgmtsystem_severity",
        "mgmtsystem_probability",
    ],
    "data": [
        "data/document_page.xml",
        "views/menus.xml",
        "views/security_measure.xml",
        "views/threat_origin.xml",
        "views/category_assets.xml",
        "views/essential_assets.xml",
        "views/underlying_assets.xml",
        "views/threat_scenario.xml",
        "views/security_events.xml",
        "views/security_event_scenario.xml",
        "views/security_event_measure.xml",
    ],
    "demo": [],
    "installable": True,
}
