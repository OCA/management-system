import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-document_page_environment_manual>=15.0dev,<15.1dev',
        'odoo-addon-document_page_environmental_aspect>=15.0dev,<15.1dev',
        'odoo-addon-document_page_procedure>=15.0dev,<15.1dev',
        'odoo-addon-document_page_quality_manual>=15.0dev,<15.1dev',
        'odoo-addon-document_page_work_instruction>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_action>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_claim>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_hazard>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_hazard_risk>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_manual>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_nonconformity>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_nonconformity_hr>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_review>=15.0dev,<15.1dev',
        'odoo-addon-mgmtsystem_survey>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
