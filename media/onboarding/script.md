# From functional pass to production question in 90 seconds

Target duration: 85–95 seconds. Target narration: calm, direct, approximately
145 words per minute.

## Timed script and shot list

### 0:00–0:08 - Establish the problem

**Visual:** Repository headline and the `functional pass → evidence profile`
graphic. Slowly frame the words “passes the benchmark” and “reviewable.”

**Narration:**

> A generated RTL design can pass its functional test and still leave an
> important production question unresolved. SV-Gap makes that handoff visible.

**On-screen text:** `Functional pass ≠ production question answered`

### 0:08–0:19 - Show the bounded result

**Visual:** Controlled-result page. Frame the safe/unsafe witness table, then
the statement that the result is an existence demonstration rather than a
defect-rate estimate.

**Narration:**

> It preserves the functional result, adds declared design intent and
> structural evidence, and reports what is answered, failed, or still unknown.
> This is evidence accounting, not silicon signoff.

### 0:19–0:31 - Run the first profile

**Visual:** Clean terminal at `/tmp/svgap-video`. Run `svgap doctor`, then type
the quickstart command. Keep the prerequisite output visible briefly.

**Narration:**

> On a machine with the open RTL prerequisites already installed, one command
> creates a complete local evidence profile.

**On-screen command:**

```text
svgap study quickstart --output first-study
```

### 0:31–0:41 - Prevent a misleading interpretation

**Visual:** Hold on the terminal output. Frame `mode quickstart`,
`functional_pass 1`, `gap_members 1`, and the sentence identifying the fixture.

**Narration:**

> Quickstart uses a clearly labelled, known-unsafe bundled fixture. It validates
> the workflow; it is not a model result.

**On-screen text:** `Bundled fixture · not a model result`

### 0:41–1:02 - Read the evidence profile

**Visual:** Open `evidence-profile.html`. First frame “What this result means,”
then move to the answered and failed sections.

**Narration:**

> The supplied functional oracle accepted the candidate. The configured
> structural rule did not. The profile then names the failed production
> question: does this candidate satisfy the declared synchronous reset-release
> requirement?

### 1:02–1:14 - Make uncertainty actionable

**Visual:** Frame “Unanswered,” “What evidence to add next,” and the claim
boundary. Do not crop out the boundary.

**Narration:**

> Unknowns remain unknown, and the profile says what evidence could resolve
> them: review, repair, an independent backend, or approved adjudication.

### 1:14–1:25 - Connect a real model

**Visual:** Evaluate-your-model page. Frame the stdin/stdout contract and the
smoke-study command without showing credentials.

**Narration:**

> To evaluate your own model or agent, wrap it as one command: prompt on stdin,
> RTL on stdout. Start with one smoke task, inspect the same profile, then scale
> to the frozen protocol.

### 1:25–1:30 - Call to action

**Visual:** Return to the repository headline and show the public URL.

**Narration:**

> Bring one model output, or one production question your benchmark leaves
> unanswered.

**On-screen text:** `github.com/shsridhar-beep/svgap`

## Editorial constraints

- Do not show a model-provider identifier, API key, personal home directory,
  internal repository, proprietary RTL, or employer branding.
- Do not call the fixture a benchmark, baseline, model output, or safety proof.
- Do not display the perturbation instrumenter or imply that it is available.
- Do not claim a population defect rate, comprehensive CDC/RDC coverage, or
  silicon signoff.
- Keep the browser zoom high enough that the evidence question is readable on
  a phone-sized player.
