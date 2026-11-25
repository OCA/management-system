from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env["ir.config_parameter"].sudo().set_param(
        "migration.document_page_mgmtsystem.type", False
    )
