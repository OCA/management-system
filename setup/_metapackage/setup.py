import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-document_page_procedure',
        'odoo11-addon-document_page_quality_manual',
        'odoo11-addon-document_page_work_instruction',
        'odoo11-addon-mgmtsystem',
        'odoo11-addon-mgmtsystem_action',
        'odoo11-addon-mgmtsystem_audit',
        'odoo11-addon-mgmtsystem_manual',
        'odoo11-addon-mgmtsystem_nonconformity',
        'odoo11-addon-mgmtsystem_nonconformity_hr',
        'odoo11-addon-mgmtsystem_quality',
        'odoo11-addon-mgmtsystem_review',
        'odoo11-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
