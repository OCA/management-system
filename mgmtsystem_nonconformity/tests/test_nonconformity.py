from openerp.tests import common
from psycopg2 import IntegrityError

model_name = "mgmtsystem.nonconformity"


class TestModelNonConformity(common.TransactionCase):
    def create(self, **kargs):
        return self.env[model_name].create(kargs)

    def create_raise_exception(self, **kargs):
        try:
            self.create(**kargs)
        except IntegrityError as exc:
            # Integrity error
            self.assertEqual(exc.pgcode, '23502')
            exc.cursor.connection.rollback()
            return True
        return False

    def test_create_model(self):
        ret = self.create_raise_exception()
        self.assertEqual(ret, True)
        partner = self.env['res.partner'].search([])[0]

        ret = self.create_raise_exception(
            name="Test"
        )
        self.assertEqual(ret, True)

        ret = self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
        )
        self.assertEqual(ret, True)

        ret = self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
            partner_id=partner.id,
        )
        self.assertEqual(ret, True)

        ret = self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
            partner_id=partner.id,
            description="description",
        )
        self.assertEqual(ret, True)

        # All required fields
        ret = self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
            partner_id=partner.id,
            description="description",
            responsible_user_id=self.env.user.id,
        )
        self.assertEqual(ret, False)
