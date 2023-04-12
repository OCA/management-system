# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Document Management - Wiki - Procedures",
    "version": "14.0.2.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["document_page_tag", "mgmtsystem"],
    "data": [
        "data/document_page_procedure.xml",
        "data/document_page_tag.xml",
        "views/document_page_procedure.xml",
    ],
    "demo": ["demo/document_page_procedure.xml"],
    "installable": True,
}
