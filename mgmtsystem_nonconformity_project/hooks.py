# -*- coding: utf-8 -*-
# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def set_action_type(cr, registry):
    """Initialize current data in inherited modules."""
    cr.execute("""
        UPDATE mgmtsystem_action SET action_type='action'
        WHERE action_type IS null
    """)
