# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from contextlib import contextmanager
from psycopg2 import IntegrityError
from openerp.tests import common

model_name = "mgmtsystem.nonconformity"


class TestModelNonConformity(common.TransactionCase):
    def setUp(self):
        super(TestModelNonConformity, self).setUp()

        self.partner = self.env['res.partner'].search([])[0]

    def create(self, **kwargs):
        return self.env[model_name].create(kwargs)

    @contextmanager
    def assertRaisesRollback(self, *args, **kwargs):
        """Do a regular assertRaises but perform rollback at the end
        """
        with self.assertRaises(*args, **kwargs) as ar:
            yield ar
        self.cr.rollback()

    def create_raise_exception(self, **kwargs):
        with self.assertRaisesRollback(IntegrityError):
            self.env[model_name].create(kwargs)

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
