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
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
<<<<<<< 19a28d85a2132bf3e180ba87be85af98327c8555
<<<<<<< 8c635f233cfc8f312d5a86ef4faca6fd8d2bf583
    "name" : "Management System - Action",
    "version" : "1.1",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< 8f0c518b2805edad798595942b974503d66a3e4f
<<<<<<< ccdb4bd26de7eaa4305a9d2bdfa2170ba166363e
    "license" : "AGPL-3",
=======
    "license" : "AGPL",
>>>>>>> [CHG] AGPL license; set verion to 1.0
=======
    "license" : "AGPL-3",
>>>>>>> [CHG] Selections use words instead of letters; fixed AGPL-3 reference
    "category" : "Management System",
=======
=======
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
=======
>>>>>>> Ported mgmtsystem_action
    "name": "Management System - Action",
    "version": "1.2",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
<<<<<<< 19a28d85a2132bf3e180ba87be85af98327c8555
>>>>>>> [FIX] PEP8 compliance after running flake8
=======
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
    "description": """\
This module enables you to manage the different actions of your management system:
=======
    "description": """\
This module enables you to manage the different actions of your management
system:
>>>>>>> Ported mgmtsystem_action
  * immediate actions
  * corrective actions
  * preventive actions
  * improvement opportunities.
""",
    "depends": ['mgmtsystem', 'crm_claim'],
    "data": [
        'security/ir.model.access.csv',
        'security/mgmtsystem_action_security.xml',
        'action_sequence.xml',
        'workflow_mgmtsystem_action.xml',
        'mgmtsystem_action.xml',
        'board_mgmtsystem_action.xml',
    ],
    "demo": ['demo_action.xml'],
<<<<<<< 2cb3e23cd6da406a2afd4eedfd7745ab01746e88
    "installable": True,
=======
    'installable': True,
>>>>>>> Ported mgmtsystem_action
}
