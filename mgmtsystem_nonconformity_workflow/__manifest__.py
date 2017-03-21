# -*- coding: utf-8 -*-
# Copyright (C) 2017 Eugen Don (<https://www.don-systems.de>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System - Nonconformity - Workflow",
    "version": "10.0.1.0.0",
    "author": "Eugen Don - Don-Systems, Odoo Community Association (OCA)",
    "website": "http://www.don-systems.de",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_nonconformity',
    ],
    "data": [
        'views/mgmtsystem_nonconformity_workflow.xml',
        'data/workflow.xml',
    ],
    "images": [],
    "demo": [
    ],
    'installable': True,
}
