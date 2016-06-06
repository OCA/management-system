# -*- coding: utf-8 -*-
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
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ['mgmtsystem', 'mail'],
    "data": [
        'data/mgmtsystem_action_stage.xml',
        'data/automated_reminder.xml',
        'data/email_template.xml',
        'security/ir.model.access.csv',
        'security/mgmtsystem_action_security.xml',
        'data/action_sequence.xml',
        'views/mgmtsystem_action.xml',
        'views/mgmtsystem_action_stage.xml',
        'reports/mgmtsystem_action_report.xml',
        'views/menus.xml',
    ],
    "demo": [
        'demo/mgmtsystem_action.xml',
    ],
    'installable': True,
}
