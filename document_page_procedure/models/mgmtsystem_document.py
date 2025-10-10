# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MgmtsystemDocument(models.Model):
    _inherit = "mgmtsystem.document"

    kind = fields.Selection(
        selection_add=[("procedure", "Procedure")],
        ondelete={"procedure": "set null"},
    )
    document_page_id = fields.Many2one(
        "document.page",
    )

    def _get_document_page_vals(self):
        result = super()._get_document_page_vals()
        if self.kind == "procedure":
            parent = self.env.ref(
                "document_page_procedure.document_page_group_procedure",
                raise_if_not_found=False,
            )
            result.update({"parent_id": parent and parent.id})
        return result

    @api.depends("document_page_id.name")
    def _compute_name(self):
        return super()._compute_name()

    def _get_document_context(self):
        result = super()._get_document_context()
        if self.kind == "procedure":
            parent = self.env.ref(
                "document_page_procedure.document_page_group_procedure",
                raise_if_not_found=False,
            )
            result.update(
                {
                    "_mgmtsystem_procedure_generate": True,
                    "default_parent_id": parent and parent.id,
                }
            )
        return result
