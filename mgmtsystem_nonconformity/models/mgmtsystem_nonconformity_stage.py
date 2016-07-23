# -*- coding: utf-8 -*-

from openerp import models, fields


class MgmtsystemNonconformityStage(models.Model):
    """This object is used to defined different stage for non conformity."""

    _name = 'mgmtsystem.nonconformity.stage'
    _description = "nonconformity stages"
    _order = 'sequence'

    name = fields.Char('Stage Name', required=True, translate=True)
    sequence = fields.Integer(
        'Sequence', help="Used to order stages. Lower is better.", default=100)
