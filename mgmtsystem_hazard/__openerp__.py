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
    "name": "Management System - Hazard",
    "version": "7.0.1.2.1",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "description": """\
This module enables you to manage the hazards and risks of your health
and safety management system.

Configuration
=============

To configure this module, you need to:
* go to Settings > Companies > Companies
* open your company
* in the configuration tab, select the default computation method for risk.

A is for probability, B for severity and C for occupation/usage.
    """,
    "depends": ['mgmtsystem', 'hr'],
    "data": [
        'data/mgmtsystem_hazard_data.xml',
        'security/ir.model.access.csv',
        'security/mgmtsystem_hazard_security.xml',
        'views/mgmtsystem_hazard.xml',
    ],
}
