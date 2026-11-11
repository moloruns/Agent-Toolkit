# Iteration

## Main issue: inconsistent case-coverage ratings

The checker was supposed to distinguish a proposal's minimum case coverage from proof that the implementation works. Version 2 blurred that distinction during the PokeJam review.

Its [varied-cases finding](demos/run-b/checker-v2/response.md) stated:

> Ordinary, different-combination, and no-good-match specifications are present.

Despite acknowledging all three required categories, it marked coverage UNKNOWN because it wanted additional boundary and trait-selection cases. Version 1 had marked the same coverage PASS. The proposal files had not changed.

**Diagnosis:** the skill named statuses but did not define their meaning precisely enough for each criterion. This let the reviewer raise the minimum standard during the review. Missing execution evidence and opportunities for extra tests also became mixed with the narrower question of whether the required proposal cases existed.

**Change:** [version 3](versions/fix-the-pattern-v3/SKILL.md) added criterion-specific status rules. In proposal mode, varied cases receive PASS when the three minimum categories have inputs, expected judgments, and rationale. Extra cases remain recommendations. Implementation behavior still requires execution evidence and otherwise stays UNKNOWN.

**Rerun:** fresh sessions reviewed both unchanged proposals again. In the final [PokeJam review](demos/run-b/checker-v3/response.md), minimum case coverage passed while the unresolved relationship between ranking and quality gates remained UNKNOWN under general mechanism. The final [Game Finder review](demos/run-a/checker-v3/response.md) also passed minimum coverage and retained additional findings about retrieval and ranking.

After this distinction was explained, the author replied, “yes it does. that works.” These two reruns show an improvement, not a guarantee of consistent judgments on every task. Game Finder's mechanism rating also changed across versions as reviewers interpreted the proposal's scope; the detailed findings are more informative than the status alone.

## Earlier refinement: explain missing-case recommendations

Version 1 requested a proportional-profile test without explaining its relationship to an existing same-shape, different-level case. This was not established to be a false finding: an additive shift and proportional scaling are different inputs. The problem was an unclear recommendation.

[Version 2](versions/fix-the-pattern-v2/SKILL.md) required the checker to inspect the case inventory, cite the closest existing case, and explain the distinct behavior still needed. Later reports did this more clearly. The [observation record](validation/checker-iteration/observation.md) preserves the before, change, and results.

## MCP retrieval failure

A separate test exposed a concrete search failure. For `specific examples` in Game Finder, the first search version ranked an initial app-choice message matching only `specific` above the later correction matching both words.

The revision prioritizes passages covering more query terms, then consecutive phrase matches, with FTS relevance as a tie-breaker. It also chooses a shortened excerpt around the relevant phrase. The same query then returned the general-fix instruction at line 416.

Evidence: [before](validation/retrieval-iteration/before.json), [failing regression](validation/retrieval-iteration/failing-test.txt), [after](validation/retrieval-iteration/after.json), and [preserved earlier source](versions/history-v1/). The saved final [test run](validation/checks/tests.txt) passed all 15 tests. No historical source logs were modified.
