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
<<<<<<< 3ef0d6681c9f2b5d1e2d5250a3a97b2ed9d9b6eb
<<<<<<< 1079161f42ff13d72cc09e135702bf9974ec0d26
    "name" : "Management System - Survey",
    "version" : "1.0",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< 94d214c43b1c1025f4471291cd2a5e0bcb297021
<<<<<<< 5df8409ead71a04a7588d51ad33d5d46bc319c79
    "license" : "AGPL-3",
=======
    "license" : "GPL",
>>>>>>> [CHG] AGPL license; set verion to 1.0
=======
    "license" : "AGPL-3",
>>>>>>> [CHG] Selections use words instead of letters; fixed AGPL-3 reference
    "category" : "Management System",
=======
    "name": "Management System - Survey",
    "version": "1.0",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
>>>>>>> [FIX] PEP8 compliance after running flake8
    "description": """This module enables you to manage your satisfaction surveys and its answers.""",
    "depends": ['survey'],
    "data": ['mgmtsystem_survey.xml'],
    "demo": [],
    "installable": True,
    "certificate": ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
    "name": "Management System - Survey",
    "version": "8.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "description": """\
This module enables you to manage your satisfaction surveys and its answers.
""",
    "depends": [
        'mgmtsystem',
        'survey'
    ],
    "data": [
        'data/survey_stage.xml',
        'views/survey_survey.xml',
    ],
    "demo": [
    ],
    'installable': True,
}
>>>>>>> Added mgmtsystem_survey to ported code
