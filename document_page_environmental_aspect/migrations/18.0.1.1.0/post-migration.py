from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.ref(
        "document_page_environmental_aspect.document_page_environmental_aspect"
    ).write({"mgmtsystem_page_type": "environmental_aspect"})
