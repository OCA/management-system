import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-document_page_procedure',
        'odoo12-addon-document_page_quality_manual',
        'odoo12-addon-document_page_work_instruction',
        'odoo12-addon-mgmtsystem',
        'odoo12-addon-mgmtsystem_action',
        'odoo12-addon-mgmtsystem_action_efficacy',
        'odoo12-addon-mgmtsystem_audit',
        'odoo12-addon-mgmtsystem_hazard',
        'odoo12-addon-mgmtsystem_manual',
        'odoo12-addon-mgmtsystem_nonconformity',
        'odoo12-addon-mgmtsystem_nonconformity_hr',
        'odoo12-addon-mgmtsystem_nonconformity_maintenance',
        'odoo12-addon-mgmtsystem_nonconformity_product',
        'odoo12-addon-mgmtsystem_nonconformity_project',
        'odoo12-addon-mgmtsystem_nonconformity_repair',
        'odoo12-addon-mgmtsystem_quality',
        'odoo12-addon-mgmtsystem_review',
        'odoo12-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
