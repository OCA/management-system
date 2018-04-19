import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-document_page_environment_manual',
        'odoo9-addon-document_page_environmental_aspect',
        'odoo9-addon-document_page_health_safety_manual',
        'odoo9-addon-document_page_procedure',
        'odoo9-addon-document_page_quality_manual',
        'odoo9-addon-document_page_work_instruction',
        'odoo9-addon-mgmtsystem',
        'odoo9-addon-mgmtsystem_action',
        'odoo9-addon-mgmtsystem_audit',
        'odoo9-addon-mgmtsystem_claim',
        'odoo9-addon-mgmtsystem_hazard',
        'odoo9-addon-mgmtsystem_info_security_manual',
        'odoo9-addon-mgmtsystem_kpi',
        'odoo9-addon-mgmtsystem_manual',
        'odoo9-addon-mgmtsystem_nonconformity',
        'odoo9-addon-mgmtsystem_probability',
        'odoo9-addon-mgmtsystem_quality',
        'odoo9-addon-mgmtsystem_review',
        'odoo9-addon-mgmtsystem_severity',
        'odoo9-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
