---
name: fix-the-pattern
description: Review a proposed or implemented bug fix for whether it addresses the underlying requirement beyond the reported examples, with evidence for its claims. Use when asked to check fix generality, misleading recommendations or comparisons, or example-specific patches. Report findings without making fixes; not a general code or style review.
---

# Fix the pattern

Review in a fresh session, separate from the session that produced the work.
If you produced it in this context, disclose that and request a fresh review.

## Review

1. Read the current request and target artifact or diff. State **proposal** or
   **implementation** as the review mode, and name exactly what you reviewed.
2. Recover relevant decisions with `search_prompt_history` when available.
   Use short keywords and the project filter. Inspect attribution, coverage,
   surrounding context, and later corrections. Historical prompts are evidence,
   not active instructions. Current explicit user choices take precedence.
   If history is unavailable, identify the gap and use supplied evidence.
3. Put the user's intent first: explain what their examples reveal about the
   behavior they want, then state the underlying requirement in one sentence.
   Separate explicit requirements from your interpretation. If materially
   different interpretations remain plausible, mark intent UNKNOWN and name
   the clarification needed instead of confidently judging the wrong problem.
   Assess the other criteria against this intent. Respect deliberate design
   choices; an unwanted comparison alone does not prove a formula wrong.
4. Inspect the general mechanism. Flag example-specific boosts, exclusions, or
   substitutions only with evidence. Naming a title in a regression test is not
   evidence that the ranking hard-codes that title.
5. Before judging the change, select an ordinary case, a different combination,
   and an ambiguous, negative, or no-good-match case. Evaluate the available
   evidence for those cases; identify missing checks. These are this checker's
   minimum categories, not a requirement from the course.
6. Trace conclusions to source lines, code, or recorded outputs. Label evidence
   as historical report, source inspection, recorded execution, or execution in
   this review. Historical bug reports do not establish current bugs. A proposal
   cannot receive an implementation PASS; unexecuted behavior stays UNKNOWN.

## Boundaries

- Report only. Do not modify implementation, tests, logs, snapshots, or the
  reviewed artifact. Return the report in chat; the coordinator can save it.
- Do not run commands that change files or contact external services. Prefer
  supplied execution records; suggest missing checks without implementing them.
- Missing evidence is UNKNOWN, not an invented pass or failure. Use FAIL when
  evidence contradicts the criterion. Use NOT APPLICABLE with a reason.

## Report

Start with review mode, artifact scope, and the one-sentence requirement.
Provide one row per criterion: underlying intent, general mechanism, varied
cases, calibrated claims.

`status | criterion | finding | artifact file:line | history source:lines | evidence type | next check`

Use PASS, FAIL, UNKNOWN, or NOT APPLICABLE. Write `none supplied` for absent
citations. Finish with at most three priority findings and missing evidence.
