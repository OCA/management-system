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
    "version": "10.0.1.2.2",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "description": """\
This module enables you to manage the different actions of your management
system:
  * immediate actions
  * corrective actions
  * preventive actions
  * improvement opportunities.
""",
    "depends": [
        'base_action_rule',
        'base_setup',
        'mgmtsystem',
        'mail', 
        'website'],
    "data": [
        'data/action_sequence.xml',
        'data/mgmtsystem_action_stage.xml',
        'data/automated_reminder.xml',
        'data/email_template.xml',
        #'data/workflow_mgmtsystem_action.xml',
        'security/ir.model.access.csv',
        'security/mgmtsystem_action_security.xml',
        'views/mgmtsystem_action.xml',
        'views/mgmtsystem_action_stage.xml',
        'views/board_mgmtsystem_action.xml',
        'reports/mgmtsystem_action_report.xml',
        'views/menus.xml',
    ],
    "demo": ['demo_action.xml'],
    "installable": True,
}
