from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref(
        "document_page_health_safety_manual.document_page_health_safety_manual"
    ).write({"mgmtsystem_page_type": "health_safety_manual"})
