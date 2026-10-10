# Test plan: proving the system works in general

Two cases in the **same mall and cameras**, with different families, clothing colours, times, causes of separation, walking directions and end places. Each case also has a **trick clip**.

| | Case A (build set) | Case B (blind test) |
|---|---|---|
| When | Afternoon, 14:00 | Evening, 19:10 (busier) |
| Child | Boy, 6, **red t-shirt** | Girl, 7, **yellow hoodie, purple bunny** |
| Family | White thobe + **red** shemagh + green bag; abaya + **grey** hijab | **Grey** thobe + white ghutra + backpack; abaya + niqab + **stroller** |
| Enters by | Main entrance ENT-01 | Parking entrance ENT-02 |
| Why separated | Parents busy with phones in a shop | Mother busy with the baby, father queuing for food |
| Separation | STR-B (electronics), 14:19 | FC-01 (food court), 19:21 |
| Child walks | West | East |
| Child now | Alone at the food court counters FC-02 | Playing alone in the toy store STR-C |
| **Trick** | **A6**: a lookalike family (same thobe and shemagh, grey hijab, boy in red) eating together at FC-01, 14:24 | **B6**: a girl in a yellow hoodie alone in COR-E for a few seconds, then her mother catches up, 19:30 |
| Trick must give | "Not our boy": he's with his parents, wears shorts, and the real family is somewhere else at that time | No alarm: she's not alone and not our girl (our girl is in the toy store since 19:25 with no exit) |

The true timelines, including the tricks, are in `mall_topology.json` → `cases`.

## The blind-test rule

Case B only proves something if the system has never "seen" it while being built.

1. **Build on Case A only.** All code, question wording and thresholds are developed and adjusted with A1–A6.
2. **Case B stays sealed.** B clips go into `demo/raw/case-B/`, and nothing is uploaded to CreativAI or run on them before step 3.
3. **Freeze.** When Case A passes, the code is committed and tagged `freeze-v1`. From then on, no changes.
4. **One run.** Case B is uploaded and the frozen system runs once. The result is recorded in `demo/results/case-B.md` exactly as it comes out, pass or fail.
5. **After that**, fixes are allowed, but they become `v2` and need a **new** unseen case to prove themselves again.

This is the same rule scientists use (train on one set, test once on a set you never touched), and it's what makes "it works in general" a fair claim.

## The questions (same templates for both cases)
They're in `demo/prompts/06-creativai-questions.md`. Only the family and child descriptions change, and those come from the guard's report.

## The tests

A test **passes** when the expected clip is in CreativAI's **top 3** and the time is within **±3 s**.

| # | Test | Case A expects | Case B expects |
|---|---|---|---|
| 1 | Family on arrival (Q1) | A1 | B1 |
| 2 | Child with the family on each family clip (Q2) | A1, A2 yes; A3 yes until ~9 s | B1, B2 yes; B3 yes until ~9 s |
| 3 | **Separation moment** (Q3) | **A3, ~9–13 s** | **B3, ~9–13 s** |
| 4 | Child alone (Q4) | A4, A5 | B4, B5 |
| 5 | **Where now** (Q4 + Q5 on the latest clips) | **A5, FC-02** | **B5, STR-C** |
| 6 | **Trick rejected** (Q5 + Q6 + camera map) | A6 not reported as our boy | B6 no alarm, not our girl |
| 7 | Path walkable on the camera map | STR-B → ATR-01 → COR-W → FC-01 → FC-02 | FC-01 → COR-W → ATR-01 → COR-E → STR-C |

## What counts as success
- **Case A:** all 7 tests pass (we can adjust until they do, since it's the build set).
- **Case B, one blind run:** tests 3, 5 and 6 pass, and at least 6 of 7 overall.
- We report Case B honestly, whatever happens. A clean blind pass is the strongest thing to show the jury.

## Step 0: test early
Generate **A1 and A3 first**. We check tests 1–3 on them before spending more credits.
