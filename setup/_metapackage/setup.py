import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-document_page_procedure',
        'odoo14-addon-document_page_quality_manual',
        'odoo14-addon-mgmtsystem',
        'odoo14-addon-mgmtsystem_action',
        'odoo14-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
