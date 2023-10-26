# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)


def migrate(cr, version):
    """Set nonconformity stages from module data as noupdate."""
    cr.execute(
        """
        UPDATE ir_model_data
        SET noupdate = TRUE
        WHERE module = 'mgmtsystem_nonconformity'
        AND model = 'mgmtsystem.nonconformity.stage';
    """
    )
