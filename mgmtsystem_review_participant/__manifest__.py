# -*- coding: utf-8 -*-

{
    "name": "Management System - Review - Participant",
    "version": "1.0",
    "author": "Ludovic Lelarge",
    "website": "http://www.eta123.be",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": ['mgmtsystem_review','hr'],
    "data": [
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/mgmtsystem_review_email.xml',
        'views/mgmtsystem_review_participant.xml',
    ],
    'installable': True,
}
