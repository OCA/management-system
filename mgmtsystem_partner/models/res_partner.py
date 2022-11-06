# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    """
    Extend res.partner with contact info for communications on quality
    """

    _inherit = ["res.partner"]

    # type for manage quality contact
    type = fields.Selection(selection_add=[("quality", "Quality Address")])
