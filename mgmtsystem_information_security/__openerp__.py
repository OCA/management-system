# -*- coding: utf-8 -*-
{
    'name': 'Information Security Management System',
    'summary': 'Manage your ISMS',
    'version': '9.0.1.0.0',
    'author': 'Savoir-faire Linux, Odoo Community Association (OCA)',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Management System',
    'depends': [
        'mgmtsystem_security_event',
        'information_security_manual',
        'mgmtsystem_audit',
        'mgmtsystem_review',
    ],
    'data': [
        'data/system.xml',
        'views/mgmtsystem_action.xml',
    ],
    'demo': [
    ],
    'js': [],
    'css': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
