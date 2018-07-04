# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System",
    "version": "10.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    'images': ['images/mgmtsystem.png', 'images/mgmtsystem-hover.png'],
    "depends": [
        'base',
    ],
    "data": [
        'security/mgmtsystem_security.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/mgmtsystem_system.xml',
        'views/res_config.xml'
    ],
    "demo": [],
    'installable': True,
}
