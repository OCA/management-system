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
    "name": "Hazard Risk",
    "version": "8.0.1.1.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_hazard',
        'hr'
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/mgmtsystem_hazard_risk_computation.xml',
        'data/mgmtsystem_hazard_risk_type.xml',
        'views/res_company.xml',
        'views/mgmtsystem_hazard.xml',
        'views/mgmtsystem_hazard_risk_type.xml',
        'views/mgmtsystem_hazard_risk_computation.xml',
        'views/mgmtsystem_hazard_residual_risk.xml',
    ],
    "installable": True,
}
