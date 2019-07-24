
from odoo import exceptions
from odoo.tests import common
from datetime import datetime, timedelta
import mock
import time


def freeze_time(dt):
    mock_time = mock.Mock()
    mock_time.return_value = time.mktime(dt.timetuple())
    return mock_time


class TestModelAction(common.SavepointCase):
    """Test class for mgmtsystem_action."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.record = cls.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate"
        })

    def _assert_date_equal(self, val, expected=None):
        expected = expected or datetime.now()
        self.assertEqual(
            tuple(val.timetuple())[:5],
            tuple(expected.timetuple())[:5]
        )

    def test_create_action(self):
        """Test object creation."""
        stage = self.env.ref('mgmtsystem_action.stage_open')
        self.assertEqual(self.record.name, "SampleAction")
        self.assertNotEqual(self.record.reference, "NEW")
        self.assertEqual(self.record.type_action, "immediate")
        self.assertEqual(self.record.stage_id.name, "Draft")
        self.assertEqual(self.record.stage_id.is_starting, True)
        self.assertFalse(self.record.date_open)
        self.record.stage_id = stage
        self._assert_date_equal(self.record.date_open)

    def test_case_close(self):
        """Test object close state."""
        stage = self.env.ref('mgmtsystem_action.stage_open')
        stage_new = self.env.ref('mgmtsystem_action.stage_draft')
        self.record.stage_id = stage
        stage = self.env.ref('mgmtsystem_action.stage_close')
        self.record.stage_id = stage
        self._assert_date_equal(self.record.date_closed)
        try:
            self.record.write({'stage_id': stage_new.id})
        except exceptions.ValidationError:
            self.assertTrue(True)
        stage = self.env.ref('mgmtsystem_action.stage_close')
        try:
            self.record.write({'stage_id': stage.id})
        except exceptions.ValidationError:
            self.assertTrue(True)

    def test_get_action_url(self):
        """Test if action url start with http."""
        url = self.record.get_action_url()
        self.assertEqual(url.startswith('http'), True)
        self.assertIn(
            '&id={}&model={}'.format(self.record.id, self.record._name), url
        )

    def test_process_reminder_queue(self):
        """Check if process_reminder_queue work when days reminder are 10."""
        ten_days_date = datetime.now().date() + timedelta(days=10)
        self.record.write({
            'date_deadline': ten_days_date,  # 10 days from now
            'stage_id': self.env.ref('mgmtsystem_action.stage_open').id,
        })
        with mock.patch('time.time', freeze_time(ten_days_date)):
            tmpl_model = self.env['mail.template']
            with mock.patch.object(type(tmpl_model), 'send_mail') as mocked:
                self.env['mgmtsystem.action'].process_reminder_queue()
                mocked.assert_called_with(self.record.id)

    def test_stage_groups(self):
        """Check if stage_groups return all stages."""
        stage_ids = self.env['mgmtsystem.action.stage'].search([])
        stages_found = self.record._stage_groups(stage_ids)
        state = (len(stage_ids) == len(stages_found[0]))
        self.assertFalse(state)

    def test_send_mail(self):
        """Check if mail send action work."""
        tmpl_model = self.env['mail.template']
        with mock.patch.object(type(tmpl_model), 'send_mail') as mocked:
            self.env['mgmtsystem.action'].send_mail_for_action(self.record)
            mocked.assert_called_with(self.record.id, force_send=True)
