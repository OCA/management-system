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
from . import test_security_measure
from . import test_security_assets_category
from . import test_security_assets_essential
from . import test_security_threat_origin
from . import test_security_event_measure
from . import test_security_assets_underlying
from . import test_security_event_scenario
from . import test_security_threat_scenario
from . import test_security_event

checks = [
    test_security_measure,
    test_security_assets_category,
    test_security_assets_essential,
    test_security_threat_origin,
    test_security_event_measure,
    test_security_assets_underlying,
    test_security_event_scenario,
    test_security_threat_scenario,
    test_security_event,
]
