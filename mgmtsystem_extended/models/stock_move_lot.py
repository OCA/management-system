# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class MgmtsystemMgmLotReference(models.Model):
    """
    Extend stock move with lot reference
    """

    # extended model
    _inherit = ['stock.move']

    # new field
    # lot reference
    lot_reference = fields.Char('Lot reference')

    @api.onchange('lot_reference')
    def onchange_lot_reference(self):
        """
        change lot_reference on qc_inspection
        """

        if self.lot_reference:
            # create origin key as 'name,id'
            origin_key = self._origin._name + ',' + str(self._origin.id)

            # get inspection object
            qc_inspection = self.env['qc.inspection'
                                     ].search([('object_id', '=', origin_key)],
                                              limit=1
                                              )

            # if exist inspection set the lot_reference value
            if qc_inspection:
                qc_inspection.sudo().write({'lot_reference': self.lot_reference})
