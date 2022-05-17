# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import exceptions
from odoo.tests import common


class TestModelCause(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.record = cls.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "TestCause"}
        )
        cls.record2 = cls.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "test2", "parent_id": cls.record.id}
        )
        cls.record3 = cls.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "test3", "parent_id": cls.record2.id}
        )

    def test_create_cause(self):
        self.assertNotEqual(self.record.id, 0)
        self.assertNotEqual(self.record.id, None)

    def test_name_get(self):
        name_assoc = self.record.name_get()
        self.assertEqual(name_assoc[0][1], "TestCause")
        self.assertEqual(name_assoc[0][0], self.record.id)

        name_assoc = self.record2.name_get()
        self.assertEqual(name_assoc[0][1], "TestCause / test2")
        self.assertEqual(name_assoc[0][0], self.record2.id)

        name_assoc = self.record3.name_get()
        self.assertEqual(name_assoc[0][1], "TestCause / test2 / test3")
        self.assertEqual(name_assoc[0][0], self.record3.id)

    def test_recursion(self):
        parent = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "ParentCause"}
        )
        child = self.env["mgmtsystem.nonconformity.cause"].create(
            {"name": "ChildCause", "parent_id": parent.id}
        )
        # no recursion
        with self.assertRaises(exceptions.UserError), self.cr.savepoint():
            parent.write({"parent_id": child.id})
