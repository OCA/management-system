# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Information Security Management System",
    "summary": "Manage your ISMS",
    "version": "19.0.1.0.1",
    "author": "Savoir-faire Linux, Gray Matter Logic, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management Systems",
    "depends": [
        "mgmtsystem_manual",
        "mgmtsystem_info_security_manual",
        "mgmtsystem_security_event",
        "mgmtsystem_action",
        "mgmtsystem_audit",
        "mgmtsystem_review",
    ],
    "data": [
        "data/mgmtsystem_system.xml",
        "views/mgmtsystem_action.xml",
    ],
    "installable": True,
    "application": True,
    "maintainers": ["max3903"],
}
