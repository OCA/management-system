# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestModelOrigin(common.TransactionCase):
    def test_create_origin(self):

        record = self.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "TestOrigin"}
        )

        self.assertNotEqual(record.id, 0)
        self.assertNotEqual(record.id, None)

    def test_name_get(self):

        record = self.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "TestOrigin"}
        )

        name_assoc = record.name_get()

        self.assertEqual(name_assoc[0][1], "TestOrigin")
        self.assertEqual(name_assoc[0][0], record.id)

        record2 = self.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "test2", "parent_id": record.id}
        )

        name_assoc = record2.name_get()

        self.assertEqual(name_assoc[0][1], "TestOrigin / test2")
        self.assertEqual(name_assoc[0][0], record2.id)

        record3 = self.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "test3", "parent_id": record2.id}
        )

        name_assoc = record3.name_get()

        self.assertEqual(name_assoc[0][1], "TestOrigin / test2 / test3")
        self.assertEqual(name_assoc[0][0], record3.id)
