## Typical workflow

### 1. Create attack vectors

Go to **Management System > Manuals > Security > Vectors** and create one record
per attack vector. For each vector:

- Set the **Original** probability and severity (risk without any control).
- Set the **Current** probability and severity (risk with existing controls).
- Set the **Residual** probability and severity (risk after planned remediation).
- Optionally link the supporting assets that are exposed by this vector.

### 2. Create security controls

Go to **Management System > Manuals > Security > Controls** and create the
countermeasures available in your organization.

### 3. Create feared events

Go to **Management System > Manuals > Security > Feared Events** and create one
record per feared event. For each event:

- Tick the **Confidentiality**, **Integrity**, and/or **Availability** flags that
  the event threatens.
- In the **Scenarios** tab, add one line per attack scenario: select the vector
  and threat source, and describe how the attack could unfold. The event's risk
  ratings (probability and severity) are automatically computed as the maximum
  across all linked vectors.
- In the **Controls** tab, add the controls that mitigate this event. For each
  control line, indicate whether it acts as **Prevention**, **Protection**,
  and/or **Recovery**, and optionally link the specific supporting asset it
  protects.

Use the search bar to filter events by **Confidentiality**, **Integrity**, or
**Availability**, or group them by system or severity.

### 4. Generate the risk matrix

Go to **Management System > Manuals > Security > Risk Matrix**, select the risk
type (**Original**, **Current**, or **Residual**), and click **Done** to
generate the PDF report. Each cell shows the feared events at that
probability/severity intersection, color-coded by the configured risk level.
