## Risk Matrix Levels

Define which cells in the risk matrix are green, orange, or red.

Go to **Management System > Configuration > Security > Risk Matrix Levels** and
create one record per zone. Each level covers a rectangular region of the matrix
defined by a probability range and a severity range. Ranges must not overlap.

A default 4 × 4 matrix configuration is installed with the module. Adjust it to
match your organization's risk appetite.

## Assets and Threat Sources

Before creating vectors and events, populate the reference data:

- **Management System > Manuals > Security > Assets > Primary Assets** — the
  information assets or business processes you need to protect.
- **Management System > Manuals > Security > Assets > Supporting Assets** — the
  servers, software, and infrastructure that host primary assets. Link each
  supporting asset to the primary assets it carries.
- **Management System > Manuals > Security > Threat Sources** — the actors or
  causes that could exploit a vector (e.g. external attacker, malicious insider).
