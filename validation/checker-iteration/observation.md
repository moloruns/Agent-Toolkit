# Observed checker weakness — AI working note

Input: unchanged `demos/run-b/proposal.md` and `cases.json`.
First review: `demos/run-b/checker-v1/response.md`, priority finding 2:

> Missing evidence includes borderline overlap, a large single-attribute mismatch, and proportional profiles at different magnitudes.

The existing `same_shape_different_levels` case at `cases.json:17` adds 60 to
every attribute. Its centered shape is identical. A raw multiplicative profile
would be a distinct case, so the review's proportional-profile request is **not
established to be a false positive**. The observed weakness is that the report
does not identify the existing case or explain this distinction, making its
missing-evidence recommendation unnecessarily ambiguous to the user.

Revision: the checker now requires a full inventory check before a missing-case
claim, a citation to the closest existing case, and an explanation of the distinct
input or expected behavior still needed. It also distinguishes an absent case
from a case that exists but has not been executed.

The revised checker is preserved in `versions/fix-the-pattern-v2/SKILL.md`.
Both reviews will rerun on unchanged artifacts with the same prompts in new
sessions; no expected verdict or prior report is supplied to the reviewers.
Use the actual resulting reports to assess the effect, not this proposed outcome.

Separately, `validation/retrieval-iteration/` records a stronger, deterministic
MCP retrieval failure: a one-keyword match outranked the passage matching both
query words. The real failing test and corrected result are preserved.

## Result of v2 and a second observed weakness

`demos/run-b/checker-v2/response.md` now identifies the existing
`same_shape_different_levels` fixture and explains the missing conflicting-error
pattern. Its trait recommendation likewise names the existing single-candidate
case and specifies the additional independent-winner/fallback behavior. This
supports improvement on the original report-precision issue in one rerun.

However, its varied-cases row is UNKNOWN even while explicitly stating that
ordinary, different-combination, and no-good-match specifications are present.
V1 had marked that same coverage PASS. Both reports correctly refrain from
claiming execution. V2 instead lets additional boundary tests change the minimum
proposal-coverage judgment. This shows that the generic status definitions leave
too much room to change the standard while reviewing.

V3 will define criterion-specific status anchors: proposal case coverage checks
the three minimum categories with explicit inputs/expectations/rationales;
additional coverage suggestions remain findings. Mechanism completeness and
implementation execution are assessed separately. This is a general scoring
clarification, not an instruction to produce a particular verdict for either demo.
The same unchanged artifacts and prompts will be reviewed again in fresh sessions.

## Observed v3 rerun results

- `demos/run-b/checker-v3/response.md` marks minimum case coverage PASS and
  explicitly states that extra cases supplement it. The unresolved relationship
  between ranking and quality-gate rejection remains UNKNOWN under mechanism.
  Its proposed competing-trait-winner case cites the existing single-candidate
  fixture and explains the distinct behavior to test.
- `demos/run-a/checker-v3/response.md` also marks minimum case coverage PASS and
  names the closest existing cases for each additional recommendation. It gives
  the qualification mechanism a proposal-level PASS while retaining unresolved
  retrieval and ordering findings. Earlier versions used UNKNOWN for mechanism;
  this remaining scope judgment should be assessed by the human, not treated as
  a guaranteed objective score.
- Both reviews retain the distinction between synthetic specifications and
  execution. Both made six real MCP searches, read the installed skill, and
  left all reviewed artifacts, skills, and source snapshots unchanged.
- The session metadata and `validation/session-summary.json` verify distinct
  fresh thread IDs. These two reruns show the observed improvement; they do not
  establish perfect reliability across all models or tasks.

Subsequent author feedback is recorded in the AI-assisted `DEMONSTRATION.md`
and `ITERATION.md` drafts: the author agreed with the two main demonstration
findings and with separating minimum coverage from additional improvements.
This does not establish agreement with every detailed finding or rating.
