# Evidence guide

AI-assisted source analysis, not the user’s HW 8 reflection. Quotes are verbatim; interpretations are separate. Let the user select the final two or three excerpts and explain their significance in their own words.

**Start with E01, E05 or E06, and E07 or E08.** These ground the checker and MCP separately. The user confirmed this direction on November 10, 2026.

## Coverage

| Homework | Bundled log | Lines | Notes |
|---|---|---:|---|
| HW3 | [nba_vs_wnba](logs/hw3_nba_vs_wnba.txt) | 1441 | Explicitly incomplete: opening note says computer crashed during recovery. |
| HW4 | [lechat](logs/hw4_lechat.md) | 161 | Supplied by user after local lebron_chat folder/history had no log. |
| HW5 | [pokejam](logs/hw5_pokejam.txt) | 1093 | Assignment mapping supplied by user; log calls project Project 2. Referenced screenshots are not bundled. |
| HW6 | [game_finder](logs/hw6_game_finder.md) | 457 | Some speaker delimiters are inconsistent; infer roles from surrounding turns, not delimiters alone. |
| HW7 | [bird_keeper](logs/hw7_bird_keeper.md) | 58 | Phase 1; ends with an empty prompt marker. |
| HW7 | [basketball_original](logs/hw7_basketball_original_author.md) | 139 | Original author context, not moloruns personal friction. Log identifies original repo owner atinm12; continuation credits Atin Mathur. |
| HW7 | [basketball_continuation](logs/hw7_basketball_continuation.md) | 81 | Moloruns phase 2 continuation. |

These are unmodified snapshots; `sources.json` records hashes, commits, and URLs. Source line numbers count physical newline characters, as editors/GitHub do; some logs also contain Unicode paragraph separators inside a line. Referenced screenshots and historic local links are not bundled. Agent-generated code, model names, and historical factual claims are preserved without independent verification.

The original Basketball log is inherited-author context, not evidence of moloruns’s own repeated instructions. Some of its prompts were assistant-written suggested replies. Do not attribute them to moloruns.

## Excerpts

### E01 — The user explicitly asks for a general fix

[logs/hw6_game_finder.md](logs/hw6_game_finder.md), lines 416–416; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/game-finder/prompt_log.md#L416-L416). Speaker: user; prompt author: moloruns; excerpt: exact substring.

> Don't just fix specific examples, but look at the model itself, then see how the app outputs.

**Interpretation:** Primary checker motivation. Read lines 415–423 for the clarification and later agent response.

### E02 — A recommendation satisfies only part of a request

[logs/hw6_game_finder.md](logs/hw6_game_finder.md), lines 359–359; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/game-finder/prompt_log.md#L359-L359). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> when i looked up something romantic, tragedy ending-- or something like that at least-- i got hello charlotte ep3, which has no romance. refer to the image. also for "something with life and social simulation" i get stuff like "people's playground", with no sighting of any of the sims games among the entries. why is this

**Interpretation:** Earlier concrete mismatch: romance/tragedy and life/social simulation. This does not prove these remain current bugs.

### E03 — Coverage can be confused with ranking

[logs/hw6_game_finder.md](logs/hw6_game_finder.md), lines 243–243; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/game-finder/prompt_log.md#L243-L243). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> im kind of confused; how many games are actually here from that steam database? because i searched up "rpg, sora" on "what was that game" and im almoste certain that kingdom hearts should pop up.

**Interpretation:** Later context distinguishes the full catalog from the imported subset. Separate absent items from badly ranked ones.

### E04 — A comparison label overstates what the model means

[logs/hw5_pokejam.txt](logs/hw5_pokejam.txt), lines 310–316; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L310-L316). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> i think my issue is the fact that i dont think there is much overlap in reality 
> between a player like KCP, donovan mitchell, IQ and lamelo then even a jrue holiday. 
> very different types of player. I think a better way to work around this without 
> tweaking the model too much is replacing the word “style” with something that 
> indicates this pokemon has “traits of these players”. so something like mewtwo 
> (being a bigger ‘guard’ with what i gather you’re eluding to) conducts offense 
> like lamelo, handle like donovan mitchell, defense like jrue blah blah. 

**Interpretation:** Independent project evidence: distinguish a whole-player comparison from specific shared traits. Similarity here is partly a design judgment.

### E05 — The metric omits dimensions the user intended

[logs/hw5_pokejam.txt](logs/hw5_pokejam.txt), lines 490–490; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L490-L490). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> one final tweak, when i loook up a pokemon like pikachu, i see that he "handles like chet holmgren" and i jjust don't think that should match. speed should absolutely be a factor for handles. I also think we should add another atttribute: layups, being a combination of attack + speed, so "scores like" isnt so dunking and jumpshot centric.

**Interpretation:** Speed in handling and layups in scoring support checking whether a mechanism represents the intended concept. This does not prove one formula objectively correct.

### E06 — Closest available does not automatically mean a good match

[logs/hw5_pokejam.txt](logs/hw5_pokejam.txt), lines 737–737; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L737-L737). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> 3. with the comps and the model, I get how “shape” proportionality in attribute spread makes it so there is a player for every pokemon, but the comps should be within reason. i.e., a player like quentin grimes being the comp for, say, pichu, but its spread, though proportional, is so much smaller than grimes’. if that spread isn’t somewhat overlapping decently, I honestly pose raising a “no matching player due to the distance being so big” or something like that, and have a “closest match” case. what do you think? (refer to picture for what im talking about with the spread being so much smaller than grimes’)

