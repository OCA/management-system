from odoo.tests.common import SavepointCase


class TestMgmtsystemNonconformityProject(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a project
        cls.project = cls.env["project.project"].create(
            {
                "name": "Test Project",
            }
        )
        # Create a nonconformity action
        cls.action = cls.env["mgmtsystem.action"].create(
            {
                "name": "Test Action",
                "action_type": "action",
            }
        )

    def test_action_type_selection(self):
        """Test that action_type field works correctly."""
        self.assertEqual(self.action.action_type, "action")

    def test_complete_name_action_type(self):
        """Test complete_name computation for action type."""
        self.assertEqual(self.action.complete_name, "Test Action")

    def test_complete_name_project_type(self):
        """Test complete_name computation for project type."""
        self.action.action_type = "project"
        self.action.project_id = self.project
        self.assertEqual(self.action.complete_name, "Test Project")
