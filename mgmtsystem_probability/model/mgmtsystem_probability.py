# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 - Present
#    Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.tools.translate import _
from osv import fields, orm


class MgmtSystemProbability(orm.Model):

    """
    Define the Probability for management system.

    Allow you to manage scale of probability (or likelihood)
    used across different modules (health and safety, information security).
    """

    _name = "mgmtsystem.probability"
    _description = "Management System Probability"

    def __category_selection(self, cr, uid, context=None):
        """
        Return the category selection.

        This method act as a proxy between the model method
        _category_selection and odoo. Subclassing the method
        used in the field.selection has no effect. Subclass
        the _category_selection method instead.
        """
        return self._category_selection(cr, uid, context)

    _columns = {
        "name": fields.char("Name", required=True),
        "value": fields.integer("Value", required=True),
        "category": fields.selection(
            __category_selection,
            "Category",
            required=True
        ),
    }

    def _category_selection(self, cr, uid, context=None):
        """
        Return the category selection.

        This method can be subclassed by other classes.
        """
        return [
            ("hazard", _("hazard")),
            ("security", _("security")),
        ]
