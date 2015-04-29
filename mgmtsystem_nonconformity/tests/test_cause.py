from openerp.tests import common
from psycopg2 import IntegrityError


class TestModelCause(common.TransactionCase):
    def test_create_cause(self):
        with self.assertRaises(IntegrityError):
            # Will generate an error in the logs but we handle it
            self.env['mgmtsystem.nonconformity.cause'].create({})
            # Should not be possible to create without name
        self.cr.rollback()

        record = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "TestCause",
        })

        self.assertNotEqual(record.id, 0)
        self.assertNotEqual(record.id, None)

    def test_name_get(self):

        record = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "TestCause",
        })

        name_assoc = record.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause")
        self.assertEqual(name_assoc[0][0], record.id)

        record2 = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "test2",
            "parent_id": record.id
        })

        name_assoc = record2.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause / test2")
        self.assertEqual(name_assoc[0][0], record2.id)

        record3 = self.env['mgmtsystem.nonconformity.cause'].create({
            "name": "test3",
            "parent_id": record2.id
        })

        name_assoc = record3.name_get()

        self.assertEqual(name_assoc[0][1], "TestCause / test2 / test3")
        self.assertEqual(name_assoc[0][0], record3.id)
