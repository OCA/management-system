from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref(
        "document_page_work_instruction.document_page_group_work_instructions"
    ).write({"mgmtsystem_page_type": "work_instruction"})
