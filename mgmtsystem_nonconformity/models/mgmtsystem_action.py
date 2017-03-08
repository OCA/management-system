# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from lxml import etree
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
import re
import logging
import pdb
_logger = logging.getLogger(__name__)


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    @api.model
    def default_get(self, field_list):
        """ Set 'date_assign' if user_id is set. """
        result = super(MgmtsystemAction, self).default_get(field_list)
        if 'user_id' in result:
            result['date_assign'] = fields.Datetime.now()
        return result

    nonconformity_immediate_id = fields.One2many(
        'mgmtsystem.nonconformity',
        'immediate_action_id',
        readonly=True,
    )
    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity',
        'mgmtsystem_nonconformity_action_rel',
        'action_id',
        'nonconformity_id',
        'Nonconformities',
        readonly=True,
    )
