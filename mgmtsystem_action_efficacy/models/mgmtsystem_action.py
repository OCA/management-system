# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MgmtsystemAction(models.Model):
    """
    Extend actions adding fields for record efficacy informations with changes tracking
    """

    _inherit = "mgmtsystem.action"

    # new fileds
    # value of efficacy
    efficacy_value = fields.Integer(
        "Rating",
        help="0:not effective | 50:efficacy not complete | 100: effective",
        tracking=True,
    )
    # user in charge of evaluation
    efficacy_user_id = fields.Many2one(
        "res.users",
        "Inspector",
        tracking=True,
    )
    # notes on the efficacy
    efficacy_description = fields.Text("Notes")

    @api.onchange("efficacy_value")
    def _onchange_efficacy_value(self):
        if self.efficacy_value < 0 or self.efficacy_value > 100:
            raise ValidationError(_("Rating must be between 0 and 100"))
        return
