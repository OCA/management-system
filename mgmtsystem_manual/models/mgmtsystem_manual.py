
from odoo import models, fields


class MgmtSystemManual(models.Model):

    _inherit = 'mgmtsystem.system'
    _description = 'Manual'
    manual_id = fields.Many2one('document.page', string='Manual',
                                oldname='manual')
