# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Quality Management System",
    "summary": "Manage your quality management system",
    "version": "19.0.1.0.1",
    "author": "Savoir-faire Linux, Gray Matter Logic, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management Systems",
    "depends": [
        "mgmtsystem_manual",
        "mgmtsystem_audit",
        "document_page_quality_manual",
        "mgmtsystem_review",
    ],
    "data": ["data/mgmtsystem_system.xml"],
    "installable": True,
    "application": True,
    "maintainers": ["max3903"],
}
