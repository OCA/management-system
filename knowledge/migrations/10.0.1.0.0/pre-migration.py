# -*- coding: utf-8 -*-
# Copyright 2017 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

_xmlid_renames = [
    ('base.group_document_user', 'knowledge.group_document_user'),
]


def migrate(cr, version):
    for (old, new) in _xmlid_renames:
        query = ("UPDATE ir_model_data SET module = %s, name = %s "
                 "WHERE module = %s and name = %s")
        cr.execute(query, tuple(new.split('.') + old.split('.')))
