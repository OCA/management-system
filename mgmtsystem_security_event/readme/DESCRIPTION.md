This module allows you to manage **feared events** (security incidents) of your
Information Security Management System (ISMS) and assess their risk using a
configurable risk matrix.

Key concepts:

- **Feared Events** — Security incidents that could impact your organization,
  each classified by the security properties they threaten: Confidentiality,
  Integrity, and/or Availability (CIA triad).

- **Attack Vectors** — The means by which a threat could materialize. Each
  vector carries three risk ratings (probability × severity): *Original* (before
  any control), *Current* (with controls already in place), and *Residual* (after
  planned remediation). A feared event's overall rating is automatically computed
  as the maximum across all its vectors.

- **Scenarios** — Links between a feared event, an attack vector, and a threat
  source, with a description of how the attack could unfold.

- **Threat Sources** — The origin of a threat (e.g. external attacker, malicious
  insider, compromised supplier).

- **Security Controls** — Countermeasures applied to reduce risk, each flagged as
  *Prevention*, *Protection*, and/or *Recovery*.

- **Assets** — Primary assets (the information or processes to protect) and
  Supporting assets (the infrastructure that hosts them), organized by category.

- **Risk Matrix** — A visual heat-map report that plots feared events by
  probability and severity for a chosen risk type (original, current, or
  residual), with color-coded cells (green / orange / red).
