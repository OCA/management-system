import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-document_page_environment_manual',
        'odoo8-addon-document_page_environmental_aspect',
        'odoo8-addon-document_page_health_safety_manual',
        'odoo8-addon-document_page_procedure',
        'odoo8-addon-document_page_quality_manual',
        'odoo8-addon-document_page_work_instructions',
        'odoo8-addon-information_security_manual',
        'odoo8-addon-mgmtsystem',
        'odoo8-addon-mgmtsystem_action',
        'odoo8-addon-mgmtsystem_audit',
        'odoo8-addon-mgmtsystem_claim',
        'odoo8-addon-mgmtsystem_environment',
        'odoo8-addon-mgmtsystem_hazard',
        'odoo8-addon-mgmtsystem_hazard_risk',
        'odoo8-addon-mgmtsystem_health_safety',
        'odoo8-addon-mgmtsystem_manuals',
        'odoo8-addon-mgmtsystem_nonconformity',
        'odoo8-addon-mgmtsystem_nonconformity_analytic',
        'odoo8-addon-mgmtsystem_nonconformity_claim',
        'odoo8-addon-mgmtsystem_nonconformity_project',
        'odoo8-addon-mgmtsystem_quality',
        'odoo8-addon-mgmtsystem_review',
        'odoo8-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
