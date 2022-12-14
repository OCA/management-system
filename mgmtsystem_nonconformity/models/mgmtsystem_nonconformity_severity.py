# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemNonconformitySeverity(models.Model):

    """Nonconformity Severity - Critical, Major, Minor, Invalid, ..."""

    _name = "mgmtsystem.nonconformity.severity"
    _description = "Severity of Complaints and Nonconformities"

    name = fields.Char("Title", required=True, translate=True)
    sequence = fields.Integer()
    description = fields.Text(translate=True)
    active = fields.Boolean("Active?", default=True)
