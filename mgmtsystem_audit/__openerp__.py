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
    "name": "Management System - Audit",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ['mgmtsystem_nonconformity', 'base_action_rule'],
    "data": [
        'security/ir.model.access.csv',
        'security/mgmtsystem_audit_security.xml',
        'data/audit_sequence.xml',
        'data/audit_automated_actions.xml',
        'views/mgmtsystem_audit.xml',
        'report/audit.xml',
        'report/verification.xml',
        'report/report.xml',
        'report/mgmtsystem_audit_pivot.xml',
        'wizard/copy_verification_lines.xml',
    ],
    "demo": [
        'demo/demo_audit.xml',
    ],
    'installable': True,
}
