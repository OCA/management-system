.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================
Management System - Action
==========================

This module enables you to manage the different actions of your management system:

* immediate actions
* corrective actions
* preventive actions
* improvement opportunities.

The person responsible for an action is notified by email:

* when the action is assigned
* 10 calendar days before the deadline	

Installation
============

No installation required.

Configuration
=============

The email content of notifications can be customized as any email templates.

Usage
=====

To use this module:

* Go to Management System > Actions
* Create new Action
* Select a type and enter the subject

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/128/9.0

Mention/Description
===================

* mgmtsystem_action/data/automated_reminder.xml
    - Contains cron job actions
* mgmtsystem_action/data/email_template.xml
    - Contains needed email templates

Known issues / Roadmap
======================

* The custom emails should be replaced by Mail Tracking features and Subtypes (like in Project Tasks and Project Issues)
* Replace the cron job (process_reminder_queue) by an automated actions. It is located in mgmtsystem_action.py

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/Management-system/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
Management-system/issues/new?body=module:%20
mgmtsystem_system%0Aversion:%20
10.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Savoir-faire Linux <support@savoirfairelinux.com>
* Gervais Naoussi <gervaisnaoussi@gmail.com>
* Eugen Don <eugen.don@don-systems.de>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

Changelog
---------


v9.0.1.0.0

* the module does no depends anymore on document_page module.
* the module does no depends anymore on crm_claim module.
