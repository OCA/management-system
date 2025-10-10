# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MgmtsystemDocument(models.Model):
    _name = "mgmtsystem.document"
    _description = "Mgmtsystem Document"  # TODO

    name = fields.Char(
        required=True, compute="_compute_name", store=True, readonly=False
    )
    document_type = fields.Selection(
        selection=lambda self: self._get_document_type_selection(),
        required=True,
        readonly=True,
    )
    kind = fields.Selection(
        selection=[],
    )
    link = fields.Char()
    system_id = fields.Many2one(
        "mgmtsystem.system",
    )
    active = fields.Boolean(default=True)

    @api.model
    def _get_document_types(self):
        result = [
            {
                "id": "link",
                "label": _("Link"),
                "add_label": _("Add Link"),
                "sequence": 10,
            }
        ]
        if "document.page" in self.env and "document_page_id" in self._fields:
            # We should show them only in some specific cases.
            result.append(
                {
                    "id": "document",
                    "label": _("Page"),
                    "sequence": 5,
                    "add_label": _("Add Page"),
                }
            )
        return result

    @api.model
    def get_document_types(self):
        return sorted(self._get_document_types(), key=lambda d: d.get("sequence", 100))

    @api.model
    def _get_document_type_selection(self):
        return [
            (doc_type["id"], doc_type["label"])
            for doc_type in self._get_document_types()
        ]

    @api.depends()
    def _compute_name(self):
        """This is a hook to be used with document pages"""
        for record in self:
            if record.document_type == "document":
                record.name = (
                    record.document_page_id.name
                    if record.document_page_id
                    else _("(No Page)")
                )

    @api.model
    def add_element(self, element_type):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "mgmtsystem.mgmtsystem_document_act_window_new"
        )
        action["context"] = self.with_context(
            default_document_type=element_type
        ).env.context.copy()
        return action

    def _get_document_page_vals(self):
        return {"name": self.name, "content": self.name}

    def action_create(self):
        if self.document_type == "document":
            page = self.env["document.page"].create(self._get_document_page_vals())
            # This field is not defined yet, but we expect it to be there.
            self.document_page_id = page
        return self.get_formview_action()

    def get_formview_action(self, access_uid=None):
        if self.document_type == "document":
            return self.document_page_id.with_context(
                **self._get_document_context()
            ).get_formview_action(access_uid=access_uid)
        return super().get_formview_action(access_uid=access_uid)

    def _get_document_context(self):
        return {}
