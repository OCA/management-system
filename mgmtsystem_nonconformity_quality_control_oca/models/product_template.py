from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    create_nonconformity = fields.Boolean(
        string="Create Non-Conformity",
        help="If selected, automatically creates Nonconformity when inspections fail",
    )
