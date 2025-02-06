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
    state_compliant = fields.Selection(
        [('compliant', '=', 'Compliant'), ('non_compliant', '=', 'None Compliant')],
        string="State Compliant"
    )
    external_reference = fields.Html("External Reference(s)")
    internal_reference = fields.Html("Internal Reference(s)")


    def action_open_childs(self):
        for record in self:
            return {
                "type": "ir.actions.act_window",
                "name": "Child Documents",
                "res_model": "document.page",
                "domain": [('parent_id', '=', record.id)],
                "view_mode": "tree,form",
                "target": "current",
            }
