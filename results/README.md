# Public result registry

SV-Gap records **evidence profiles**, not a single leaderboard score. The
registry makes generation, diagnosis, and repair results inspectable without
implying that one narrow open-source checker measures overall RTL quality.

The checked-in [`registry-v1.json`](registry-v1.json) currently contains:

- aggregate profiles for the frozen 72-call reset-generation artifact;
- scored diagnosis runs that test whether a model preserves the distinction
  between contradicted and unanswered production questions; and
- scored repair runs that test whether a finding is removed without functional
  or structural regression.

The exploratory diagnosis and repair baseline is intentionally small: two model
configurations from one provider, one prompt, and one run per configuration.
It demonstrates the contract and exposes contrasting failure modes. It is not a
model comparison study.

## Reproduce

```bash
python scripts/build_adoption_baseline.py --check
python scripts/verify_result_registry.py
```

To reproduce the repair evidence itself, install Yosys and Icarus Verilog and
run `svgap check` on each before/after manifest in
[`baselines/v0.1/repair`](baselines/v0.1/repair/).

## Contribute a result

Follow the [result-submission guide](../docs/submitting-results.md) to create a
content-addressed directory, choose a provenance level, run a private
publication denylist, and produce a deterministic bundle.

1. Start with a task under [`challenges/v0.1`](../challenges/v0.1/).
2. Preserve the model identifier, run identifier, exact prompt, decoding
   settings, tool access, and execution environment in provenance.
3. Score with `svgap challenge-score` and retain the complete profile.
4. Run `svgap submission init`, `svgap submission validate`, and optionally
   `svgap submission bundle`.
5. Open a pull request adding the immutable directory beneath
   `results/submissions/`. The registry discovers valid submissions
   automatically.

Cross-vendor replications, failures, abstentions, and disputed checker results
are especially valuable. Do not include private RTL, proprietary tool output,
or data you cannot redistribute.

## Interpretation boundary

These profiles describe submitted digital RTL evidence under configured
open-source checks. They do not establish silicon safety, signoff readiness,
population defect rates, or general model rankings.
