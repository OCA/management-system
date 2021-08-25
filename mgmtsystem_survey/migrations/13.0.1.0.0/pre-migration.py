# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        sql.SQL(
            """UPDATE survey_survey s
            SET state = 'management_system'
            FROM ir_model_data imd
            WHERE imd.res_id = s.{}
            AND imd.module = 'mgmtsystem_survey'
            AND imd.name = 'mgmtsystem_survey_type'"""
        ).format(sql.Identifier(openupgrade.get_legacy_name("stage_id"))),
    )
