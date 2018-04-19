import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-document_page_procedure',
        'odoo10-addon-document_page_quality_manual',
        'odoo10-addon-document_page_work_instruction',
        'odoo10-addon-mgmtsystem',
        'odoo10-addon-mgmtsystem_action',
        'odoo10-addon-mgmtsystem_audit',
        'odoo10-addon-mgmtsystem_manual',
        'odoo10-addon-mgmtsystem_nonconformity',
        'odoo10-addon-mgmtsystem_quality',
        'odoo10-addon-mgmtsystem_review',
        'odoo10-addon-mgmtsystem_survey',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
