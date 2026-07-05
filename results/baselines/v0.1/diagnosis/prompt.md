# Diagnosis prompt

The model receives this normalized evidence:

- the supplied functional oracle reports `pass` and records executed Icarus
  commands;
- the configured `reference-yosys` structural backend reports `fail` with
  `REF-RDC-001`, stating that raw asynchronous reset reaches operational state
  although synchronized deassertion is required; and
- configured checks cover only declared rules and are not silicon signoff.

It must classify exactly three questions from
`challenges/v0.1/diagnosis/task.json` as `answered`, `failed`, or `unanswered`,
provide evidence text, and name next evidence for any unanswered question.

Model tools are disabled. Only the normalized response is retained.
