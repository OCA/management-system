# -*- coding: utf-8 -*-

{
	"name": "Management System - Action - Claim",
    "version": "13.0.1.0.0",
    "author" : "Ludovic Lelarge, Odoo Community Association (OCA)",
    "website": "www.eta123.be",
    'license': 'LGPL-3',
    "category": "Management System",
    'depends': ['mgmtsystem_action','mgmtsystem_claim'],
    'data': [
        'views/mgmtsystem_action_views.xml',
        'views/mgmtsystem_claim_views.xml'
    ],
    'installable': True,
}
