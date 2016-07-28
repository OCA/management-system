<<<<<<< 30d639046d4a0862cd4144a32f76826bb489b0b0
# -*- encoding: utf-8 -*-
=======
# -*- coding: utf-8 -*-
>>>>>>> Migrate mgmtsystem_quality
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
<<<<<<< 30d639046d4a0862cd4144a32f76826bb489b0b0
<<<<<<< 1f65871678dc62e50eb086ae107502490474b8ec
    "name" : " Quality Management System",
    "version" : "1.0",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< d9d582b596182f5ff2408dbec985ae954a121edf
<<<<<<< ab17a67d5cf4de853b75c589fd094a698c2c878d
    "license" : "AGPL-3",
=======
    "license" : "AGPL",
>>>>>>> [CHG] AGPL license; set verion to 1.0
=======
    "license" : "AGPL-3",
>>>>>>> [CHG] Selections use words instead of letters; fixed AGPL-3 reference
    "category" : "Management System",
=======
    "name": " Quality Management System",
    "version": "1.0",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
>>>>>>> [FIX] PEP8 compliance after running flake8
    "description": """\
This module enables you to manage your quality management system, including :
    * Quality Manual
    * Reviews
    * Audits
    * Procedures
    * Nonconformities
    * Actions
    * Employee Training
    """,
=======
    "name": "Quality Management System",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
>>>>>>> Migrate mgmtsystem_quality
    "depends": [
        'mgmtsystem_audit',
        'document_page_quality_manual',
        'mgmtsystem_review',
    ],
<<<<<<< 30d639046d4a0862cd4144a32f76826bb489b0b0
    "data": ['quality.xml'],
    "demo": [],
    "installable": True,
    "application": True,
    "certificate": ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
    "data": [
        'data/mgmtsystem_system.xml',
    ],
    'installable': True,
    "application": True,
}
>>>>>>> Migrate mgmtsystem_quality
