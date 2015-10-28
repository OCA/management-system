.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Management System - Base
================================

This module is the basis of any management system applications:
     * audit reports,
     * nonconformities,
     * immediate actions,
     * preventive actions,
     * corrective actions,
     * improvement opportunities.

Installation
============

Makes the document page approval available from where some users can approved the modification
made by oder users in documents that required approvement

Configuration
=============

No configuration required

Usage
=====

To use this module, you need to:
* Set a valid email address on the company settings.
* go to knowledge > Categories
* Create a new page category and set an approver group. Make sure users
  belonging to that group have valid email addresses.
* go to knowledge > Pages
* Create a new page and choose the previously created category.
* A notification is sent to the group with a link to the page history to
  review.
* Depending on the review, the page history is approved or not.
* Users reading the page see the last approved version.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/118/9.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
knowledge/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
knowledge/issues/new?body=module:%20
document_page_approval%0Aversion:%20
9.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Odoo SA <info@odoo.com>
* Savoir-faire Linux <support@savoirfairelinux.com>
* Gervais Naoussi <gervaisnaoussi@gmail.com>

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

Here are the modification that have been done

The module no more depends on email_template but on mail module
the model's module are now in the models folder and they are been split so that
we have one file for each model (document_page_approval.py and
document_page_history_workflow.py)
we moved the view in the views folder  and the workflow int the workflow folder
we edited the data file data/email_template.xml and
the document_page_history_workflow.py so that they now use the mail module
the __openerp__.py file now reflected the new module structure
