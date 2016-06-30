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
from openerp import exceptions

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
        return self.create(
            partner_id=self.partner.id,
            manager_user_id=self.env.user.id,
            description="description",
            responsible_user_id=self.env.user.id,
        )

    def test_state_transition(self):
        # Analysis
        nonconformity = self.test_create_model_all_required()
        # Test action_sign_analysis in non analysis mode
        try:
            nonconformity.action_sign_analysis()
        except exceptions.ValidationError:
            self.assertTrue(True)
        # Set analysis
        nonconformity.write({
            "state": "analysis",
        })
        # Test action_sign_analysis in analysis state and in non analysis mode
        try:
            nonconformity.action_sign_analysis()
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Test action_sign_analysis  set analysis
        nonconformity.write({
            "analysis": "analysis test"
        })

        # Test transition to pending state without action_sign_analysis perform
        try:
            nonconformity.state = "pending"
        except exceptions.ValidationError:
            self.assertTrue(True)
        # perform action_sign_analysis
        nonconformity.action_sign_analysis()
        self.assertTrue(nonconformity.analysis_date)

        # Perform action_sign_analysis when it is already done
        try:
            nonconformity.action_sign_analysis()
        except exceptions.ValidationError:
            self.assertTrue(True)

        # Back to draft state when the object is not in cancel state
        try:
            nonconformity.state = "draft"
        except exceptions.ValidationError:
            self.assertTrue(True)
        # Cancel the object
        nonconformity.state = "cancel"
        self.assertTrue(nonconformity.cancel_date)

        # Reset the object
        nonconformity.state = "draft"
        self.assertFalse(nonconformity.analysis_date)
        self.assertFalse(nonconformity.actions_date)
