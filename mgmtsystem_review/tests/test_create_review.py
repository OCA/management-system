# -*- coding: utf-8 -*-

from odoo.tests import common
from datetime import datetime


class TestModelReview(common.TransactionCase):
    """Test class for mgmtsystem_review."""

    def test_create_review(self):
        """Test object creation."""
        record = self.env['mgmtsystem.review'].create({
            "name": "SampleReview",
            "date": datetime.now()
        })

        self.assertEqual(record.name, "SampleReview")
        record.button_close()
        self.assertEqual(record.state, "done")
