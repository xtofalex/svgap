# Starter issue drafts

## 1. [Add a second open-source SystemVerilog frontend](https://github.com/shsridhar-beep/svgap/issues/1)

Evaluate a maintained open-source frontend that accepts the function and enum
syntax currently rejected by Yosys/Icarus. Document its license, normalized
failure states, source-location behavior, and differential results on all
controlled fixtures. Do not silently convert frontend failures into passes.

Acceptance criteria: backend capability probe, stable normalized statuses,
paired-fixture regression tests, third-party license entry, and a limitations
section comparing results with `reference-yosys`.

## 2. [Export normalized findings as SARIF and static HTML](https://github.com/shsridhar-beep/svgap/issues/2)

Add deterministic SARIF output for CI annotations and a dependency-light static
HTML summary for research artifacts. Preserve `unknown` and `tool_error` as
first-class states and add golden-file tests.

Acceptance criteria: versioned output contract, deterministic golden fixtures,
escaped untrusted RTL/evidence text, and one documented GitHub Actions example.

## 3. [Import blinded expert adjudication](https://github.com/shsridhar-beep/svgap/issues/3)

Implement a command that validates completed review CSVs, joins them to a private
case mapping, reports pre-reconciliation inter-reviewer agreement, and lists all
oracle disagreements. Never expose model identity in reviewer-facing output.

Acceptance criteria: schema validation, duplicate/missing-case rejection,
pre-reconciliation Cohen/Krippendorff agreement, unresolved-case preservation,
and tests proving that the public output contains no private mapping fields.

## 4. [Build reset taskpack v0.2](https://github.com/shsridhar-beep/svgap/issues/4)

Resolve the timer output ambiguity in a new version rather than editing v0.1,
add executable safe/unsafe references for each task, and expand task diversity.
Preserve the v0.1 digest and report both original and sensitivity analyses.

Acceptance criteria: immutable v0.1 replay, new canonical digest, executable
references for every task, documented ambiguity resolution, and a side-by-side
sensitivity table rather than a retroactive replacement of v0.1 results.
