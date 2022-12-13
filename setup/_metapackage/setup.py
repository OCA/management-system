import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-document_page_environment_manual>=16.0dev,<16.1dev',
        'odoo-addon-document_page_environmental_aspect>=16.0dev,<16.1dev',
        'odoo-addon-document_page_work_instruction>=16.0dev,<16.1dev',
        'odoo-addon-mgmtsystem>=16.0dev,<16.1dev',
        'odoo-addon-mgmtsystem_action>=16.0dev,<16.1dev',
        'odoo-addon-mgmtsystem_manual>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
