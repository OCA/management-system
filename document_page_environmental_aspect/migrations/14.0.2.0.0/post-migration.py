from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    folder = env.ref(
        "document_page_environment_aspect.document_page_group_environmental_aspect",
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
                            "document_page_environment_aspect.environment_aspect_tag"
                        ).id,
                    )
                ]
            }
        )
