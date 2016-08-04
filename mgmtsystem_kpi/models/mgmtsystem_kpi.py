#  -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
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

from datetime import datetime, timedelta
from openerp import fields, models, api
from openerp.tools import (
    DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT,
)
import re
import logging
_logger = logging.getLogger(__name__)


def is_one_value(result):
    # check if sql query returns only one value
    if type(result) is dict and 'value' in result.dictfetchone():
        return True
    elif type(result) is list and 'value' in result[0]:
        return True
    else:
        return False


RE_SELECT_QUERY = re.compile('.*(' + '|'.join((
    'INSERT',
    'UPDATE',
    'DELETE',
    'CREATE',
    'ALTER',
    'DROP',
    'GRANT',
    'REVOKE',
    'INDEX',
)) + ')')


def is_select_query(query):
    """Check if sql query is a SELECT statement"""
    return not RE_SELECT_QUERY.match(query.upper())


class MgmtsystemKPI(models.Model):
    """Key Performance Indicators."""

    _name = "mgmtsystem.kpi"
    _description = "Key Performance Indicator"

    name = fields.Char('Name', size=50, required=True)
    description = fields.Text('Description')
    category_id = fields.Many2one(
        'mgmtsystem.kpi.category',
        'Category',
        required=True,
    )
    threshold_id = fields.Many2one(
        'mgmtsystem.kpi.threshold',
        'Threshold',
        required=True,
    )
    periodicity = fields.Integer('Periodicity', default=1)

    periodicity_uom = fields.Selection((
        ('hour', 'Hour'),
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month')
    ), 'Periodicity UoM', required=True, default='day')

    next_execution_date = fields.Datetime(
        'Next execution date',
        readonly=True,
    )
    value = fields.Float(string='Value',
                         compute="_compute_display_last_kpi_value",
                         )
    kpi_type = fields.Selection((
        ('python', 'Python'),
        ('local', 'SQL - Local DB'),
        ('external', 'SQL - External DB')
    ), 'KPI Computation Type')

    dbsource_id = fields.Many2one(
        'base.external.dbsource',
        'External DB Source',
    )
    kpi_code = fields.Text(
        'KPI Code',
        help=("SQL code must return the result as 'value' "
              "(i.e. 'SELECT 5 AS value')."),
    )
    history_ids = fields.One2many(
        'mgmtsystem.kpi.history',
        'kpi_id',
        'History',
    )
    active = fields.Boolean(
        'Active',
        help=("Only active KPIs will be updated by the scheduler based on"
              " the periodicity configuration."), default=True
    )
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env.user.company_id.id)

    def _compute_display_last_kpi_value(self):
        result = {}
        for obj in self.browse(self.ids):
            if obj.history_ids:
                result[obj.id] = obj.history_ids[0].value
            else:
                result[obj.id] = 0

        return result

    @api.multi
    def compute_kpi_value(self):
        for obj in self:
            kpi_value = 0
            if obj.kpi_type == 'local' and is_select_query(obj.kpi_code):
                self.env.cr.execute(obj.kpi_code)
                dic = self.env.cr.dictfetchall()
                if is_one_value(dic):
                    kpi_value = dic[0]['value']
            elif (obj.kpi_type == 'external' and obj.dbsource_id.id and
                  is_select_query(obj.kpi_code)):
                dbsrc_obj = obj.dbsource_id
                res = dbsrc_obj.execute(obj.kpi_code)
                if is_one_value(res):
                    kpi_value = res[0]['value']
            elif obj.kpi_type == 'python':
                kpi_value = eval(obj.kpi_code)

            threshold_obj = obj.threshold_id
            values = {
                'kpi_id': obj.id,
                'value': kpi_value,
                'color': threshold_obj.get_color(kpi_value),
            }

            history_obj = self.env['mgmtsystem.kpi.history']
            history_id = history_obj.create(values)
            obj.history_ids.append(history_id)

        return True

    def update_next_execution_date(self):
        for obj in self:
            if obj.periodicity_uom == 'hour':
                delta = timedelta(hours=obj.periodicity)
            elif obj.periodicity_uom == 'day':
                delta = timedelta(days=obj.periodicity)
            elif obj.periodicity_uom == 'week':
                delta = timedelta(weeks=obj.periodicity)
            elif obj.periodicity_uom == 'month':
                delta = timedelta(months=obj.periodicity)
            else:
                delta = timedelta()
            new_date = datetime.now() + delta

            values = {
                'next_execution_date': new_date.strftime(DATETIME_FORMAT),
            }

            obj.write(values)

        return True

    # Method called by the scheduler
    def update_kpi_value(self):
        if not self.ids:
            filters = [
                '&',
                '|',
                ('active', '=', True),
                ('next_execution_date', '<=',
                    datetime.now().strftime(DATETIME_FORMAT)),
                ('next_execution_date', '=', False),
            ]
            if 'filters' in self.env.context:
                filters.extend(self.env.context['filters'])
            self.ids = self.search(filters)
        res = None

        try:
            res = self.compute_kpi_value()
            self.update_next_execution_date()
        except Exception:
            _logger.exception("Failed updating KPI values")

        return res
