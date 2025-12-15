from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref("document_page_quality_manual.document_page_quality_manual").write(
        {"mgmtsystem_page_type": "quality_manual"}
    )
