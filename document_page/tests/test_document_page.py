# -*- coding: utf-8 -*-

from odoo.tests import common


class TestDocumentPage(common.TransactionCase):

    def setUp(self):
        super(TestDocumentPage, self).setUp()
        self.page_obj = self.env['document.page']
        self.history_obj = self.env['document.page.history']
        self.category1 = self.env.ref('document_page.demo_category1')
        self.page1 = self.env.ref('document_page.demo_page1')

    def test_page_creation(self):
        page = self.page_obj.create({
            'name': 'Test Page 1',
            'parent_id': self.category1.id,
            'content': 'Test content'
        })
        self.assertEqual(page.content, 'Test content')
        self.assertEqual(len(page.history_ids), 1)
        page.content = 'New content for Demo Page'
        self.assertEqual(len(page.history_ids), 2)

    def test_category_template(self):
        page = self.page_obj.create({
            'name': 'Test Page 2',
            'parent_id': self.category1.id,
        })
        page._onchange_parent_id()
        self.assertEqual(page.content, self.category1.template)

    def test_page_history_diff(self):
        page = self.page_obj.create({
            'name': 'Test Page 3',
            'content': 'Test content'
        })
        page.content = 'New content'
        self.assertIsNotNone(page.history_ids[0].diff)