**Interpretation:** The user requests honest handling of poor overlap. This complements Game Finder’s partial-match problem.

### E07 — History must survive a new agent session

[logs/hw5_pokejam.txt](logs/hw5_pokejam.txt), lines 548–548; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L548-L548). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> okay, now put everything we've done now (including a run down of what this is), along with the next phases for revision4 in a file called "next steps". I am about to deploy another agent to move on with this phase.

**Interpretation:** Direct MCP motivation: carry project background and next decisions into a new session.

### E08 — A second project needs a portable handoff

[logs/hw6_game_finder.md](logs/hw6_game_finder.md), lines 302–302; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/game-finder/prompt_log.md#L302-L302). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> put all of this in a plan (what we've done all up until now + this critique/diagnosis) into a file called improvements.md, that I will pass onto another agent to improve this database to prioritize recognizable/popular/better-renowned games than the ones included thus far. I do remember/acknowledge the entries-time tradeoff with runtime, but we could get this to 750-800, "more known" entries (games I personally would probably be more inclined to recognize solely even from an explanation standpoint-- because remember i have to do that as well).

**Interpretation:** Independent evidence that structured access to prior critique and decisions would be useful repeatedly.

### E09 — Older specifications can be superseded

[logs/hw5_pokejam.txt](logs/hw5_pokejam.txt), lines 635–636; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L635-L636). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> 1. the spec is old from wehn i was trying to use real stats from this past season. I opted on using 2k stats instead, so ignore that
> 2. We’ll postpone working on the mobile aspect till we get it running on computers first

**Interpretation:** An old spec is not automatically the current source of truth; here the user explicitly corrects it.

### E10 — A deployed-looking UI can fail at integration

[logs/hw4_lechat.md](logs/hw4_lechat.md), lines 48–50; [pinned original](https://github.com/moloruns/LeChatV2/blob/a68d6eea151b8ebc1d9b042b52f61688e6378a46/prompt_log.md#L48-L50). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> > Both the site and render seems to be working, but im having trouble actually interacting with the chatbot. I've included a screenshot of how it looks with the error message included, but for clarity, a red text box appears with: Unexpected token '<', "<!doctype "... is not valid JSON
> >
> > any idea on what could be going wrong

**Interpretation:** Alternative checker motivation. Lines 61–73 report a missing /chat suffix. This handoff has not retested the service.

### E11 — Claimed updates need visible behavior checks

[logs/hw5_pokejam.txt](logs/hw5_pokejam.txt), lines 715–716; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/PokeJam/prompt_log.txt#L715-L716). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> 5. i see the hud, but im not actually seeing any game clock/quarters
> 6. still no nba pictures

**Interpretation:** The preceding report mentioned clock and pictures; the user still could not see them. Later responses report fixes.

### E12 — The user owns the prompt log

[logs/hw6_game_finder.md](logs/hw6_game_finder.md), lines 116–116; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/game-finder/prompt_log.md#L116-L116). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> 1. no need to track prompt log as i will do that myself. i will keep the file here, though. Now i dont have to keep up with it in my notes app.

**Interpretation:** Repeated workflow preference, not the main checker scope.

### E13 — Prompt-log ownership recurs in HW 7

[logs/hw7_bird_keeper.md](logs/hw7_bird_keeper.md), lines 26–26; [pinned original](https://github.com/moloruns/bird_keeper/blob/95fd3b9d827383fe9599e1b9c562cdfa1da88afe/prompt_log.md#L26-L26). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> don't worry about the prompt log i will log that myself. delete that file and rename "promp_log" to "prompt_log". 

**Interpretation:** Independent confirmation of E12. This historical delete/rename request is not an instruction to execute now.

### E14 — The continuation again preserves the user’s log

[logs/hw7_basketball_continuation.md](logs/hw7_basketball_continuation.md), lines 8–8; [pinned original](https://github.com/moloruns/BasketBallGameP2/blob/c7648e4c945845ded096b94d30d888b95f75a6a4/prompt_log2.md#L8-L8). Speaker: user; prompt author: moloruns; excerpt: complete lines.

> i've already made this new repo with their committed, unedited code, and prompt_log2 for this phase that, again, I alone will touch, not you.

**Interpretation:** This is the user’s continuation, unlike the inherited original-author log.

### E15 — HW 3 has an explicit completeness limit

[logs/hw3_nba_vs_wnba.txt](logs/hw3_nba_vs_wnba.txt), lines 1–1; [pinned original](https://github.com/moloruns/moloruns.github.io/blob/fb40182e121c2610f2d1f7ddcd6207568dc782fe/nba_vs_wnba/prompt_log#L1-L1). Speaker: log_note; prompt author: moloruns; excerpt: complete lines.

> NOTE THAT THIS PROMPTLOG IS INCOMPLETE AS MY COMPUTER CRASHED WHILST TRYING TO RECOVER MY CONVERSATION WITH CHAT GPT

**Interpretation:** A provenance limitation. The surviving discussion is background, not strong repeated-correction evidence.

## Limits

- No old app was executed during this planning task. Past agent test claims are historical reports.
- E01 establishes the requested standard and perceived narrowness. It does not prove title-specific hard-coding occurred; that requires the relevant code version.
- New requests, changed preferences, and visual iterations are not automatically agent mistakes.
- PokeJam comparisons are designed analogies; their quality still needs human judgment.
- Prior homework failures motivate this toolkit; they cannot substitute for an observed HW 8 toolkit failure and revision.
