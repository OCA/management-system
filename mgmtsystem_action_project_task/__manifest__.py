# -*- coding: utf-8 -*-

{
	"name": "Management System - Action - Project Task",
    "version": "1.0",
    "author" : "Ludovic Lelarge",
    "website": "www.eta123.be",
    'license': 'LGPL-3',
    "category": "Management System",
    'description': """
        Link Mgmtsystem Action - Project Task.
    """,
    'depends': ['mgmtsystem_action','project'],
    'data': [
        'views/mgmtsystem_action_views.xml',
        'views/project_views.xml'
    ],
    'installable': True,
}