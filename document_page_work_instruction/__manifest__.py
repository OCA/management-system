# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Document Management - Wiki - Work Instructions",
    "version": "12.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
    "depends": [
        'document_page',
        'mgmtsystem',
    ],
    "data": [
        'data/document_page.xml',
        'views/document_page_work_instructions.xml',
    ],
    "demo": [],
    'installable': True,
}
