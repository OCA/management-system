
from odoo.tests import common


class TestNonconformityProject(common.TransactionCase):

    def test_create_action(self):
        action = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
            "action_type": "project",
            "project_id": self.env.ref('project.project_project_data').id
        })
        self.assertEqual(action.name, "SampleAction")
        self.assertEqual(action.complete_name, "Start here to discover Odoo")
