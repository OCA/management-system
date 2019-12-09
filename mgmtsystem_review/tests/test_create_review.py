from odoo import fields
from odoo.tests import common


class TestModelReview(common.TransactionCase):
    """Test class for mgmtsystem_review."""

    def test_create_review(self):
        """Test object creation."""
        record = self.env["mgmtsystem.review"].create(
            {"name": "SampleReview", "date": fields.Datetime.now()}
        )

        self.assertEqual(record.name, "SampleReview")
        record.button_close()
        self.assertEqual(record.state, "done")
