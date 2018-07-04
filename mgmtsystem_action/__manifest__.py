# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System - Action",
    "version": "10.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ['mgmtsystem', 'mail'],
    "data": [
        'data/mgmtsystem_action_stage.xml',
        'data/automated_reminder.xml',
        'data/email_template.xml',
        'security/ir.model.access.csv',
        'security/mgmtsystem_action_security.xml',
        'data/action_sequence.xml',
        'views/mgmtsystem_action.xml',
        'views/mgmtsystem_action_stage.xml',
        'reports/mgmtsystem_action_report.xml',
        'views/menus.xml',
    ],
    "demo": [
        'demo/mgmtsystem_action.xml',
    ],
    'installable': True,
}
