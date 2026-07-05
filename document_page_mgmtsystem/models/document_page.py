# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    mgmtsystem_page_type = fields.Selection(
        selection=[],
        string="Management System Page Type",
        help="Classification of the management system document page.",
        compute="_compute_mgmtsystem_page_type",
        store=True,
        recursive=True,
        readonly=False,
    )

    @api.depends("parent_id.mgmtsystem_page_type")
    def _compute_mgmtsystem_page_type(self):
        for record in self:
            mgmtsystem_page_type = record.parent_id.mgmtsystem_page_type
            if record.type == "category" and not mgmtsystem_page_type:
                mgmtsystem_page_type = record.mgmtsystem_page_type
            record.mgmtsystem_page_type = mgmtsystem_page_type
