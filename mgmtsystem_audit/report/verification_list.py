# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

import time
from openerp.report import report_sxw
from openerp.tools.translate import _


class mgmtsystem_audit_verification_list(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(mgmtsystem_audit_verification_list, self).__init__(
            cr, uid, name, context
        )
        self.localcontext.update({
            'time': time,
            'get_lines_by_procedure': self.get_lines_by_procedure,
        })
        self.context = context

    def get_lines_by_procedure(self, verification_lines):
        p = []
        for l in verification_lines:
            if l.procedure_id.id:
                proc_nm = self.pool.get('document.page').read(
                    self.cr, self.uid, l.procedure_id.id, ['name']
                )
                procedure_name = proc_nm['name']
            else:
                procedure_name = _('Undefined')

            p.append({"id": l.id,
                      "procedure": procedure_name,
                      "name": l.name,
                      "yes_no": "Yes / No"})
        p = sorted(p, key=lambda k: k["procedure"])
        proc_line = False
        q = []
        proc_name = ''
        for i in range(len(p)):
            if proc_name != p[i]['procedure']:
                proc_line = True
            if proc_line:
                q.append({"id": p[i]['id'],
                          "procedure": p[i]['procedure'],
                          "name": "",
                          "yes_no": ""})
                proc_line = False
                proc_name = p[i]['procedure']
            q.append({"id": p[i]['id'],
                      "procedure": "",
                      "name": p[i]['name'],
                      "yes_no": "Yes / No"})
        return q


report_sxw.report_sxw(
    'report.mgmtsystem.audit.verificationlist',
    'mgmtsystem.audit',
    'addons/mgmtsystem_audit/report/verification_list.rml',
    parser=mgmtsystem_audit_verification_list
)
