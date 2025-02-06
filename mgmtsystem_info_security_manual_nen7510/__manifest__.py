#    Copyright (C) 2025 Open2bizz BV www.open2bizz.nl

{
    "name": "Information Security Management System Manual NEN7510",
    "version": "17.0.1.0.0",
    "author": "Open2bizz BV",
    "website": "https://github.com/open2bizz/management-system",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
    "depends": [
        "mgmtsystem_manual",
        "mgmtsystem_nonconformity",
        "mgmtsystem_hazard_risk",
        "mgmtsystem_action",
    ],
    "data": [
        "views/document_page.xml",
        "views/document_page_chapter.xml",
        "views/mgmtsystem_risk_canvas.xml",
        "views/mgmtsystem_hazard.xml",
        "data/document_page_chapter.xml",
        "data/document_page.xml",
        'data/mgmtsystem_hazard_type.xml',
        "data/mgmtsystem_hazard_hazard.xml",
        "security/ir_model_access.xml",

    ],
    "demo": [],
    "installable": True,
}
