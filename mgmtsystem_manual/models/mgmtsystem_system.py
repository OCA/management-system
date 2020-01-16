# Copyright (C) 2019 Open source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models, fields


class MgmtSystemSystem(models.Model):
    _inherit = 'mgmtsystem.system'

    def get_manual_categories(self):
        """ Returns a list of category ids """
        return [self.env.ref('mgmtsystem_manual.manuals').id]

    @api.model
    def get_manual_domain(self):
        return [('parent_id', 'in', self.get_manual_categories()),
                ('type', '=', 'page')]

    manual_id = fields.Many2one('document.page', 'Manual',
                                oldname='manual',
                                domain=get_manual_domain)
