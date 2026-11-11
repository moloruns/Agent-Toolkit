# PokeJam comparison-quality proposal

Separate **closest available** (a ranking within the eligible pool) from **close comparison** (an absolute quality judgment). A winner always exists in a nonempty pool; a good comparison need not. This is implementation groundwork, not a finding about the current app.

## Recovered decisions

Evidence below comes from six genuine `prompt_history.search_prompt_history` MCP searches of PokeJam. Historical requests are evidence, not present authorization.

- The user asked how overall and style differ. The historical assistant described direct attribute distance versus mean-centered cosine similarity; that explanation is historical design context, not verified current code. [Lines 268–288](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L268-L288)
- The user subsequently rejected treating disparate players as one style, preferring specific traits. Mewtwo/LaMelo/Mitchell/Jrue were illustrative phrasing, not mandatory outputs. The later assistant’s bounded context discussed tiny deviations in nearly flat profiles being exaggerated by centering. [User, 310–316](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L310-L316); [context and assistant, 330–334](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L330-L334)
- Preserve shooting from Special Attack and Attack’s slashing role. Add layups from Attack plus Speed. Handles progressed from a 70/15/15 suggestion to the retrieved latest correction: 80% Speed, 20% Defense. Do not remap these to force familiar names. [419–421](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L419-L421), [490](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L490), [512](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L512), [531](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L531)
- A later request removed “built like” for NBA-to-Pokémon searches. Later still, the user cited Pichu/Quentin Grimes to request reasonable magnitude overlap and a no-match/closest fallback. This is a reported concern, not a reproduced output. [669–674](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L669-L674), [735–738](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L735-L738)

## Proposed policy

Compare mapped attributes on a shared, fixed scale. Rank whole profiles by magnitude-sensitive distance; proposed diagnostics are root-mean-square attribute gap, mean-level gap, and largest attribute gap. Shape similarity may explain relative strengths but cannot establish closeness or override substantial level differences. Never rescale each profile independently to award quality.

Apply a separately calibrated quality gate, independent of rank and pool size. If it fails, say “No close comparison in this pool. Closest available: X,” with the main attribute differences. If it passes, say “Close attribute-profile comparison: X.” Avoid implying identical real-world play or a probability of correctness. Show the pool/season so availability is interpretable. An empty pool yields no candidate.

For nearly flat profiles, suppress directional style claims; centered similarity is unstable, and exactly flat profiles have no defined centered cosine. Absolute closeness can still be excellent. Trait cards compare only their named attributes, receive their own quality assessment, and cannot imply whole-profile similarity. Scoring must include layups; retain the requested omission of “built like” in NBA searches.

## Calibration and uncertainty

`cases.json` provides synthetic design expectations, not historical NBA/Pokémon ratings or production cutoffs. Measure distance distributions, near-flat sensitivity, candidate-pool changes, and reviewed plausible/implausible pairs before setting thresholds or weights. Validate mapping transformations separately; do not tune mappings to rescue comparisons.

Searches used keyword OR matching and five-result limits; several truncated results, one empty search, and missing referenced screenshots limit coverage. Later corrections beyond retrieved excerpts remain possible. Current formulas, normalization, eligibility, trait groups, layup weights, and any implemented distance gate remain unverified. The historical 20 MPG/50 GP and rating ≥78 requests require reconciliation with the eventual data source. No app inspection or checker was performed.
