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

from osv import fields, orm


class UnderlyingAssets(orm.Model):

    """Underlying Assets."""

    _name = "mgmtsystem.security.assets.underlying"
    description = "Underlying Assets"

    _columns = {
        'name': fields.char("Name"),
        'category': fields.many2one(
            "mgmtsystem.security.assets.category", "Category"
        ),
        'essential_assets': fields.many2many(
            "mgmtsystem.security.assets.essential",
            "mgmtsystem_security_assets_essential_rel",
            "underlying_asset_id",
            "essential_asset_id",
            "Essential Assets"
        ),
    }
