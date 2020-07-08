# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MgmtsystemNonconformity(models.Model):

    _inherit = 'mgmtsystem.nonconformity'

    fsm_order_id = fields.Many2one('fsm.order', 'FSM Order')
