# -*- coding: utf-8 -*-
# Copyright 2019 Alexandre Fayolle <alexandre.fayolle@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def migrate(env, version):
    """Update database from previous versions, after updating module."""
    env['mgmtsystem.nonconformity.cause']._parent_store_compute()
    env['mgmtsystem.nonconformity.origin']._parent_store_compute()
