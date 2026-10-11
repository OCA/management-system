from odoo import fields, models


class MgmtsystemVerificationLine(models.Model):
    """Class to manage verification's Line."""

    _name = "mgmtsystem.verification.line"
    _description = "Verification Line"
    _order = "seq"

    name = fields.Char("Question", required=True)
    audit_id = fields.Many2one("mgmtsystem.audit", ondelete="cascade", index=True)
    procedure_id = fields.Many2one("document.page", ondelete="restrict", index=True)
    is_conformed = fields.Boolean(default=False)
    comments = fields.Text()
    seq = fields.Integer("Sequence")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
