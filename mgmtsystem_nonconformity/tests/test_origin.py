# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestModelOrigin(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.record = cls.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "TestOrigin"}
        )
        cls.record2 = cls.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "test2", "parent_id": cls.record.id}
        )
        cls.record3 = cls.env["mgmtsystem.nonconformity.origin"].create(
            {"name": "test3", "parent_id": cls.record2.id}
        )

    def test_create_origin(self):
        self.assertNotEqual(self.record.id, 0)
        self.assertNotEqual(self.record.id, None)

    def test_display_name(self):
        name_assoc = self.record
        name_assoc._compute_display_name()
        self.assertEqual(name_assoc.display_name, "TestOrigin")
        self.assertEqual(name_assoc.id, self.record.id)

        name_assoc = self.record2
        name_assoc._compute_display_name()
        self.assertEqual(name_assoc.display_name, "TestOrigin / test2")
        self.assertEqual(name_assoc.id, self.record2.id)

        name_assoc = self.record3
        name_assoc._compute_display_name()
        self.assertEqual(name_assoc.display_name, "TestOrigin / test2 / test3")
        self.assertEqual(name_assoc.id, self.record3.id)
