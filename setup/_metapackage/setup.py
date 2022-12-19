import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-document_page_environment_manual',
        'odoo14-addon-document_page_environmental_aspect',
        'odoo14-addon-document_page_health_safety_manual',
        'odoo14-addon-document_page_procedure',
        'odoo14-addon-document_page_quality_manual',
        'odoo14-addon-document_page_work_instruction',
        'odoo14-addon-mgmtsystem',
        'odoo14-addon-mgmtsystem_action',
        'odoo14-addon-mgmtsystem_action_efficacy',
        'odoo14-addon-mgmtsystem_action_template',
        'odoo14-addon-mgmtsystem_audit',
        'odoo14-addon-mgmtsystem_claim',
        'odoo14-addon-mgmtsystem_environment',
        'odoo14-addon-mgmtsystem_hazard',
        'odoo14-addon-mgmtsystem_hazard_risk',
        'odoo14-addon-mgmtsystem_info_security_manual',
        'odoo14-addon-mgmtsystem_manual',
        'odoo14-addon-mgmtsystem_nonconformity',
        'odoo14-addon-mgmtsystem_nonconformity_hr',
        'odoo14-addon-mgmtsystem_nonconformity_mrp',
        'odoo14-addon-mgmtsystem_nonconformity_product',
        'odoo14-addon-mgmtsystem_nonconformity_quality_control_oca',
        'odoo14-addon-mgmtsystem_nonconformity_type',
        'odoo14-addon-mgmtsystem_partner',
        'odoo14-addon-mgmtsystem_quality',
        'odoo14-addon-mgmtsystem_review',
        'odoo14-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
