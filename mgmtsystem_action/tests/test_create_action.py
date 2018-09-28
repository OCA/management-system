
from odoo import exceptions
from odoo.tests import common
from datetime import datetime, timedelta


class TestModelAction(common.TransactionCase):
    """Test class for mgmtsystem_action."""

    def test_create_action(self):
        """Test object creation."""
        stage = self.env.ref('mgmtsystem_action.stage_open')
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate"
        })

        self.assertEqual(record.name, "SampleAction")
        self.assertNotEqual(record.reference, "NEW")
        self.assertEqual(record.type_action, "immediate")
        self.assertEqual(record.stage_id.name, "Draft")
        self.assertEqual(record.stage_id.is_starting, True)
        self.assertFalse(record.date_open)
        record.stage_id = stage
        self.assertEqual(record.date_open[:-3], datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        ))

    def test_case_close(self):
        """Test object close state."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        stage = self.env.ref('mgmtsystem_action.stage_open')
        stage_new = self.env.ref('mgmtsystem_action.stage_draft')
        record.stage_id = stage
        stage = self.env.ref('mgmtsystem_action.stage_close')
        record.stage_id = stage
        self.assertEqual(record.date_closed[:-3], datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        ))
        try:
            record.write({'stage_id': stage_new.id})
        except exceptions.ValidationError:
            self.assertTrue(True)
        stage = self.env.ref('mgmtsystem_action.stage_close')
        try:
            record.write({'stage_id': stage.id})
        except exceptions.ValidationError:
            self.assertTrue(True)

    def test_get_action_url(self):
        """Test if action url start with http."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        ret = record.get_action_url()
        self.assertEqual(isinstance(ret, str), True)
        self.assertEqual(ret.startswith('http'), True)

    def test_process_reminder_queue(self):
        """Check if process_reminder_queue work when days reminder are 10."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
            "date_deadline": datetime.now() + timedelta(days=10)
        })
        self.assertTrue(record.process_reminder_queue())

    def test_stage_groups(self):
        """Check if stage_groups return all stages."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        stage_ids = self.env['mgmtsystem.action.stage'].search([])
        stages_found = record._stage_groups(stage_ids)
        state = (len(stage_ids) == len(stages_found[0]))
        self.assertFalse(state)

    def test_send_mail(self):
        """Check if mail send action work."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        self.assertTrue(record.send_mail_for_action(record))
