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
    "name": "Health and Safety Management System",
    "version": "1.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "description": """\
This module enables you to manage your health and safety management system,
including :
            * Hazards
            * Equipments
            * Employee Training
            * Reviews
            * Audits
            * Procedures
            * Nonconformities
            * Actions
            * Claims
            * Letters
    """,
    "depends": [
        'mgmtsystem_audit',
        'mgmtsystem_review',
        'mgmtsystem_claim',
        'document_page_health_safety_manual',
        'mgmtsystem_hazard',
    ],
    "data": ['health_safety.xml'],
    "demo": [],
    'installable': False,
    "application": True,
    "certificate": ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
