# Repository-level production-risk review

Brief answers are sufficient. Please focus on material risks rather than copy
editing.

## 1. Are the production questions legitimate?

Do the five controlled rule families and selective-reset questions correspond
to real concerns in production RTL review? Which are misstated, oversimplified,
or missing essential qualifiers?

[Seshu] Yes, they all are real issues. 

REF-CDC-001	- Whether a 2D sync cell is sufficient or not depends on many things (we might need a 3d sync cell or some kind of feedback in many cases)
REF-CDC-002	 - The user has to assume that the co-operands are timed synchronously 
REF-CDC-003	 - The user has to assume that it is ok if the receiver skips values.
REF-RDC-001	-  We don’t know where the arst_n is coming from, so the reset synchroniser may or may not be needed 

## 2. Is the declared intent sufficient?

What additional intent would normally be required to judge these properties—for
example clock relationships, reset architecture, power domains, technology
target, synchronizer constraints, protocol validity, waivers, or initialization
assumptions?

[Seshu] No, Apart from all the ones that are already mentioned, we need to know more about the functionality (like is it ok to miss packets in case of multi bit async crossing). Another requirements one can think of is MTBF target. 

## 3. Is abstention handled correctly?

When should this evaluator return `unknown` instead of `pass` or `fail`? Identify
the most dangerous ways it could create false confidence.
[Seshu] It should return unknown when the design intent is not clear to the system. 
For example, if the model does not know the type of reset is input. The most dangerous ways it creates false confidence is if it does not fully understand the request, makes common assumptions and returns a "pass". If this code also passes simulation it can lead to issues in real hardware (async crossing and reset being the most common ones) 

## 4. What does a clean result safely mean?

Give the strongest wording you would accept for a clean report from this narrow
checker, and wording you would reject as overstated.
[Seshu] Accept can be put something like - "For the requested intent, the checker found no instance of violation of specific rule patterns it inspects."

overstated might be something like : "CDC/RDC clean" or "no hardware issues." The danger is precisely that a designer reads a bare pass as "the AI considered everything." 

## 5. Is the finding evidence actionable?

What must a finding contain for an RTL designer to investigate it efficiently?
Consider source locations, signal paths, domains, reset polarity/value,
schematics, constraints, traces, waivers, and tool provenance.
[Seshu] : A designer would need to know which rule failed and what the violation means (details like why it is considered an issue). The failing source file and line number of this violation. Apart from that, depending on the violation type, contextual information should be provided. For example, if it's a CDC issue, details about the clock domains involved. 


## 6. What evidence must follow before deployment?

After functional tests and these structural checks, name the most important
remaining verification or review steps. Which should SV-Gap represent as
explicit unanswered questions?
[Seshu] After functional and structural checks, we would review the test bench functional coverage. And still all checks like CDC checks, Reset checks,spyglass, X-prop simulation, formal verification.  We should still run everything because AI today is not 100% deterministic and checks reviews should be done. 
For explicit unanswered questions, it can explicitly mention the things that it cannot resolve unless a tool is run (like timing analysis). 


## 7. Checker coverage and failure modes

Which ordinary RTL structures are likely to fool a small Yosys-netlist
recognizer—for example gated/inverted resets, generated clocks, synchronizer
variants, handshakes, reconvergence, memories, declaration initialization,
hierarchy, or synthesis transformations?
[Seshu] Hard macros like SRAMs are likely to fool it. 


## 8. Research-to-production usefulness

Would preserving the functional result while listing answered, failed, and
unanswered production questions improve the handoff from benchmark research to
an RTL team? What would make the profile actionable rather than report noise?
[Seshu] Yes, it's important for a RTL engineer to know what questions were asked and what is the reason behind an answer. This is so they can review and feel confident about the analysis. For the report, I think it's important to have precise details rather than high level generic statements. 

## 9. Highest-priority change

If the project could make only one technical or methodological improvement
before broader use, what should it be?
[Seshu] I have not used SV Gap yet to comment on this. 
