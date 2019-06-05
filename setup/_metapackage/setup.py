import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-management-system",
    description="Meta package for oca-management-system Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-mgmtsystem',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
