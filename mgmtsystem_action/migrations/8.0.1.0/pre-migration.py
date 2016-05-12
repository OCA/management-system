# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux <https://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(cr, version):
    if not version:
        return

    copy_crm_claim_stage(cr)


def copy_crm_claim_stage(cr):
    """
    Copy the whole table crm_claim_stage to mgmtsystem_action_stage

    In 7.0, mgmtsystem_action.stage_id was pointing to crm_claim_stage
    In 8.0, it points to mgmtsystem_action_stage which is a table
    inherited from crm_claim_stage.
    """
    openupgrade.logged_query(
        cr,
        """
        CREATE TABLE mgmtsystem_action_stage (
            LIKE crm_claim_stage
            INCLUDING ALL
        );
        """)

    cr.execute(
        """
        select nextval('crm_claim_stage_id_seq')
        """
    )

    sequence_num = cr.fetchall()[0][0]

    openupgrade.logged_query(
        cr,
        """
        CREATE SEQUENCE mgmtsystem_action_stage_id_seq
            INCREMENT 1
            MINVALUE 1
            MAXVALUE 9223372036854775807
            START %s
            CACHE 1;
        """, (sequence_num,)
    )

    openupgrade.logged_query(
        cr,
        """
        INSERT INTO mgmtsystem_action_stage
        SELECT * FROM crm_claim_stage
        """
    )

    cr.execute(
        "ALTER TABLE mgmtsystem_action "
        "DROP CONSTRAINT IF EXISTS mgmtsystem_action_stage_id_fkey")

    cr.execute(
        "ALTER TABLE mgmtsystem_action "
        "DROP CONSTRAINT IF EXISTS mgmtsystem_action_stage_id_fkey1")
