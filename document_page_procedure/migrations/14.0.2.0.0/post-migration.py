from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    folder = env.ref(
        "document_page_procedure.document_page_group_procedure",
        raise_if_not_found=False,
    )
    if folder:
        procedures = (
            env["document.page"]
            .with_context(active_test=False)
            .search([("parent_id", "=", folder.id)])
        )
        procedures.write(
            {"tag_ids": [(4, env.ref("document_page_procedure.procedure_tag").id)]}
        )
