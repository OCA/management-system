# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DocumentPage(models.Model):
    _inherit = "document.page"

    mgmtsystem_page_type = fields.Selection(
        selection_add=[("environment_manual", "Environmental Manual")],
    )
