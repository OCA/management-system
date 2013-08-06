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
    "description": """\
This module enables you to manage audits and verifications lists of your management system.
    """,
    "depends": ['mgmtsystem_nonconformity'],
    "data" : [
        'audit_sequence.xml',
        'security/ir.model.access.csv',
        'mgmtsystem_audit.xml',
        'report/audit_report.xml',
        'report/verification_list.xml',
        'board_mgmtsystem_audit.xml',
        'wizard/copy_verification_lines.xml',
    ],
    "demo" : [
        'demo_audit.xml',
    ],
    "installable" : True,
    "certificate" : ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
