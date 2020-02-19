# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class MgmtsystemAction(models.Model):
    _name = "mgmtsystem.action"
    _inherit = ["mgmtsystem.action"]
         
    def _compute_mgmtsystem_claim_count(self):
        for mgmtsystem_action in self:
            mgmtsystem_action.mgmtsystem_claim_count = len(
                mgmtsystem_action.mgmtsystem_claim_ids
            )
    
    mgmtsystem_claim_ids = fields.Many2many(
        "mgmtsystem.claim",
        "mgmtsystem_action_mgmtsystem_claim_rel",
        "mgmtsystem_action_id",
        "mgmtsystem_claim_id",
        "Claim Ids",
    )
    mgmtsystem_claim_count = fields.Integer(
        compute="_compute_mgmtsystem_claim_count", string="Number of claim"
    )
    
class MgmtsystemClaim(models.Model):
    _name = "mgmtsystem.claim"
    _inherit = ["mgmtsystem.claim"]

    def _compute_mgmtsystem_action_count(self):
        for mgmtsystem_claim in self:
            mgmtsystem_claim.mgmtsystem_action_count = len(
                mgmtsystem_claim.mgmtsystem_action_ids
            )
    
    mgmtsystem_action_ids = fields.Many2many(
        "mgmtsystem.action",
        "mgmtsystem_action_mgmtsystem_claim_rel",
        "mgmtsystem_claim_id",
        "mgmtsystem_action_id",
        "Action Ids",
    )
    mgmtsystem_action_count = fields.Integer(
        compute="_compute_mgmtsystem_action_count", string="Number of action"
    )
    
