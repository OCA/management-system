# Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemConfigSettings(models.TransientModel):
    """This class is used to activate management system Applications."""

    _inherit = "res.config.settings"

    # Systems
    module_mgmtsystem_quality = fields.Boolean(
        "Quality Tools",
        help="Provide quality management tools.\n"
        "- This installs the module mgmtsystem_quality.",
    )
    module_mgmtsystem_environment = fields.Boolean(
        "Environment",
        help="Provide environment management tools.\n"
        "- This installs the module mgmtsystem_environment.",
    )
    module_mgmtsystem_health_safety = fields.Boolean(
        "Hygiene & Safety",
        help="Provide health and safety management tools.\n"
        "- This installs the module mgmtsystem_health_safety.",
    )
    module_mgmtsystem_information_security = fields.Boolean(
        "Information Security",
        help="Provide information security tools.\n"
        "- This installs the module mgmtsystem_information_security.",
    )

    # Applications
    module_mgmtsystem_action = fields.Boolean(
        "Actions",
        help="Provide actions and improvement opportunities tools.\n"
        "- This installs the module mgmtsystem_action.",
    )
    module_mgmtsystem_nonconformity = fields.Boolean(
        "Nonconformities",
        help="Provide non conformity tools.\n"
        "- This installs the module mgmtsystem_nonconformity.",
    )
    module_mgmtsystem_claim = fields.Boolean(
        "Claims",
        help="Provide claim tools.\n" "- This installs the module mgmtsystem_claim.",
    )
    module_mgmtsystem_audit = fields.Boolean(
        "Audits",
        help="Provide audit tools.\n" "- This installs the module mgmtsystem_audit.",
    )
    module_mgmtsystem_review = fields.Boolean(
        "Reviews",
        help="Provide review tools.\n" "- This installs the module mgmtsystem_review.",
    )

    # Manuals
    module_document_page_quality_manual = fields.Boolean(
        "Quality Manual Template",
        help="Provide a quality manual template.\n"
        "- This installs the module document_page_quality_manual.",
    )
    module_document_page_environment_manual = fields.Boolean(
        "Environment Manual Template",
        help="Provide an environment manual template.\n"
        "- This installs the module mgmtsystem_environment_manual.",
    )
    module_mgmtsystem_health_safety_manual = fields.Boolean(
        "Health & Safety Manual Template",
        help="Provide a health and safety manual template.\n"
        "- This installs the module mgmtsystem_health_safety_manual.",
    )
    module_information_security_manual = fields.Boolean(
        "Information Security Manual Template",
        help="Provide an information security manual.\n"
        "- This installs the module information_security_manual.",
    )

    # Documentation
    module_document_page_procedure = fields.Boolean(
        "Procedures",
        help="Provide procedures category.\n"
        "- This installs the module document_page_procedure.",
    )
    module_document_page_environmental_aspect = fields.Boolean(
        "Environmental Aspects",
        help="Provide Environmental Aspect category.\n"
        "- This installs the module mgmtsystem_environmental_aspect.",
    )
    module_mgmtsystem_hazard = fields.Boolean(
        "Hazards",
        help="Provide Hazards.\n" "- This installs the module mgmtsystem_hazard.",
    )
    module_mgmtsystem_security_event = fields.Boolean(
        "Feared Events",
        help="Provide Feared Events.\n"
        "- This installs the module mgmtsystem_security_event.",
    )
    module_document_page_approval = fields.Boolean(
        "Document Page Approval",
        help="Provide document approval and history. \n"
        "- This installs the module document_page_approval.",
    )
    module_document_page_work_instruction = fields.Boolean(
        "Work Instructions",
        help="Provide Work Instructions category.\n"
        "- This installs the module document_page_work_instruction.",
    )
