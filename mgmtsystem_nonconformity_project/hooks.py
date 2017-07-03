# -*- coding: utf-8 -*-


def set_action_type(cr, registry):
    """Initialize current data in inherited modules."""
    cr.execute("""
        UPDATE mgmtsystem_action SET action_type='action'
        WHERE action_type IS null
    """)
