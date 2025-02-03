#    Copyright (C) 2025 Open2bizz BV www.open2bizz.nl

from odoo import fields, models

class DocumentPageChapter(models.Model):

    _name= "document.page.chapter"
    _description = "NEN Chapter"

    code = fields.Char("Code", required=True)
    name = fields.Char("Name", required=True)
    parent_id = fields.Many2one("document.page.chapter", "Parent Chapter")
    display_name = fields.Char("Display Name", compute="_compute_display_name")

    def _compute_display_name(self):
        for record in self:
            if record.parent_id:
                record.display_name = f"{record.parent_id.display_name} / {record.name}"
            else:
                record.display_name = record.name
