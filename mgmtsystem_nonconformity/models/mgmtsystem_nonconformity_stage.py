# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, _


_STATES = [
    ('draft', _('Draft')),
    ('analysis', _('Analysis')),
    ('pending', _('Action Plan')),
    ('open', _('In Progress')),
    ('done', _('Closed')),
    ('cancel', _('Cancelled')),
]


class MgmtsystemNonconformityStage(models.Model):
    """This object is used to defined different state for non conformity."""
    _name = 'mgmtsystem.nonconformity.stage'
    _description = "Nonconformity Stages"
    _order = 'sequence'

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Used to order states. Lower is better.", default=100)
    state = fields.Selection(
        _STATES,
        'State',
        readonly=True,
        default="draft",
    )
