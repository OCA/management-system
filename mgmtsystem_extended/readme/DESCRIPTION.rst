This module contains some new features for Management System modules.

Nonconformity (NC)

- Type: add a field to classify a NC in Internal, Partner, Customer, External.
    * Internal: when the NC is due and revealed in an internal process
    * Partner:  when the NC is due to a Partner
    * Customer: when the NC si due and connected to a claim of the Customer
    * External: when the NC si due and connected to a claim of an External entity (e.g. an Authority)
- Quantity checked and not compliant
- Product quantity: add a field to indicate the quantity used to reveal the NC (qty-ck) 
    and the quantity resulted non-compliant (qty-nc). 

    A check is performed on the quantity to ensure that qty-nc isn't greater than qty-ck and
    in case perform an auto-set.
- Tracking: add tracking information to changes of field «Plan Review» of the NC.

Action

- new tab in the action view to evaluate the efficacy of the action. Changes are tracked.
- new flag for define an Action as Template
- new field to select a Template Action for fill predefined fields
