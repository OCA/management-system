# -*- coding: utf-8 -*-

from openerp.tests import common
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
        self.assertFalse(record.opening_date)
        record.stage_id = stage
        self.assertEqual(record.opening_date[:-3], datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        ))

    def test_case_open(self):
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        record.active = False

        ret = record.case_open()

        self.assertEqual(ret, True)
        self.assertEqual(record.active, True)
        self.assertEqual(record.stage_id.name, 'In Progress')
        self.assertEqual(record.stage_id.is_starting, False)
        self.assertEqual(record.stage_id.is_ending, False)

    def test_case_close(self):
        """Test object close state."""
        stage = self.env.ref('mgmtsystem_action.stage_close')
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        record.stage_id = stage

        self.assertEqual(record.date_closed[:-3], datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        ))

    def test_get_action_url(self):
        """Test if action url start with http."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        ret = record.get_action_url()

        # self.assertEqual(isinstance(ret, list), True)
        # self.assertEqual(len(ret), 1)
        self.assertEqual(isinstance(ret, basestring), True)
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
        stages = self.env['mgmtsystem.action.stage'].search([])
        stages_found = record._stage_groups({}, None)
        state = (len(stages) == len(stages_found[0]))
        self.assertTrue(state)

    def test_send_mail(self):
        """Check if mail send action work."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        self.assertTrue(record.send_mail_for_action(record))
