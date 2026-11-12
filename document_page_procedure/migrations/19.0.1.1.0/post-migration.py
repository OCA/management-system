from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if (
        env["ir.config_parameter"]
        .sudo()
        .get_param("migration.document_page_mgmtsystem.type")
    ):
        return
    doc_group_id = env.ref(
        "document_page_procedure.document_page_group_procedure", False
    )
    if doc_group_id:
        doc_group_id.write({"mgmtsystem_page_type": "procedure"})
