# SV-Gap v0.3.0-alpha.8

This release adds the missing step between reading the Harbor experiment and
preparing a complete evidence contribution.

Researchers can now leave a short public report for a completed run, partial
run, setup blocker, counterexample, or disputed rule. A new Harbor guide keeps
the experiment, reporting path, and full submission workflow together. The
public collaboration pulse states the current evidence plainly and separates
author-run workflow demonstrations from independent replication.

After a successful `submission from-harbor` import, the CLI prints the number
of retained reports, simulation passes, and test-pass/rule-fail outcomes. It
also prints voluntary links for reporting or contributing the result. The CLI
still performs no telemetry or automatic upload.

The primary project metric is a complete, independently produced agent run
with inspectable evidence. Views, likes, stars, clones, and downloads remain
discovery signals rather than evidence of adoption.
