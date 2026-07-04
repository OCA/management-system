from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref("document_page_procedure.document_page_procedure").write(
        {"mgmtsystem_page_type": "procedure"}
    )
