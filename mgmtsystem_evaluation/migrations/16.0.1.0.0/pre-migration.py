from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.add_fields(
        env,
        [
            (
                "model_id",
                "mgmtsystem.evaluation",
                "mgmtsystem_evaluation",
                "many2one",
                None,
                "mgmtsystem_evaluation",
                None,
            ),
        ],
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE mgmtsystem_evaluation me
        SET model_id = met.model_id
        FROM mgmtsystem_evaluation_template met
        WHERE me.template_id = met.id
        """,
    )
