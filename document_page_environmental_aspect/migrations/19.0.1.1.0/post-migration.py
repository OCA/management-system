from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if (
        env["ir.config_parameter"]
        .sudo()
        .get_param("migration.document_page_mgmtsystem.type")
    ):
        return
    env.ref(
        "document_page_environmental_aspect.document_page_environmental_aspect"
    ).write({"mgmtsystem_page_type": "environmental_aspect"})
