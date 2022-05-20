# Copyright 2020 Creu Blanca
# Copyright 2019 Marcelo Frare (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)
# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)

from odoo import fields, models


class MgmtsystemActionTemplate(models.Model):
    """
    Define a support structure to set action template values
    """

    _name = "mgmtsystem.action.template"
    _description = "Define fields to save action template values"

    def _selection_type_action(self):
        # link to action type values
        return self.env["mgmtsystem.action"]._fields["type_action"].selection

    # fields
    # template identification
    name = fields.Char(required=True)
    # action preset
    description = fields.Html()
    type_action = fields.Selection(
        selection=lambda self: self._selection_type_action(), string="Response Type"
    )
    user_id = fields.Many2one(
        "res.users",
        "Responsible",
        default=lambda self: self.env["mgmtsystem.action"]._default_owner(),
        required=True,
    )
    tag_ids = fields.Many2many("mgmtsystem.action.tag", string="Tags")
