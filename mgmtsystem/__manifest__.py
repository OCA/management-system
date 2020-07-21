# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System",
    "version": "13.0.1.4.1",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/management-system",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ["base"],
    "data": [
        "security/mgmtsystem_security.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/mgmtsystem_system.xml",
        "views/res_config.xml",
    ],
    "installable": True,
    "application": True,
}
