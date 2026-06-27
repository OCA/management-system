# Copyright (C) 2025 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_model_renames = [
    ("mgmtsystem.hazard.probability", "mgmtsystem.risk.probability"),
    ("mgmtsystem.hazard.severity", "mgmtsystem.risk.severity"),
]

_table_renames = [
    ("mgmtsystem_hazard_probability", "mgmtsystem_risk_probability"),
    ("mgmtsystem_hazard_severity", "mgmtsystem_risk_severity"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_models(env.cr, _model_renames)
    openupgrade.rename_tables(env.cr, _table_renames)
