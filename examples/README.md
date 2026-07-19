# Examples

Five controlled witness pairs plus two supporting folders. Each witness
family holds a `safe/` and an `unsafe/` variant that share the same
testbench (`tb.sv`): both variants pass functionally, and only the
structural oracle splits them. The `unsafe` variant fails with exactly one
expected reference rule.

## Scenario-to-rule mapping

| Folder | Scenario | Rule fired by `unsafe/` |
|---|---|---|
| `level_crossing` | Stable level crossed by direct asynchronous sampling, no second destination stage | `REF-CDC-001` |
| `comb_crossing` | Combinational logic immediately before an otherwise recognized synchronizer | `REF-CDC-002` |
| `gray_counter` | Multi-bit crossing synchronized bit-by-bit without a Gray-code protocol | `REF-CDC-003` |
| `reset_release` | Raw asynchronous reset on unmarked state where the manifest requires synchronous deassertion | `REF-RDC-001` |
| `power_on_x` | Un-reset state reaching a module output where the manifest declares power-on reset coverage | `REF-XPROP-001` |

The rule IDs belong to the built-in reference oracle; full definitions are
in `docs/architecture.md`, the scenario table is in
`docs/research-protocol.md`, and the mapping is enforced by
`tests/test_examples.py`. Each `unsafe/build/report.json` carries its
`rule_id` directly, so `grep rule_id examples/*/unsafe/build/report.json`
reproduces this table from the artifacts.

## Supporting folders

- `adjudication_calibration/`: calibration packets for blinded adjudication
  (see its own README).
- `imported_result/`: a worked example of importing an externally produced
  functional result instead of running the shipped testbench.
