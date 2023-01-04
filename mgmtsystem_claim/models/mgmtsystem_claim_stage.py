##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 - present Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
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
from odoo import fields, models


class MgmtsystemClaimStage(models.Model):
    _name = "mgmtsystem.claim.stage"
    _description = "Claim stages for Management system"
    _inherit = "crm.claim.stage"
    _order = "sequence"

    team_ids = fields.Many2many(
        comodel_name="crm.team",
        relation="crm_team_mgmtsystem_claim_stage_rel",
        column1="stage_id",
        column2="team_id",
        string="Teams",
        help="Link between stages and sales teams. When set, this limitate "
        "the current stage to the selected sales teams.",
    )
