# -*- coding: utf-8 -*-
{
    "name": "Management System - Project",
    "version": "9.0.1.0.0",
    "author": "Savoir-faire Linux,Odoo Community Association (OCA)",
    "website": "http://www.savoirfairelinux.com",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_nonconformity',
        'mgmtsystem_action',
        'project',
    ],
    "data": [
        'views/mgmtsystem_nonconformity_project.xml',
    ],
    "demo": [],
    'installable': True,
    "post_init_hook": "set_action_type",
}
