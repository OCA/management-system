# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemNonconformity(models.Model):

    _inherit = 'mgmtsystem.nonconformity'

    maintenance_request_id = fields.Many2one('maintenance.request',
                                             'Maintenance Request')
