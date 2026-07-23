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
        "document_page_work_instruction.document_page_group_work_instructions"
    ).write({"mgmtsystem_page_type": "work_instruction"})
