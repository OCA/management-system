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
    "description": """
    """,
    "depends": [
        "information_security_manual",
        "document_page_work_instructions",
        "mgmtsystem_severity",
        "mgmtsystem_probability",
    ],
    "data": [
        "views/menus.xml",
        "views/security_measure.xml",
        "views/threat_origin.xml",
        "views/category_assets.xml",
        "views/essential_assets.xml",
        "views/underlying_assets.xml",
        "views/threat_scenario.xml",
        "views/security_events.xml",
    ],
    "demo": [],
    "installable": True,
}
