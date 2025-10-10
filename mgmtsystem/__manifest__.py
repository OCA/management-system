# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System",
    "version": "18.0.1.1.4",
    "summary": "Support for management systems, such as ISO compliance.",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["web"],
    "data": [
        "security/mgmtsystem_security.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/mgmtsystem_document.xml",
        "views/mgmtsystem_system.xml",
        "views/res_config.xml",
    ],
    "application": True,
    "assets": {
        "web.assets_backend": [
            "mgmtsystem/static/src/**/*.esm.js",
            "mgmtsystem/static/src/**/*.xml",
        ],
    },
}
