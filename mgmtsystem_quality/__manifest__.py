# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Quality Management System",
    "version": "10.0.1.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_audit',
        'document_page_quality_manual',
        'mgmtsystem_review',
    ],
    "data": [
        'data/mgmtsystem_system.xml',
    ],
    'installable': True,
    "application": True,
}
