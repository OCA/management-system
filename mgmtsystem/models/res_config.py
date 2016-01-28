# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

from openerp import models, fields


class MgmtSystemConfigSettings(models.TransientModel):
    """This class in needed to activate management system Applications."""

    _name = 'mgmtsystem.config.settings'
    _inherit = 'res.config.settings'

    module_mgmtsystem_quality = fields.Boolean(
        'Quality (ISO 9001)',
        help='Provide quality management tools.\n'
        '-This installs the module mgmtsystem_quality.'
    )

    module_mgmtsystem_environment = fields.Boolean(
        'Environment (ISO 14001)',
        help='Provide environment management tools.\n'
        '-This installs the module mgmtsystem_environment.'
    )

    module_mgmtsystem_health_safety = fields.Boolean(
        'Hygiene & Safety (OHSAS 18001)',
        help='Provide health and safety management tools.\n'
        '-This installs the module mgmtsystem_health_safety.'
    )

    module_mgmtsystem_information_security = fields.Boolean(
        'Information Security (ISO 27001)',
        help='Provide information security tools.\n'
        '-This installs the module mgmtsystem_information_security.'
    )

    module_mgmtsystem_action = fields.Boolean(
        """
    Actions (immediate, corrective, preventive) and improvement opportunities
        """,
        help='Provide actions and improvement opportunities tools.\n'
        '-This installs the module mgmtsystem_action.'
    )

    module_mgmtsystem_nonconformity = fields.Boolean(
        'Nonconformities',
        help='Provide non conformity tools.\n'
        '-This installs the module mgmtsystem_nonconformity.'
    )

    module_mgmtsystem_claim = fields.Boolean(
        'Claims',
        help='Provide claim tools.\n'
        '-This installs the module mgmtsystem_claim.'
    )

    module_mgmtsystem_audit = fields.Boolean(
        'Audits',
        help='Provide audit tools.\n'
        '-This installs the module mgmtsystem_audit.'
    )

    module_mgmtsystem_review = fields.Boolean(
        'Top management reviews',
        help='Provide review tools.\n'
        '-This installs the module mgmtsystem_review.'
    )
