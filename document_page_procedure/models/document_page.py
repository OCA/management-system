# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    mgmtsystem_document_procedure_ids = fields.One2many(
        "mgmtsystem.document",
        "document_page_id",
        domain=[("kind", "=", "procedure")],
    )

    def toggle_active(self):
        to_activate = self.filtered(lambda p: not p.active)
        to_deactivate = self.filtered(lambda p: p.active)
        for pages, expected in [(to_activate, False), (to_deactivate, True)]:
            if pages:
                self.env["mgmtsystem.document"].search(
                    [
                        ("kind", "=", "procedure"),
                        ("document_page_id", "in", pages.ids),
                        ("active", "=", expected),
                    ]
                ).toggle_active()
        return super().toggle_active()

    def toggle_procedure(self):
        self.ensure_one()
        if not self.active:
            # If the page is archived, we do nothing.
            return
        document = (
            self.env["mgmtsystem.document"]
            .with_context(active_test=False)
            .search([("kind", "=", "procedure"), ("document_page_id", "in", self.ids)])
        )
        if document:
            document.toggle_active()
        else:
            self.env["mgmtsystem.document"].create(
                {
                    "name": self.name,
                    "kind": "procedure",
                    "document_type": "document",
                    "document_page_id": self.id,
                }
            )

    @api.model_create_multi
    def create(self, mvals):
        result = super().create(mvals)
        if self.env.context.get("_mgmtsystem_procedure_generate"):
            for record in result:
                record.toggle_procedure()
        return result
