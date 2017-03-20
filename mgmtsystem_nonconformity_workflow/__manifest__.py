# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Eugen Don (<https://www.don-systems.de>).
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
    "name": "Management System - Nonconformity - Workflow",
    "version": "10.0.1.0.0",
    "author": "Eugen Don - Don-Systems, Odoo Community Association (OCA)",
    "website": "http://www.don-systems.de",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_nonconformity',
    ],
    "data": [
        'views/mgmtsystem_nonconformity_workflow.xml',
        'data/workflow.xml',
    ],
    "images": [],
    "demo": [
    ],
    'installable': True,
}
