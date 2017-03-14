# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MgmtsystemNonconformitySeverity(models.Model):

    """Nonconformity Severity - Critical, Major, Minor, Invalid, ..."""

    _name = "mgmtsystem.nonconformity.severity"
    _description = "Severity of Complaints and Nonconformities"

    name = fields.Char("Title", required=True, translate=True)
    sequence = fields.Integer('Sequence')
    description = fields.Text('Description', translate=True)
    active = fields.Boolean('Active?', default=True)
