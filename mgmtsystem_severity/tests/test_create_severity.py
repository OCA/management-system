from openerp.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestCreateSeverity(TransactionCase):

    """
    Test management severity object.

    Test the management severity object creation.
    It checks that each fields are required and that
    a valid value creates an entry.
    """


    def setUp(self):
        super(TestCreateSeverity, self).setUp()

        self.severities = self.registry('mgmtsystem.severity')

    def test_create_severity(self):
        id = self.severities.create(self.cr, self.uid, {
            "name": "test",
            "value": 0,
            "category": "hazard"
        })

        self.assertNotEqual(id, 0)

        obj = self.severities.browse(self.cr, self.uid, id)

        self.assertEqual(obj.value, 0)
        self.assertEqual(obj.name, "test")
        self.assertEqual(obj.category, "hazard")

        id = self.severities.create(self.cr, self.uid, {
            "name": "test2",
            "value": 10,
            "category": "security"
        })

        self.assertNotEqual(id, 0)

        obj = self.severities.browse(self.cr, self.uid, id)

        self.assertEqual(obj.value, 10)
        self.assertEqual(obj.name, "test2")
        self.assertEqual(obj.category, "security")

    def test_create_serverity_without_name(self):

        with self.assertRaises(IntegrityError):
            self.severities.create(self.cr, self.uid, {
                "value": 0,
                "category": "hazard"
            })

    def test_create_serverity_without_value(self):

        with self.assertRaises(IntegrityError):
            self.severities.create(self.cr, self.uid, {
                "name": "test",
                "category": "hazard"
            })

    def test_create_serverity_without_category(self):

        with self.assertRaises(IntegrityError):
            self.severities.create(self.cr, self.uid, {
                "name": "test",
                "value": 0,
            })
