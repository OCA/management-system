from openerp.tests import common
from psycopg2 import IntegrityError


class TestModelCause(common.TransactionCase):
    def test_create_cause(self):
        with self.assertRaises(IntegrityError):
            # Will generate an error in the logs but we handle it
            self.env['mgmtsystem.nonconformity.cause'].create({})
            # Should not be possible to create without name

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
        name_dict = record._name_get_fnc(None, None)

        self.assertEqual(name_dict[record.id], "TestCause")
        self.assertEqual(name_assoc[0][1], "TestCause")
        self.assertEqual(name_assoc[0][0], record.id)
