.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Management System base
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

Makes the Management System base Application Configuration available from where you can install
any oder management system applications.

Configuration
=============

No configuration required

Usage
=====

To use this module, you need to:
* go to Management system > Configuration > System to create your system domain

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/118/9.0

Known issues / Roadmap
======================

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
Management-system/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback `here <https://github.com/OCA/
Management-system/issues/new?body=module:%20
mgmtsystem_system%0Aversion:%20
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

The manual field is been removed from model mgmtsystem_system so that the module
 no more depends on document_page module.
 The manual field is also removed from views system_form and system_tree which are inside
 mgmtsystem_system.xml

We added views folder
we moved menus.xml, mgmtsystem_system.xml and board_mgmtsystem_view.xml to views
we renamed board_mgmtsystem_view.xml to board_mgmtsystem.xml

 In oder to fixed an missing context.js error
 The following code was removed from board_mgmtsystem.xml view
<hpaned>
    <child1>
    </child1>
    <child2>
    </child2>
</hpaned>

inside the form tag

inside menu.xml

we removed inside the menuitem with id "menu_mgmtsystem_root" the following parameters
web_icon="images/mgmtsystem.png"
web_icon_hover="images/mgmtsystem-hover.png"

we created models folder
we moved mgmtsystem_system.py to that folder and edited it to respect the new Odoo model api
and OCA guidelines
we created the __init__.py file

we edited the __openerp__.py file to reflect the new folder structure
we edited the __init__.py file to initialised the python module
