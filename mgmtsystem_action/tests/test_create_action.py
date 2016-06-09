from openerp.tests import common


class TestModelAction(common.TransactionCase):
    def test_create_action(self):
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        self.assertEqual(record.name, "SampleAction")
        self.assertNotEqual(record.reference, "NEW")
        self.assertEqual(record.type_action, "immediate")
        self.assertEqual(record.stage_id.name, "Draft")
        self.assertEqual(record.stage_id.is_starting, True)

    def test_case_open(self):
<<<<<<< 30b7755499fb1bc52d6afb3c3e19c803eb3ba928
=======
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
>>>>>>> add the case_open method, because it is usefull for mgmtsystem_nonconformity
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

    def test_get_action_url(self):
        record = self.env['mgmtsystem.action'].create({
            "name": "SampleAction",
            "type_action": "immediate",
        })

        ret = record.get_action_url()

        self.assertEqual(isinstance(ret, list), True)
        self.assertEqual(len(ret), 1)
        self.assertEqual(isinstance(ret[0], basestring), True)
        self.assertEqual(ret[0].startswith('http'), True)
