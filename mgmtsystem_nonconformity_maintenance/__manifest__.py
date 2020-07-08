# Copyright 2020 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mgmtsystem Nonconformity Maintenance',
    'summary': """
        Bridge module between Maintenance and Non Conformities""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/management-system',
    'depends': [
        'mgmtsystem_nonconformity',
        'maintenance',
    ],
    'data': [
        'views/mgmtsystem_nonconformity.xml',
    ],
    'demo': [
    ],
}
