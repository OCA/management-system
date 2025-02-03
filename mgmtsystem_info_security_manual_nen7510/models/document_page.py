#    Copyright (C) 2025 Open2bizz BV www.open2bizz.nl

from odoo import fields, models

class DocumentPage(models.Model):
    """
    Extend Document Page with info for Procedure NEN7510
    """

    _inherit = ["document.page"]

    nen_chapter = fields.Many2one("document.page.chapter", "NEN Chapter")
    nen_control = fields.Char("NEN Control")
    nen_mandatory = fields.Boolean("Mandatory")
    external_reference = fields.Char("External Reference(s)")
    internal_reference = fields.Char("Internal Reference(s)")


