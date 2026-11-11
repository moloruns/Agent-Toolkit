# Demonstration

The toolkit was used to produce improvement proposals and regression-case specifications for two existing projects: Game Finder and PokeJam. This was useful groundwork for later implementation. Neither live app was changed or executed.

Each producer used the MCP history tool. A separate fresh Codex session then loaded the checker skill and reviewed its artifacts. The reviews were repeated after checker revisions, using the same proposal files. [Session metadata](validation/session-summary.json) records distinct thread IDs, actual calls, and checks that the reviewed inputs stayed unchanged.

## Run A: Game Finder

**Task:** propose a general evidence policy for compound game recommendations, including partial matches, ambiguity, and exclusions. The producer created a [proposal](demos/run-a/proposal.md) and [26 synthetic case specifications](demos/run-a/cases.json).

One actual call from the [producer transcript, line 27](demos/run-a/producer/events.jsonl#L27):

```text
Tool: prompt_history.search_prompt_history
Arguments: {"project":"game_finder","query":"romance tragedy","speaker":"user","limit":5}
Result excerpt: "when i looked up something romantic, tragedy ending-- or something like that at least-- i got hello charlotte ep3, which has no romance."
Source: hw6_game_finder.md, line 359; speaker: user
```

The result excerpt is shortened from the recorded response. Other searches recovered the later instruction to fix the general ranking weakness rather than particular titles. The producer made 30 MCP calls; the final checker made six.

**What the checker caught:** the proposal explains which recommendations qualify, but still needs specifications for finding a strong candidate missed during retrieval, ordering several qualifying games, and avoiding repeated explanations.

From the [final review](demos/run-a/checker-v3/response.md):

> The proposed qualification mechanism generalizes beyond the examples. Whether it retrieves and orders the best batch remains unverified.

All four criteria received proposal-level PASS ratings in that final review. Those ratings do not establish working implementation behavior; the retrieval and ordering findings remain relevant.

**Author feedback:** after discussing the proposal and the criticism that it does not fully explain how to find and rank the best games, the author replied, “yeah both of those are good.” This confirms agreement with that main direction and finding, not a separate endorsement of every detailed rating.

## Run B: PokeJam

**Task:** propose a comparison-quality policy that separates closest available from genuinely close, preserves deliberate attribute mappings, and distinguishes individual traits from whole-profile similarity. The producer created a [proposal](demos/run-b/proposal.md) and [eight synthetic case specifications](demos/run-b/cases.json).

One actual call from the [producer transcript, line 9](demos/run-b/producer/events.jsonl#L9):

```text
Tool: prompt_history.search_prompt_history
Arguments: {"project":"pokejam","query":"comparison compare closest","speaker":"user","limit":5}
Result excerpt: "the comps should be within reason."
Source: hw5_pokejam.txt, line 737, within returned lines 735–738; speaker: user
```

The full returned passage discusses Pichu, Quentin Grimes, differences in attribute magnitude, and a no-match/closest-match fallback. Both the producer and final checker made six MCP calls.

**What the checker caught:** ranking and quality gates can disagree. If the nearest candidate fails a maximum-gap check, a slightly more distant candidate might still pass. The proposal needs to resolve that before declaring that the entire pool contains no close match.

From the [final review](demos/run-b/checker-v3/response.md):

> rejecting the winner may not justify rejecting the pool.

The final ratings were PASS for intent, varied cases, and calibrated claims, with UNKNOWN for the general mechanism because that decision remained unresolved.

**Author feedback:** after discussing the policy and this main criticism, the author replied, “sure this works.”

## What these demonstrations establish

The agents called the real MCP tool, the checker loaded in separate sessions, and the reports identified gaps beyond the original examples. The final reviews also separated minimum case coverage from additional improvements. The author agreed that this distinction made sense.

These were unexecuted design specifications, not application regression results. The runs used the same Codex setup rather than a cross-model comparison. Full prompts, unedited events, and reports are retained under [run A](demos/run-a/) and [run B](demos/run-b/); checker revisions are explained in [ITERATION.md](ITERATION.md).
