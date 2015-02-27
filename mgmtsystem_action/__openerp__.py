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
    "name": "Management System - Action",
    "version": "1.2",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "description": """
Management System - Action
==========================

This module enables you to manage the different actions of your management
system:
  * immediate actions
  * corrective actions
  * preventive actions
  * improvement opportunities.

Installation
============

To install this module, you need to:

* Clone the project from github on your instance
    * git clone https://github.com/OCA/management-system.git
* Start odoo with the project in the addons path

Configuration
=============

Usage
=====

Known issues / Roadmap
======================

None

Credits
=======

Contributors
------------
Daniel Reis <dreis.pt@hotmail.com>
Joao Alfredo Gama Batista <joao.gama@savoirfairelinux.com>
Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>
Pedro M. Baeza <pedro.baeza@gmail.com>
Sandy Carter <sandy.carter@savoirfairelinux.com>
Virgil Dupras <virgil.dupras@savoirfairelinux.com>

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
    "depends": ['mgmtsystem', 'crm_claim'],
    "data": [
        'security/ir.model.access.csv',
        'security/mgmtsystem_action_security.xml',
        'data/ir_sequence_type.xml',
        'data/ir_sequence.xml',
        'views/mgmtsystem_action.xml',
        'mgmtsystem_action_workflow.xml',
    ],
    "demo": [
        'demo/mgmtsystem_action.xml',
    ],
    "installable": True,
}
