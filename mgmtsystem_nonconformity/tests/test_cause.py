# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from contextlib import contextmanager

from odoo import exceptions
from odoo.tests import common


class TestModelCause(common.TransactionCase):
    @contextmanager
    def assertRaisesRollback(self, *args, **kwargs):
        """Do a regular assertRaises but perform rollback at the end
        """
        with self.assertRaises(*args, **kwargs) as ar:
            yield ar
        self.cr.rollback()

    def test_create_cause(self):

        record = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "TestCause"}
        )

        self.assertNotEqual(record.id, 0)
        self.assertNotEqual(record.id, None)

    def test_name_get(self):

        record = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "TestCause"}
        )

        name_assoc = record.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause")
        self.assertEqual(name_assoc[0][0], record.id)

        record2 = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "test2", "parent_id": record.id}
        )

        name_assoc = record2.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause / test2")
        self.assertEqual(name_assoc[0][0], record2.id)

        record3 = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "test3", "parent_id": record2.id}
        )

        name_assoc = record3.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause / test2 / test3")
        self.assertEqual(name_assoc[0][0], record3.id)

    def test_recursion(self):
        parent = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "ParentCause"}
        )
        child = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "ChildCause", "parent_id": parent.id}
        )
        with self.assertRaisesRollback(exceptions.UserError):
            parent.write({"parent_id": child.id})
