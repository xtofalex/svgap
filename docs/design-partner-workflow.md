# Research design-partner workflow

The SV-Gap design-partner workflow is for frontier-model researchers and
applied chip-design AI teams that want to turn one research-to-production
handoff problem into a reproducible public experiment. It is not consulting,
signoff, or an invitation to disclose internal designs.

## What a partner can build

A partner starts with one question that a functional RTL evaluation leaves
unanswered. Useful outcomes include:

- a model-generation profile that separates functional acceptance, structural
  evidence, unknowns, and tool errors;
- a diagnosis study testing whether an agent requests missing intent instead of
  inventing it;
- a repair study testing finding removal without functional or structural
  regression;
- an intent-bearing public task derived from a recurring handoff question;
- an adapter that binds an existing benchmark result to the evaluated RTL; or
- an independent checker comparison or disputed-finding case.

The first outcome should be the smallest result that another team can inspect
or reproduce, not a broad integration commitment.

## Entry criteria

The workflow is a fit when:

1. the question concerns AI-generated digital RTL or its digital verification
   evidence;
2. the first experiment can use public, redistributable, or synthetic inputs;
3. the intended claim can be stated without confidential organizational facts;
   and
4. at least one partner can review the protocol, evidence, and interpretation.

Private model names and internal harness details are not required. Stable
attested aliases and non-comparative case studies are supported. Proprietary
RTL and unapproved internal tool output must not enter the repository.

## Four bounded stages

### 1. Research scoping call

In 30 minutes, identify:

- the downstream decision the current functional result cannot support;
- the minimum public or synthetic artifact that represents the problem;
- whether SV-Gap can answer, contradict, or only expose the missing question;
  and
- the smallest result worth producing next.

The call ends with a go, revise, or out-of-scope decision. Continuing is
optional.

### 2. One-page experiment contract

Record the research question, task or input, evidence sources, success and
abstention conditions, provenance, claim boundary, expected public artifact,
and owner for each next action. Freeze claim-bearing choices before running the
experiment.

### 3. Minimal reproducible run

Run one smoke profile, one diagnosis/repair starter, one checker comparison, or
one public task. Preserve failures, unknowns, and disagreements. Expand only
after the minimal run establishes that the question is measurable.

### 4. Evidence and continuation decision

Produce a citable evidence profile, scoped case note, task or adapter RFC, or a
documented negative result. Then decide whether to stop, replicate, expand the
taskpack, or pursue a broader integration.

## Credit and research integrity

Design-partner participation is not itself contributor credit. Named repository
credit follows an accepted, attributable contribution such as protocol design,
a redistributable model result, task design, analysis, validation,
documentation, or code. The contribution and any material AI assistance are
recorded explicitly.

Paper authorship is decided separately using the target venue's policy and
requires substantive intellectual contribution, drafting or revision, approval
of the submitted work, and accountability. Affiliation or access alone is not
authorship.

## Start

[Request a research scoping call](https://github.com/shsridhar-beep/svgap/issues/new?template=collaboration.yml).
Use only public, non-confidential language in the intake. The maintainer will
acknowledge a scoped request within two working days and coordinate scheduling
separately. Researchers who received a direct invitation may instead reply in
that private channel with “SV-Gap research call” and a one-sentence question;
the public intake is optional.
