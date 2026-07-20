# SV-Gap v0.3.0-alpha.10

This release imports the project's first completed independent human-expert
review and lifts the hold that protected it.

An independent RTL engineer (10 years RTL design/verification, attested; no
dedicated CDC/RDC signoff background, also attested) reviewed the frozen
packet blind, without the checker. All five controlled witness pairs were
judged to support their stated rule distinction at high confidence, and all
three blinded generated candidates were labeled violations at high
confidence, in agreement with the frozen structural verdicts. On two
candidates the agreement extends to the root cause, including independent
identification of the synchronizer-bypass mechanism on a real study case.
The returned files ship verbatim under `artifacts/independent-review-v0.1/`,
hash-locked in issue #3 before import; a summary with the reviewer's
qualifiers, a disclosed mid-review clarification, and claim boundaries is in
the new "Independent review result" docs page. One reviewer and three
candidates establish concordance on this diagnostic selection, not reviewer
statistics or defect prevalence.

The release also documents the synchronizer-bypass pattern in the frozen
reset study: all 14 detected gap cases contain a recognized two-flop reset
synchronizer whose output feeds only synchronous data-path logic, never a
reset pin, while the flagged registers' asynchronous reset pins stay on the
raw net. `scripts/verify_synchronizer_bypass.py` recomputes this from the
frozen artifact without modifying it.

Smaller changes: an animated terminal demo above the README fold, a
scenario-to-rule mapping README for the examples, searchable phrasing in the
README and docs index openers, and removal of a stale project-status
disclaimer.
