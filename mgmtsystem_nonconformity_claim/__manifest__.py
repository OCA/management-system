# -*- coding: utf-8 -*-

{
    "name": "Management System - Non Conformity - Claim",
    "version": "1.0",
    "author" : "Ludovic Lelarge",
    "website": "www.eta123.be",
    'license': 'LGPL-3',
    "category": "Management System",
    'description': """
        Link Mgmtsystem Non Conformity - Claim.
    """,
    'depends': ['mgmtsystem_nonconformity','mgmtsystem_claim'],
    'data': [
        'views/mgmtsystem_nonconformity.xml',
        'views/mgmtsystem_claim.xml'
    ],
    'installable': True,
}
