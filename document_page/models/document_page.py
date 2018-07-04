# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DocumentPage(models.Model):
    """This class is use to manage Document."""

    _name = "document.page"
    _inherit = ['mail.thread']
    _description = "Document Page"
    _order = 'name'

    name = fields.Char('Title', required=True)

    type = fields.Selection(
        [('content', 'Content'), ('category', 'Category')],
        'Type',
        help="Page type",
        default="content"
    )

    parent_id = fields.Many2one(
        'document.page',
        'Category',
        domain=[('type', '=', 'category')]
    )

    child_ids = fields.One2many(
        'document.page',
        'parent_id',
        'Children'
    )

    content = fields.Text(
        "Content",
        compute='_compute_content',
        inverse='_inverse_content',
        search='_search_content',
        required=True,
    )

    # no-op computed field
    summary = fields.Char(
        help='Describe the changes made',
        compute=lambda x: x,
        inverse=lambda x: x,
    )

    template = fields.Html(
        "Template",
        help="Template that will be used as a content template "
             "for all new page of this category.",
    )

    # deprecated - should be removed on 11.0
    # left here because some modules might still need it
    display_content = fields.Text(
        string='Displayed Content',
        compute='_compute_display_content'
    )

    history_head = fields.Many2one(
        'document.page.history',
        'HEAD',
        compute='_compute_history_head',
        store=True,
        auto_join=True,
    )

    history_ids = fields.One2many(
        'document.page.history',
        'page_id',
        'History',
        order='create_date DESC',
        readonly=True,
    )

    menu_id = fields.Many2one(
        'ir.ui.menu',
        "Menu",
        readonly=True
    )

    content_date = fields.Datetime(
        'Last Contribution Date',
        related='history_head.create_date',
        store=True,
        index=True,
        readonly=True,
    )

    content_uid = fields.Many2one(
        'res.users',
        'Last Contributor',
        related='history_head.create_uid',
        store=True,
        index=True,
        readonly=True,
    )

    @api.multi
    def _get_page_index(self, link=True):
        """Return the index of a document."""
        self.ensure_one()
        index = []
        for subpage in self.child_ids:
            index += ["<li>" + subpage._get_page_index() + "</li>"]
        r = ''
        if link:
            r = '<a href="#id=%s">%s</a>' % (self.id, self.name)

        if index:
            r += "<ul>" + "".join(index) + "</ul>"
        return r

    @api.multi
    @api.depends('content')
    def _compute_display_content(self):
        # @deprecated, simply use content
        for rec in self:
            rec.display_content = rec.content

    @api.multi
    @api.depends('history_head', 'history_ids')
    def _compute_content(self):
        for rec in self:
            if rec.type == 'category':
                rec.content = rec._get_page_index(link=False)
            else:
                if rec.history_head:
                    rec.content = rec.history_head.content
                else:
                    # html widget's default, so it doesn't trigger ghost save
                    rec.content = '<p><br></p>'

    @api.multi
    def _inverse_content(self):
        for rec in self:
            if rec.type == 'content':
                rec._create_history({
                    'content': rec.content,
                    'summary': rec.summary,
                })

    @api.multi
    def _search_content(self, operator, value):
        return [('history_head.content', operator, value)]

    @api.multi
    @api.depends('history_ids')
    def _compute_history_head(self):
        for rec in self:
            if rec.history_ids:
                rec.history_head = rec.history_ids[0]

    @api.multi
    def _create_history(self, vals):
        self.ensure_one()
        history = self.env['document.page.history']
        vals['page_id'] = self.id
        return history.create(vals)

    @api.onchange("parent_id")
    def _onchange_parent_id(self):
        """We Set it the right content to the new parent."""
        if not self.content or self.content == '<p><br></p>':
            if self.parent_id and self.parent_id.type == "category":
                    self.content = self.parent_id.template
