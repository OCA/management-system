# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class MgmtsystemMgmTD(models.Model):
    """
    Extend stock picking with transport documentation
    """

    # extended model
    _inherit = ['stock.picking']

    # new fields
    # partner related to the movement
    # (eg. final Customer that give products to the supplier)
    related_partner_id = fields.Many2one('res.partner',
                                         'Related partner',
                                         help="Fill only if necessary.")
    # transport document number
    td = fields.Char('TD number')
    # transport document date
    td_date = fields.Date('TD date')
