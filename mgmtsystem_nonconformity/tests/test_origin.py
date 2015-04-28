from openerp.tests import common
from psycopg2 import IntegrityError


class TestModelOrigin(common.TransactionCase):
    def test_create_origin(self):

        with self.assertRaise(IntegrityError):
            self.env['mgmtsystem.nonconformity.origin'].create({})

        record = self.env['mgmtsystem.nonconformity.origin'].create({
            "name": "TestOrigin",
        })

        self.assertNotEqual(record.id, 0)
        self.assertNotEqual(record.id, None)

    def test_name_get(self):

        record = self.env['mgmtsystem.nonconformity.origin'].create({
            "name": "TestOrigin",
        })

        name_assoc = record.name_get()
        name_dict = record._name_get_fnc(None, None)

        self.assertEqual(name_dict[record.id], "TestOrigin")
        self.assertEqual(name_assoc[0][1], "TestOrigin")
        self.assertEqual(name_assoc[0][0], record.id)
