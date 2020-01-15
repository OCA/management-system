# Copyright (C) 2019 Open source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class MgmtSystemSystem(models.Model):
    _inherit = 'mgmtsystem.system'

    @api.model
    def get_manual_categories(self):
        res = super().get_manual_categories()
        res.update(self.env.ref(
            'document_page_quality_manual.document_page_quality_manual').id)
        return res
