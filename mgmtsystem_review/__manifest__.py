# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
<<<<<<< 175f2f66ce72543a357e8fd8e89b4ba0f9e8a52c
<<<<<<< a2fe05867a1faacf29508c3abc1f0c8b98285c87
    "name" : "Management System - Review",
    "version" : "1.0",
    "author" : "Savoir-faire Linux",
    "website" : "http://www.savoirfairelinux.com",
<<<<<<< 3f17ee8a034d239a66d5f045cbd9a8a03a6363a9
<<<<<<< d494b4b853d2a89f552200583478a2ebdffcb095
    "license" : "AGPL-3",
=======
    "license" : "AGPL",
>>>>>>> [CHG] AGPL license; set verion to 1.0
=======
    "license" : "AGPL-3",
>>>>>>> [CHG] Selections use words instead of letters; fixed AGPL-3 reference
    "category" : "Management System",
=======
    "name": "Management System - Review",
    "version": "1.0",
    "author": "Savoir-faire Linux",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
>>>>>>> [FIX] PEP8 compliance after running flake8
    "description": """\
This module enables you to manage reviews of your management system.
    """,
=======
    "name": "Management System - Review",
    "version": "10.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
>>>>>>> Moved mgmtsystem_review to root folder
    "depends": [
        'mgmtsystem_nonconformity',
        'mgmtsystem_survey',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/mgmtsystem_review_security.xml',
<<<<<<< 175f2f66ce72543a357e8fd8e89b4ba0f9e8a52c
        'review_sequence.xml',
        'mgmtsystem_review.xml',
        'report/review_report.xml',
    ],
    "demo": [],
    "installable": True,
    "certificate": ''
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
        'data/ir_sequence.xml',
        'views/mgmtsystem_review.xml',
        'report/review.xml',
        'report/report.xml',
    ],
    'installable': True,
}
>>>>>>> Moved mgmtsystem_review to root folder
