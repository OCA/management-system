# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemMgmMRP(models.Model):
    """
    Extend nonconformity adding fields for workcenter
    """

    _inherit = ["mgmtsystem.nonconformity"]

    # new fields
    # workcenter reference
    workcenter_id = fields.Many2one("mrp.workcenter", "Workcenter")
