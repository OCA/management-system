# -*- coding: utf-8 -*-

{
    "name": "Mgmt System Action - Partner",
    "version": "1.0",
    "author" : "Ludovic Lelarge",
    "website": "www.eta123.be",
    'license': 'LGPL-3',
    'category': 'Management System',
    'description': """
        Add partner to Mgmtsystem_action Form.
    """,
    'depends': ['mgmtsystem_action'],
    'data': [
        'views/mgmtsystem_action_views.xml',
    ],
    'installable': True,
}