# -*- coding: utf-8 -*-

{
	"name": "Management System - Action - Purchase Order",
    "version": "1.0",
    "author" : "Ludovic Lelarge",
    "website": "www.eta123.be",
    'license': 'LGPL-3',
    "category": "Management System",
    'description': """
        Link Mgmtsystem Action - Purchase Order.
    """,
    'depends': ['mgmtsystem_action','purchase'],
    'data': [
        'views/mgmtsystem_action_views.xml',
        'views/purchase_views.xml'
    ],
    'installable': True,
}