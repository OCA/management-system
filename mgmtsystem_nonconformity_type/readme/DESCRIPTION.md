This module add classification for the Nonconformity of Management
System module.

Nonconformity (NC)

- Type: add a field to classify a NC in Internal, Partner, Customer, External.  
  - Internal: when the NC is due and revealed in an internal process
  - Partner: when the NC is due to a Partner
  - Customer: when the NC si due and connected to a claim of the
    Customer
  - External: when the NC si due and connected to a claim of an External
    entity (e.g. an Authority)

- For the Partner NC type add a button to send an email to the Partner
  associated with the Nonconformity: for this
  mgmtsystem_nonconformity_partner has to be installed and a Partner's
  Contact of type Quality has to be set

- Quantity checked (qty-ck) and not compliant (qty-nc): a check is
  performed on the quantity to ensure that qty-nc isn't greater than
  qty-ck and in case perform an auto-set.
