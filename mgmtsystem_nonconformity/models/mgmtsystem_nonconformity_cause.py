# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _


class MgmtsystemNonconformityCause(models.Model):

    """Cause of the nonconformity of the management system."""

    _name = "mgmtsystem.nonconformity.cause"
    _description = "Cause of the nonconformity of the management system"
    _order = 'parent_id, sequence'
    _parent_store = True

    name = fields.Char('Cause', required=True, translate=True)
    description = fields.Text('Description')
    sequence = fields.Integer(
        'Sequence',
        help="Defines the order to present items",
    )
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    parent_id = fields.Many2one(
        'mgmtsystem.nonconformity.cause',
        'Group',
        ondelete='restrict'
    )
    child_ids = fields.One2many(
        'mgmtsystem.nonconformity.cause',
        'parent_id',
        'Child Causes',
    )
    ref_code = fields.Char('Reference Code')

    @api.multi
    def name_get(self):
        res = []
        for obj in self:
            name = obj.name
            if obj.parent_id:
                name = obj.parent_id.name_get()[0][1] + ' / ' + name
            res.append((obj.id, name))
        return res

    @api.constrains("parent_id")
    def _check_recursion(self):
        if not super(MgmtsystemNonconformityCause, self)._check_recursion():
            raise exceptions.ValidationError(
                _("Error! Cannot create recursive cycle.")
            )
