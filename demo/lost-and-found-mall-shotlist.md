# Lost & Found demo: mall shot list (Kling 3.0 via Higgsfield)

Budget: **~$15 → ~15 clips of 15 s** ($0.945 each).
Plan: **11 story clips (~$10.40) + 4 spares for failed generations (~$3.80).**

> 💡 **Check the price per second first.** If Higgsfield charges by duration, generate **8–10 s clips** instead of 15 s. Security footage doesn't need more, and you get almost twice as many clips (more decoys, more spares).

## Why a mall and not the Haram
- You can design a mall layout yourself. You can't reproduce the Haram's real layout believably.
- Making fake security footage of a holy site is sensitive, and AI models get its architecture wrong.
- **Pitch line:** *"We demo in a mall. The same system scales to Hajj, stadiums and airports."* Keep the Hajj use case for the final slide.

## Why this works with AI-generated video
The system searches by **description** (red shirt + blue balloon), not by face. So the boy's face doesn't need to be identical in every clip, only his **outfit**. That's exactly where AI video struggles least. Each camera shows a **different place**, so you never need the impossible "same moment from two angles" shot.

---

## 1. The mall: "Al-Noor Mall", 2 floors, 8 cameras

```
                         UPPER FLOOR
   ┌───────────────────────────────────────────────────────────┐
   │  [CAM-05] Toy store        [CAM-06] Atrium balcony        │
   │   front ◄──── corridor ────►  benches + fountain view      │
   │        ▲ [CAM-04] Upper corridor                           │
   │        │                                                   │
   │   [CAM-03] Escalator top                                   │
   └────────┼──────────────────────────────────────────────────┘
            │ escalator
   ┌────────┼──────────────────────────────────────────────────┐
   │   [CAM-02] Escalator base         [CAM-08] Info / Security │
   │        ▲                                desk               │
   │        │                                                   │
   │   [CAM-01] Food court ───────────── [CAM-07] Main entrance │
   └───────────────────────────────────────────────────────────┘
                         GROUND FLOOR
```

**Realistic camera placement:** every camera is **ceiling-mounted or high on a wall/pillar, 3–4 m up, angled 30–45° downward, wide lens**. Never at eye level, never moving. Every prompt includes this.

## 2. The story (timeline on the burned-in clocks)

| Time | What happens |
|---|---|
| 14:00 | Family eats at the food court. Boy (6) in a **red t-shirt** with a **blue balloon**. |
| 14:05 | Prayer time ends and the crowd surges at the escalator base. **The boy's hand slips from his mother's; the flow separates them** (← *the cause*). |
| 14:06 | Boy rides the escalator up alone. |
| 14:08 | Walks along the upper corridor, looking around. |
| 14:10 | Stops at the toy store window. |
| 14:13 | Sits on a bench at the atrium balcony, crying. |
| 14:12 | Mother reports to security at the info desk (the radio report). |
| 14:19 | Guard finds the boy on the bench. |
| 14:23 | Reunion at the info desk. |
| decoys | A **different** boy in red without a balloon at the entrance; an **adult** with a blue balloon in the corridor. The agent has to reject both. |

## 3. Shot list & prompts

**Put this style block at the start of every prompt:**
> *Security camera footage. Fixed ceiling-mounted CCTV camera, high angle looking down at about 40 degrees, wide-angle lens with slight fisheye distortion, completely static camera, no camera movement, no zoom. Modern Middle-Eastern shopping mall, bright fluorescent and LED lighting, polished marble floor. Realistic, slightly soft surveillance video quality. No on-screen text.*

**Character block (copy it exactly every time):**
> *a 6-year-old boy with short black hair wearing a bright red t-shirt, blue jeans and white sneakers, holding the string of a blue helium balloon*

**Mother block:**
> *a mother in a black abaya and a light grey headscarf carrying a beige handbag*

