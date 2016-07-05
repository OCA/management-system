# -*- coding: utf-8 -*-

from openerp import models, fields


class MgmtsystemNonconformityState(models.Model):
    """This object is used to defined different state for non conformity."""

    _name = 'mgmtsystem.nonconformity.state'
    _description = "nonconformity states"
    _order = 'sequence'

    name = fields.Char('State Name', required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Used to order states. Lower is better.", default=100)
