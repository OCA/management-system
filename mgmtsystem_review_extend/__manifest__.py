# -*- coding: utf-8 -*-

{
    "name": "Management System - Review - Extend",
    "version": "1.0",
    "author": "Ludovic Lelarge",
    "website": "http://www.eta123.be",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ['mgmtsystem_review', 'mgmtsystem_nonconformity', 'mgmtsystem_action'],
    "data": [
        'security/ir.model.access.csv',
        'views/mgmtsystem_review.xml',
        'views/mgmtsystem_review_type.xml',
    ],
    'installable': True,
}
