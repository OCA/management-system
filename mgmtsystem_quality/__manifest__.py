# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Quality Management System",
    "summary": "Manage your quality management system",
    "version": "12.0.1.0.0",
    "author": "Savoir-faire Linux, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        "mgmtsystem_audit",
        "document_page_quality_manual",
        "mgmtsystem_review",
    ],
    "data": [
        "data/mgmtsystem_system.xml",
    ],
    "development_status": "Production/Stable",
    "maintainers": ["max3903"],
}
