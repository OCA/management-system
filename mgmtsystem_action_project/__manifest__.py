# Copyright 2025 Open2Bizz <info@open2bizz.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'mgmtsystem_action_project',
    'summary': 'Create a task linked to a management system action and a project',
    'version': '17.0.1.0.0',
    'category': 'Management System',
    'website': 'https://www.open2bizz.nl/',
    'author': 'Open2Bizz',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'mgmtsystem_action',
        'project',
    ],
    'data': [
        'views/project_task.xml',
        'views/mgmtsystem_action.xml',
        'views/mgmtsystem_system.xml',
        'data/data.xml',
    ]
}
