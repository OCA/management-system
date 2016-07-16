# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux <https://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from openerp import SUPERUSER_ID
from openerp.api import Environment


@openupgrade.migrate()
def migrate(cr, version):
    if not version:
        return

    env = Environment(cr, SUPERUSER_ID, {})
    merge_action_stages(env)


def merge_action_stages(env):
    """
    The pre-migration script copies the values from crm_claim_stage
    to mgmtsystem_action_stage.

    When the module is updated, the new stages are loaded from the
    xml data file.

    Now we want to merge the stages from crm_claim_stage with the
    stages loaded from the data.
    """
    stage_draft = env.ref('mgmtsystem_action.stage_draft')
    stage_open = env.ref('mgmtsystem_action.stage_open')
    stage_close = env.ref('mgmtsystem_action.stage_close')

    old_stage_draft_id = env.ref('crm_claim.stage_claim1').id
    old_stage_open_id = env.ref('crm_claim.stage_claim5').id
    old_stage_close_id = env.ref('crm_claim.stage_claim2').id

    env['mgmtsystem.action'].search([
        ('stage_id', '=', old_stage_draft_id)
    ]).write({'stage_id': stage_draft.id})

    env['mgmtsystem.action'].search([
        ('stage_id', '=', old_stage_open_id)
    ]).write({'stage_id': stage_open.id})

    env['mgmtsystem.action'].search([
        ('stage_id', '=', old_stage_close_id)
    ]).write({'stage_id': stage_close.id})

    env['mgmtsystem.action.stage'].browse([
        old_stage_draft_id, old_stage_open_id, old_stage_close_id
    ]).unlink()