| # | Camera | Overlay start | Prompt (after the style block) | Purpose |
|---|---|---|---|---|
| 1 | CAM-01 Food court | 14:00:10 | Busy food court with families at tables. At a table in the middle-left, [MOTHER] and a father in a white thobe eat with [BOY]. The boy swings his legs and plays with the balloon. Other families walk past. | "Last seen" + baseline |
| 2 | CAM-02 Escalator base | 14:05:20 | Very crowded area at the base of an escalator; a large crowd moves toward it at once. [MOTHER] walks holding the hand of [BOY]. The crowd pushes between them, his hand slips out of hers, and she is carried forward onto the escalator while he stays behind, looking around confused, balloon above the crowd. | ⭐ **The cause.** Used by the "Learn" step |
| 3 | CAM-03 Escalator top | 14:06:40 | Top of an escalator, upper floor. People step off. [BOY] steps off alone, stops and turns around looking for someone, then walks off to the right. | Path point 2 |
| 4 | CAM-04 Upper corridor | 14:08:05 | Long upper-floor corridor with shopfronts on both sides, moderate crowd. [BOY] walks alone slowly through the middle, looking left and right, balloon bobbing above him. | Path point 3 |
| 5 | CAM-05 Toy store front | 14:10:30 | Front of a colorful toy store with a large glass window. [BOY] stands alone pressing his hands on the window, looking at the toys, then walks away toward the atrium. | Path point 4 |
| 6 | CAM-06 Atrium balcony | 14:13:00 | Upper balcony overlooking a mall atrium with a fountain below. Benches along the glass railing. [BOY] sits alone on a bench, rubbing his eyes and crying, balloon tied to his wrist. People pass by without stopping. *(Turn audio on if available: a child crying, mall ambience.)* | Final location. Audio "crying" query |
| 7 | CAM-08 Info desk | 14:12:10 | Mall information and security desk with a uniformed security guard holding a radio. [MOTHER] arrives in a panic and talks quickly, gesturing to show the height of a child. The guard speaks into his radio. | The **report** moment |
| 8 | CAM-06 Atrium balcony | 14:19:30 | Same balcony and benches as before. A uniformed security guard walks up to [BOY] sitting on a bench, kneels down to his level, talks to him gently, then takes his hand and walks with him toward the escalator. | Found |
| 9 | CAM-08 Info desk | 14:23:00 | Mall information desk. The security guard arrives holding the hand of [BOY]. [MOTHER] runs to him and hugs him tightly; the guard smiles. | Reunion, the emotional ending |
| 10 | CAM-07 Main entrance | 14:09:00 | Main mall entrance with glass sliding doors, people entering. A **different** boy, about 8, in a red t-shirt and **black** shorts, **no balloon**, walks in holding his father's hand. | **Decoy 1:** reject (has a parent, no balloon, wrong place) |
| 11 | CAM-04 Upper corridor | 14:15:00 | Same upper corridor. A teenage girl carries a bunch of blue balloons, walking with friends. No children alone. | **Decoy 2:** reject (balloon matches, person doesn't) |
| 12–15 | spares | | Regenerate whichever clip failed (wrong outfit, moving camera, garbled faces). | |

### Generation tips
- **Lock the boy's look first:** generate one still image of [BOY] (cheap on Higgsfield's image models) and use it as the **start frame / reference image** for clips 1–6, 8 and 9 if the image-to-video mode allows it. This is the best way to keep the outfit consistent.
- Keep the **same wording** for the boy every time. Changing "bright red" to "red" changes the result.
- Ask for **"static camera"** twice if the first try pans.
- Put nothing in the prompt about text, because models write gibberish. Our script adds the labels.

## 4. After generating: add the security-camera look and the labels

```bash
./demo/cctv_overlay.sh raw/01.mp4 final/CAM-01_foodcourt.mp4 "CAM-01 FOOD COURT GF" "2026-10-12 14:00:10"
./demo/cctv_overlay.sh raw/02.mp4 final/CAM-02_escalator_base.mp4 "CAM-02 ESCALATOR BASE GF" "2026-10-12 14:05:20"
# ... one line per clip, using the start times from the table
```

This adds the camera name, a running clock, slight grain and lower saturation, so AI clips look like real security footage.

## 5. In CreativAI
- One collection: `al-noor-mall-cctv`. Upload each clip with tags `{camera, zone, floor}` in `confirm_upload(tags=...)`, then index it.
- **Queries for the demo:**
  - `"small boy in red t-shirt holding a blue balloon"` → should find clips 1–6, 8 and 9, plus decoys 10/11 ranked lower
  - `"child alone crying"` (audio + vision) → clip 6
  - `"child separated from his mother in a crowd"` → clip 2 (the cause)
  - `"security guard comforting a child"` → clip 8
- **The agent** (Claude + CreativAI MCP) receives the report: *"Lost boy, 6, red shirt, blue balloon, last seen food court 14:00"*. It searches, rejects the decoys with a reason, orders the sightings by camera clock onto the map (01 → 02 → 03 → 04 → 05 → 06), predicts *"likely still at the atrium balcony"* and writes the guard dispatch. Then it explains the cause: *"separated at the escalator base during the crowd surge after prayer. Suggest a family meeting point and crowd marshal at CAM-02."*

---

## Guardian at Home (later, or with the next $15)

Realistic home setup: **3 cameras**, all high in a room corner, wide angle:

| Camera | Where | Sees |
|---|---|---|
| HOME-01 Kitchen | Upper corner above the fridge, facing the counter | Stove, counter, **pill organizer on the counter**, small dining table |
| HOME-02 Living room | Upper corner opposite the sofa | Sofa, TV, armchair, window |
| HOME-03 Entrance | Above the inside of the front door, facing the hallway | Front door, visitors arriving, leaving the house |

**Real-product detail:** during setup, the app asks the family to **keep the pill organizer on the kitchen counter in view of HOME-01**. That's how real products handle it, so the camera stays in a normal place and the pill box comes to it. Bedroom and bathroom: never.

**8-clip day for Grandpa** (one actor; same outfit block every time: *"an elderly Arab man around 75, white beard, beige thobe, white kufi cap, reading glasses"*):
1. HOME-01 07:40: makes tea, opens the pill organizer, takes the morning pill with water ✅
2. HOME-02 09:30: reads a newspaper on the sofa
3. HOME-03 11:00: a visitor (his sister) arrives, they greet
4. HOME-01 13:30: eats lunch at the small table
5. HOME-02 15:00: naps on the sofa
6. HOME-01 18:10: **puts a pot on the stove, then leaves the kitchen**; the stove is left on ⚠️
7. HOME-01 21:00: walks past the pill organizer **without** opening it ❌ (missed dose → reminder)
8. HOME-01 21:20: comes back, opens the organizer, takes the pill ✅ (after the voice reminder)
