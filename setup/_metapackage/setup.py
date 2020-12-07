import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-document_page_environment_manual',
        'odoo13-addon-document_page_environmental_aspect',
        'odoo13-addon-document_page_health_safety_manual',
        'odoo13-addon-document_page_procedure',
        'odoo13-addon-document_page_quality_manual',
        'odoo13-addon-document_page_work_instruction',
        'odoo13-addon-mgmtsystem',
        'odoo13-addon-mgmtsystem_action',
        'odoo13-addon-mgmtsystem_audit',
        'odoo13-addon-mgmtsystem_claim',
        'odoo13-addon-mgmtsystem_hazard',
        'odoo13-addon-mgmtsystem_hazard_risk',
        'odoo13-addon-mgmtsystem_info_security_manual',
        'odoo13-addon-mgmtsystem_manual',
        'odoo13-addon-mgmtsystem_nonconformity',
        'odoo13-addon-mgmtsystem_nonconformity_hr',
        'odoo13-addon-mgmtsystem_quality',
        'odoo13-addon-mgmtsystem_review',
        'odoo13-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
