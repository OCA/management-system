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

from openerp.addons.report_webkit.webkit_report import WebKitParser
from openerp import pooler
from openerp.report import report_sxw


class RiskMatrixParser(report_sxw.rml_parse):

    def __init__(self, cursor, uid, name, context):
        super(RiskMatrixParser, self).__init__(
            cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr

        self.localcontext.update({})

WebKitParser(
    'report.mgmtsystem_security_event.risk_matrix_webkit',
    'mgmtsystem.risk.matrix',
    'addons/mgmtsystem_security_event/report/risk_matrix_webkit.mako',
    parser=RiskMatrixParser)
