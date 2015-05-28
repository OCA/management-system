Management System Security Event
================================

This module allow you to manage security events.

Installation
============

To install this module, you need to:

 * Clone the project from github on your instance
    * git clone https://github.com/OCA/management-system.git
 * Start odoo with the project in the addons path

Configuration
=============

You may customize the colors to be displayed on the risk matrix.

 * go to Management System > Configuration > Security > Risk Matrix Levels

 Define the colors related to a range of cells in the risk matrix.


Usage
=====

To use this module, you need to:

 * go to Management System > Manuals > Security > Threat Scenarios

    - Create a scenario (S1)
    - Select the actual, original and residual probability and severity of the scenario

 * go to Management System > Manuals > Security > Threat Scenarios

    - Create a measure (M1)

 * go to Management System > Manuals > Security > Security Events

    - Create a security event (E1)
    - Add scenario S1 on the event
    - Add measure M1 on the event

 * go to Management System > Security > Risk Matrix

    - Select the type of matrix to generate and click on 'Done'


Credits
=======

Contributors
------------

* Loïc Faure-Lacroix <loic.lacroix@savoirfairelinux.com>
* David Dufresne <david.dufresne@savoirfairelinux.com>
* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
