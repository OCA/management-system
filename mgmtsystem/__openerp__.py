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
    "name" : "Management System",
    "version" : "1.0",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< 2a6ada183c513dd0c7f6c3159cffe689e46bfb50
<<<<<<< 3bd4e08be18e0d712e45b8d242493aaf1167aec7
    "license" : "AGPL-3",
=======
    "license" : "AGPL",
>>>>>>> [CHG] AGPL license; set verion to 1.0
=======
    "license" : "AGPL-3",
>>>>>>> [CHG] Selections use words instead of letters; fixed AGPL-3 reference
    "category" : "Management System",
    "complexity" : "normal",
    "description": """\
This module is the basis of any management system applications:
     * audit reports,
     * nonconformities,
     * immediate actions,
     * preventive actions,
     * corrective actions,
     * improvement opportunities.
    """,
    "depends" : ['base','board','document_page'],
    "init_xml" : [],
    "update_xml" : [
        'security/mgmtsystem_security.xml',
        'security/ir.model.access.csv',
        'mgmtsystem.xml',
        'mgmtsystem_system.xml',
        'board_mgmtsystem_view.xml',
    ],
    "demo_xml" : [],
    "installable" : True,
    "certificate" : ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

