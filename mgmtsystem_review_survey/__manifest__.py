# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System - Review Survey",
    "version": "18.0.2.0.0",
    "author": "Savoir-faire Linux, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["mgmtsystem_review", "survey"],
    "data": [
        "views/mgmtsystem_review_views.xml",
        "report/review.xml",
    ],
    "installable": True,
    "auto_install": True,
}
