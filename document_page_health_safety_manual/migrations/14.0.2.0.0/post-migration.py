from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    folder = env.ref(
        "document_page_health_safety_manual.document_page_health_safety_manual",
        raise_if_not_found=False,
    )
    if folder:
        documents = (
            env["document.page"]
            .with_context(active_test=False)
            .search([("parent_id", "=", folder.id)])
        )
        documents.write(
            {
                "tag_ids": [
                    (
                        4,
                        env.ref(
                            "document_page_health_safety_manual.health_safety_manual_tag"
                        ).id,
                    )
                ]
            }
        )
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE ir_model_data
            SET res_id=0
            WHERE module='document_page_health_safety_manual'
            AND name='document_page_health_safety_manual'
        """,
        )  # We want to avoid deletion of the page, but we want to delete the ir.model.data
