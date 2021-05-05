from odoo import _
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestActionEfficacy(TransactionCase):

    def test_action(self):
        """
        Test efficency changes
        """
        action = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate"
        })

        action.efficacy_value = 50
        action._onchange_efficacy_value()
        self.assertEqual(action.efficacy_value == 50, True)

        action.efficacy_value = 200
        with self.assertRaises(ValidationError) as ve:
            action._onchange_efficacy_value()
        self.assertIn(_('Rating must be between 0 and 100'), str(ve.exception))
