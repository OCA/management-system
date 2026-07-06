from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    """
    This is a small trick. We set the parameter to False in the end-migration.py file,
    and then we set it to True here.
    This way, we can check in all dependent modules if the module existed or not.
    We will remove the parameter in the end-migration.py file of this module,
    so that it is not set to True for future migrations.
    """
    env["ir.config_parameter"].sudo().set_param(
        "migration.document_page_mgmtsystem.type", "1"
    )
