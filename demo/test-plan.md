# Test plan: does the system really work?

Two cases with **different families, colours, times, separation causes, directions and end places**, in the **same mall and cameras**. If the same code solves both without changes, it's not tuned to one story.

| | Case A | Case B |
|---|---|---|
| When | Afternoon, 14:00 | Evening, 19:10 (busier) |
| Child | Boy, 6, **red t-shirt** | Girl, 7, **yellow hoodie, purple bunny** |
| Family signature | White thobe + **red** shemagh + green bag; abaya + **grey** hijab | **Grey** thobe + white ghutra + backpack; abaya + niqab + **stroller** |
| Enters by | Main entrance (ENT-01) | Parking entrance (ENT-02) |
| Why separated | Parents busy with phones in a shop | Mother tending the baby, father queuing for food |
| Separation at | Electronics store STR-B, 14:19 | Food court FC-01, 19:21 |
| Child walks | **West**, toward the food court | **East**, toward the toy store |
| Child now | Alone at the food court counters (FC-02), upset | Playing alone in the toy store (STR-C), calm |
| Lookalikes in the crowd | Other white thobes and black abayas | Many thobes, abayas and other strollers |

Both are common real situations: a child drifts away while the parents are distracted, either shopping or at the food court.

## Step 0: test early, before spending the whole budget
Generate **A1 and A3 first** (~$1.90). Upload both to CreativAI and run tests 1 and 2 below.
- ✅ If CreativAI finds the family in A1 and the boy leaving in A3, generate the rest.
- ❌ If not, we change the prompts or the questions before buying more clips.

## The tests (same for both cases)

Each test is a plain-language search in CreativAI. A test **passes** when the expected clip is among the **top 3 results** and the time inside the clip is within **±3 seconds** of the moment described.

| # | Question the system asks | Case A expects | Case B expects |
|---|---|---|---|
| 1 | Find the family on arrival: *"man in [thobe colour] thobe and [shemagh] with a woman in a black abaya and a small [boy/girl] in [colour]"* | A1 (ENT-01) | B1 (ENT-02) |
| 2 | Is the child still with them? *"family with a small child walking together"* on each family clip | A1 ✓, A2 ✓, A3 ✓ until ~9 s | B1 ✓, B2 ✓, B3 ✓ until ~9 s |
| 3 | The separation: *"child walking away alone while the parents are busy"* | **A3 at ~9–13 s** | **B3 at ~9–13 s** |
| 4 | The child alone: *"small [boy in red t-shirt / girl in yellow hoodie] walking alone"* | A4 then A5 | B4 then B5 |
| 5 | Where now: *"[boy/girl] alone, no adult with them"* in the latest clips | **A5 (FC-02)** | **B5 (STR-C)** |
| 6 | Lookalikes: test 1's search must **not** rank strangers in thobes/abayas above the family | family clip first | family clip first |
| 7 | The graph check: the path from separation to "now" must be walkable on the camera map in the time available | STR-B → ATR-01 → COR-W → FC-01 → FC-02 ✔ | FC-01 → COR-W → ATR-01 → COR-E → STR-C ✔ |

The true timelines for both cases are in `mall_topology.json` → `cases`. The code compares its answers against them automatically.

## What "it works" means for the demo
- Both cases: tests 3 and 5 pass (separation and current location found).
- At least 5 of the 7 tests pass in each case.
- Same code, no per-case tweaks.

If a test fails, we fix it in this order: the **question wording** first, then the **prompt** (regenerate the clip), and only then the code.
