# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Daniel Reis
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
{
    'name' : 'Management System - Feedback',
    'version' : '1',
    'author' : 'Daniel Reis',
    'category' : 'Management System',
    'description': """\
Extends the nonconformity model so it can also represent other types of feedback, 
such as complaints, measurements, suggestions, etc.

- "Feedback Source": the source channel originating this Feedback record - an 
audit, complaint, measurement, etc. In case this overlaps with the use of the 
nonconformity "Origin" field, it can be adapted to be used as a generic Category
attribute.

- "Feedback Type": identifies if the feedback corresponds to a nonconformity, or
to other type of record, such as "best practice", "suggestion", etc. It may be 
qualified only later in the process. 

""",
    'depends' : ['mgmtsystem_nonconformity'],
    'data' : [
        'security/ir.model.access.csv',
	    'mgmtsystem_feedback.xml',
        'mgmtsystem_feedback_data.xml',
    ],
    'demo' : [
        'mgmtsystem_feedback_demo.xml',
    ],
    'installable' : True,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

