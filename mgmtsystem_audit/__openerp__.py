# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
{
    "name" : "Management System - Audit",
    "version" : "0.1",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
    "license" : "GPL-3",
    "category" : "Management System",
    "description": """
	This module enables you to manage audits and verifications lists of 
        your management system.
    """,
    "depends" : ['mgmtsystem_nonconformity','audittrail'],
    "init_xml" : [
	'audit_sequence.xml',
    ],
    "update_xml" : [
        'security/ir.model.access.csv',
	'mgmtsystem_audit.xml',
	'report/audit_report.xml',
	'report/verification_list.xml',
	'board_mgmtsystem_audit.xml',
        'wizard/copy_verification_lines.xml',
    ],
    "demo_xml" : [
	'demo_audit.xml',
    ],
    "installable" : True,
    "certificate" : ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

