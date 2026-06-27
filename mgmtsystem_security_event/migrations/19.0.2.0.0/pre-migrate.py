# Copyright (C) 2025 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

_HAZARD_PROB_TABLE = "mgmtsystem_hazard_probability"
_HAZARD_SEV_TABLE = "mgmtsystem_hazard_severity"
_RISK_PROB_TABLE = "mgmtsystem_risk_probability"
_RISK_SEV_TABLE = "mgmtsystem_risk_severity"

_TABLES_FIELDS = {
    "mgmtsystem_security_event": [
        "severity_id",
        "original_probability_id",
        "original_severity_id",
        "current_probability_id",
        "current_severity_id",
        "residual_probability_id",
        "residual_severity_id",
    ],
    "mgmtsystem_security_vector": [
        "original_probability_id",
        "original_severity_id",
        "current_probability_id",
        "current_severity_id",
        "residual_probability_id",
        "residual_severity_id",
    ],
    "mgmtsystem_security_event_scenario": ["probability_id"],
}


def _build_id_map(cr, hazard_table, risk_table):
    openupgrade.logged_query(
        cr,
        f"""
        SELECT h.id AS old_id, r.id AS new_id
          FROM {hazard_table} h
          JOIN {risk_table} r
            ON h.value = r.value
           AND COALESCE(h.company_id, 0) = COALESCE(r.company_id, 0)
        """,
    )
    return dict(cr.fetchall())


def _ensure_risk_records(cr, hazard_table, risk_table):
    openupgrade.logged_query(
        cr,
        f"""
        INSERT INTO {risk_table} (
            company_id, name, value, description,
            create_uid, create_date, write_uid, write_date
        )
        SELECT h.company_id, h.name, h.value, h.description,
               h.create_uid, h.create_date, h.write_uid, h.write_date
          FROM {hazard_table} h
         WHERE NOT EXISTS (
               SELECT 1
                 FROM {risk_table} r
                WHERE r.value = h.value
                  AND COALESCE(r.company_id, 0) = COALESCE(h.company_id, 0)
               )
        """,
    )


def _remap_foreign_keys(cr, table, fields, id_map):
    for field in fields:
        for old_id, new_id in id_map.items():
            if old_id == new_id:
                continue
            openupgrade.logged_query(
                cr,
                f"""
                UPDATE {table}
                   SET {field} = %s
                 WHERE {field} = %s
                """,
                (new_id, old_id),
            )


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if not openupgrade.table_exists(cr, _HAZARD_PROB_TABLE):
        return
    if not openupgrade.table_exists(cr, _RISK_PROB_TABLE):
        return

    _ensure_risk_records(cr, _HAZARD_PROB_TABLE, _RISK_PROB_TABLE)
    _ensure_risk_records(cr, _HAZARD_SEV_TABLE, _RISK_SEV_TABLE)

    prob_map = _build_id_map(cr, _HAZARD_PROB_TABLE, _RISK_PROB_TABLE)
    sev_map = _build_id_map(cr, _HAZARD_SEV_TABLE, _RISK_SEV_TABLE)

    for table, fields in _TABLES_FIELDS.items():
        if not openupgrade.table_exists(cr, table):
            continue
        prob_fields = [field for field in fields if "probability" in field]
        sev_fields = [field for field in fields if "severity" in field]
        _remap_foreign_keys(cr, table, prob_fields, prob_map)
        _remap_foreign_keys(cr, table, sev_fields, sev_map)
