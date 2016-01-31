# -*- coding: utf-8 -*-
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
    "name": "Feared Events",
    "summary": "Manage your security events",
    "version": "7.0.0.0.1",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "description": """\
Feared Events
=============

This module allows you to manage feared events of your Information Security
Management System (ISMS).
    """,
    "depends": [
        "document_page_work_instructions",
        "mgmtsystem_severity",
        "mgmtsystem_probability",
        'report_webkit',
    ],
    "data": [
        "data/document_page.xml",
        'data/mgmtsystem_risk_matrix_level.xml',
        "views/menus.xml",
        "views/mgmtsystem_security_asset_category.xml",
        "views/mgmtsystem_security_asset_primary.xml",
        "views/mgmtsystem_security_asset_supporting.xml",
        "views/mgmtsystem_security_event.xml",
        "views/mgmtsystem_security_event_control.xml",
        "views/mgmtsystem_security_event_scenario.xml",
        "views/mgmtsystem_security_control.xml",
        "views/mgmtsystem_security_threat_source.xml",
        "views/mgmtsystem_security_vector.xml",
        'views/mgmtsystem_risk_matrix.xml',
        'views/mgmtsystem_risk_matrix_level.xml',
        'report/header.xml',
        'report/report.xml',
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
}
