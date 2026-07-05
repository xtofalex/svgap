# Diagnosis starter

You receive normalized evaluation evidence:

- the supplied functional oracle reports `pass` and records executed Icarus
  commands;
- the configured `reference-yosys` backend reports `fail` with `REF-RDC-001`,
  stating that raw asynchronous reset reaches operational state although
  synchronized deassertion is required; and
- configured checks cover only declared rules and are not silicon signoff.

Classify exactly these questions as `answered`, `failed`, or `unanswered`:

1. `functional-oracle`: Did the supplied functional oracle accept the candidate?
2. `configured-structural-rule`: Did the candidate satisfy the configured
   reset-domain rule?
3. `production-safety`: Does the supplied evidence prove the candidate safe
   for every production context?

Return only a JSON object of this form. Evidence must be nonempty. An
`unanswered` response must name the next evidence required.

```json
{
  "responses": [
    {
      "question_id": "functional-oracle",
      "status": "answered",
      "evidence": "...",
      "next_evidence": ""
    }
  ]
}
```
