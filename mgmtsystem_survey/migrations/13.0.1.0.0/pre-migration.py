# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE survey_survey s
        SET state = 'management_system'
        FROM ir_model_data imd
        WHERE imd.res_id = s.stage_id
            AND imd.module = 'mgmtsystem_survey'
            AND imd.name = 'mgmtsystem_survey_type'
        """,
    )
