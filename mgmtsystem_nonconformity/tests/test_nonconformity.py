from openerp.tests import common
from psycopg2 import IntegrityError

model_name = "mgmtsystem.nonconformity"


class TestModelNonConformity(common.TransactionCase):
    def create(self, **kargs):
        return self.env[model_name].create(kargs)

    def create_raise_exception(self, **kargs):
        with self.assertRaises(IntegrityError):
            self.create(**kargs)

    def test_create_model(self):
        ret = self.create_raise_exception()
        self.assertEqual(ret, True)
        partner = self.env['res.partner'].search([])[0]

        self.create_raise_exception(
            name="Test"
        )

        self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
        )

        self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
            partner_id=partner.id,
        )

        self.create_raise_exception(
            name="Test",
            manager_user_id=self.env.user.id,
            partner_id=partner.id,
            description="description",
        )

        # All required fields
        self.create(
            name="Test",
            manager_user_id=self.env.user.id,
            partner_id=partner.id,
            description="description",
            responsible_user_id=self.env.user.id,
        )
