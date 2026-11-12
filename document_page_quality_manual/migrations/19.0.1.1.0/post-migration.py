from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if (
        env["ir.config_parameter"]
        .sudo()
        .get_param("migration.document_page_mgmtsystem.type")
    ):
        return
    env.ref("document_page_quality_manual.document_page_quality_manual").write(
        {"mgmtsystem_page_type": "quality_manual"}
    )
