from odoo import _
from odoo.tests.common import TransactionCase


class TestModelNonConformity(TransactionCase):
    def setUp(self):
        """
        Sets some enviroment
        """
        super(TestModelNonConformity, self).setUp()

        self.action_model = self.env["mgmtsystem.action"]
        self.action_template_model = self.env["mgmtsystem.action.template"]

        # create a template action
        self.action_template = self.action_template_model.create(
            {
                "name": "Test Template",
                "type_action": self.action_model.search([])[0]["type_action"],
            }
        )

    def test_get_template(self):
        """
        Test set Action template
        """
        self.action = self.action_model.search([])[0]

        self.action["template_id"] = self.action_template["id"]
        self.action._onchange_template_id()

        self.assertEqual(
            self.action["name"] == _("NEW") + " " + self.action_template["name"], True
        )
