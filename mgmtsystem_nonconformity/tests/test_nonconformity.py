from openerp.tests import common
from psycopg2 import IntegrityError

model_name = "mgmtsystem.nonconformity"


class TestModelNonConformity(common.TransactionCase):
    def setUp(self):
        super(TestModelNonConformity, self).setUp()

        self.partner = self.env['res.partner'].search([])[0]

    def create(self, **kargs):
        return self.env[model_name].create(kargs)

    def create_raise_exception(self, **kargs):
        with self.assertRaises(IntegrityError):
            self.create(**kargs)
        self.cr.rollback()

    def test_create_model(self):
        self.create_raise_exception(
            manager_user_id=self.env.user.id,
        )

        self.create_raise_exception(
            manager_user_id=self.env.user.id,
            partner_id=self.partner.id,
        )

        self.create_raise_exception(
            manager_user_id=self.env.user.id,
            partner_id=self.partner.id,
            description="description",
        )

    def test_create_model_all_required(self):
        # All required fields
        self.create(
            manager_user_id=self.env.user.id,
            partner_id=self.partner.id,
            description="description",
            responsible_user_id=self.env.user.id,
        )
