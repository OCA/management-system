from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref("document_page_environment_manual.document_page_environment_manual").write(
        {"mgmtsystem_page_type": "environment_manual"}
    )
