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
<<<<<<< 697b7c1967849d398f6212cef8d15618f8ce3201
<<<<<<< b2fef5464e02e345d90a60666de68bf7b7affe15
<<<<<<< 0fd5d26265e2f6e7d4bd9dfb4a249f5d66986cfb
    "name" : "Management System - Audit",
    "version" : "1.1",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< 2627b530f5f4b36bc2c41ad049a8059c969263f9
<<<<<<< 3c33536853013978b851b9deacaa9c394c9db1b7
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
    "name": "Management System - Audit",
    "version": "1.2",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
<<<<<<< b2fef5464e02e345d90a60666de68bf7b7affe15
>>>>>>> [FIX] PEP8 compliance after running flake8
=======
>>>>>>> [FIX] PEP8 compliance in audit, action and nonconformity
    "description": """\
This module enables you to manage audits and verifications lists of your management system.
=======
    "name": "Management System - Audit",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
<<<<<<< e00fa43c595690d36669b683a085e5741efb9324
<<<<<<< 0bb2f475778b7c2c2694bf72154fdacddbde7d91
    "description": """\
This module enables you to manage audits and verifications lists of your
management system.
>>>>>>> Moved mgmtsystem_audit to root and fixed imports
    """,
=======
>>>>>>> [IMP] Module structure
    "depends": ['mgmtsystem_nonconformity'],
=======
    "depends": ['mgmtsystem_nonconformity', 'base_action_rule'],
>>>>>>> [MIG] mgmtsystem_audit
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
<<<<<<< e00fa43c595690d36669b683a085e5741efb9324
<<<<<<< 7b789f414fa0decc3c5afe3bd77d89f33eb53e4f
<<<<<<< 697b7c1967849d398f6212cef8d15618f8ce3201
    "installable": True,
=======
    'installable': True,
<<<<<<< 4f3f22d0380be9de7d49aa2a47077871c2b4c703
>>>>>>> Moved mgmtsystem_audit to root and fixed imports
    "certificate": ''
=======
>>>>>>> Removed vim lines
=======
    'installable': False,
>>>>>>> [MIG] Make modules uninstallable
=======
    'installable': True,
>>>>>>> [MIG] mgmtsystem_audit
}
