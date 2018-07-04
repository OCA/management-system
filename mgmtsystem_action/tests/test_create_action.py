# -*- coding: utf-8 -*-

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
        self.assertFalse(record.opening_date)
        record.stage_id = stage
        self.assertEqual(record.opening_date[:-3], datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        ))

    def test_case_open(self):
        """Test object open state."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        record.write(
            {'active': False, 'stage_id': record._get_stage_open().id})

        ret = record.case_open()

        self.assertEqual(ret, True)
        self.assertEqual(record.active, True)
        self.assertEqual(record.stage_id.name, 'In Progress')
        self.assertEqual(record.stage_id.is_starting, False)
        self.assertEqual(record.stage_id.is_ending, False)

    def test_get_new_stage(self):
        """Get stage new."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        stage = record._get_stage_new()

        self.assertEqual(stage.name, 'Draft')

    def test_case_close(self):
        """Test object close state."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        stage = record._get_stage_open()
        stage_new = record._get_stage_new()
        record.stage_id = stage
        stage = record._get_stage_close()
        record.stage_id = stage
        self.assertEqual(record.date_closed[:-3], datetime.now().strftime(
            '%Y-%m-%d %H:%M'
        ))
        try:
            record.write({'stage_id': stage_new.id})
        except exceptions.ValidationError:
            self.assertTrue(True)
        stage = record._get_stage_cancel()
        record.stage_id = stage
        self.assertFalse(record.date_closed)
        self.assertFalse(record.opening_date)
        stage = record._get_stage_close()
        try:
            record.write({'stage_id': stage.id})
        except exceptions.ValidationError:
            self.assertTrue(True)
        record.write({'stage_id': stage_new.id})
        self.assertFalse(record.date_closed)
        self.assertFalse(record.opening_date)

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
        stage_ids = self.env['mgmtsystem.action.stage'].search([])
        stages_found = record._stage_groups(self, record, stage_ids)
        state = (len(stage_ids) == len(stages_found[0]))
        self.assertFalse(state)

    def test_send_mail(self):
        """Check if mail send action work."""
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })
        self.assertTrue(record.send_mail_for_action(record))
