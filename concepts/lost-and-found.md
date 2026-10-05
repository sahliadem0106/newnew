# Lost & Found: finding lost people at mass gatherings

> A guard radios in a description. Minutes later, the system has found the person on several cameras, mapped where they walked, told the nearest team where they are now, and recorded *why* they got lost so it happens less next time.

Target sites: Hajj and Umrah (Masjid al-Haram, Mina, Arafat), Riyadh Season, stadiums, airports, large festivals.

---

## 1. The flow

```
REPORT ──► UNDERSTAND ──► SEARCH CAMERAS ──► BUILD PATH ──► DISPATCH ──► REUNITE ──► LEARN
```

### ① Report: from many channels, in any language
- **Security radio / hotline:** the guard or operator speaks normally. Speech-to-text, then the agent turns it into a structured case:
  `{ who: child, age≈6, male, clothing: red shirt, white ihram-style cloth, carrying: blue balloon, last_seen: Gate 4, time: 14:10, language: Urdu }`
- **Kiosk / QR / WhatsApp** for families. A photo is helpful but not required.
- **Many languages:** pilgrims speak Arabic, Urdu, Indonesian, Turkish, Bengali, Hausa and more. The agent understands all of them and replies in the reporter's language.
- The agent **asks follow-up questions** if the description is weak ("Was he wearing shoes? Anything in his hands?").

### ② Search cameras: CreativAI does the core work
- The agent turns the case into several natural-language searches: the full description, then looser versions ("small boy in red shirt", "child holding blue balloon", "child alone crying"). *Crying* is something sound and context can catch.
- The search is limited to **cameras near the last-seen point** and the **time window since then**. The radius grows step by step.
- Each hit comes back as `camera_id + timestamp + score + clip`.

### ③ Build the path: where they went and where they are now
- The agent sorts the hits by time on a **venue map**: Gate 4 (14:10) → Corridor B (14:16) → Escalator 3 (14:21) → Courtyard East (14:29).
- It rejects impossible jumps (two cameras 1 km apart, 30 seconds apart) to drop false matches.
- From the walking direction and speed it **predicts the current zone** and the next likely cameras, then keeps checking those.

### ④ Dispatch: the right team, quickly
- The **nearest guard team** gets an alert by radio (text-to-speech) or the security app: last confirmed sighting, a short clip, the predicted zone and the walking direction.
- **A human always confirms** the match before acting. The AI ranks; people decide.
- Updates stream into the case as new sightings arrive.

### ⑤ Reunite: matching both sides
- Lost people are often **brought to a help center by someone else**. Center staff log "found" persons the same way (description or photo). The agent matches *found* cases against *lost* cases and calls the family.

### ⑥ Learn: find the cause and prevent it ⭐
Every closed case is saved with its path and the point of separation. Across hundreds of cases the agent produces:
- **Hotspot map:** where separations happen most (e.g. "Escalator 3 exit, after prayer").
- **Cause analysis:** CreativAI is asked about the moment of separation in each path: *Was the crowd dense? Did the flow change direction? Was there a sign the person looked at? Was the family split by a barrier or a guard line?*
- **Recommendations** for organisers: add signs in Urdu/Indonesian at Corridor B, open a second lane at Gate 4 after Maghrib, set up a meeting point near Escalator 3.
- **Before/after** measurements once changes are made.

This is the part that turns a search tool into a **safety-planning tool**.

### It also works for things
Lost wheelchairs, bags, strollers, a passport dropped on the floor: "black backpack with yellow tag, left near Zamzam station."

---

## 2. Why simple computer vision can't do this

| Need | Simple CV | CreativAI + agent |
|---|---|---|
| Search by a free spoken description ("red shirt + blue balloon") | ❌ needs a trained class for each attribute | ✅ open-language search |
| Use sound/context ("child alone, crying") | ❌ | ✅ vision + audio |
| Thousands of hours across hundreds of cameras | slow, custom pipeline | ✅ built for scale |
| Reason about the path, filter impossible matches, predict location | ❌ | ✅ agent |
| Find the *cause* of separations | ❌ | ✅ question columns + analysis |
| Multilingual reports | ❌ | ✅ agent |

No face-recognition database is needed: the search uses **descriptions**, which also limits the privacy risk.

---

## 3. Mapping to CreativAI

| Step | CreativAI API |
|---|---|
| Camera feeds in | `live_stream.stream_rtsp(cam_url, collection_id=...)` per camera, **or** short recorded chunks every few minutes via `media.upload_file` + `confirm_upload(tags={"*": ["cam-114", "zone-gate4"]})` |
| Searching | `search.query(cid, query, search_type="hybrid")`, filtered to camera/zone tags and time |
| Watching a predicted zone | `live_stream.add_questions(session, ["Is there a small child in a red shirt alone?"])` |
| Investigating the cause | `data_plates` + `knowledge_extraction.add_columns` on the separation clips ("crowd density?", "flow direction change?") |
| Operator Q&A | `agentic_chat`: "Show all sightings of case #231 after 14:20" |
| Agent | Claude with CreativAI's MCP server + its own tools (radio TTS, map, case database) |

---

## 4. Privacy & ethics (must be in the pitch)
- **Searches only when there is an active case**, never constant tracking of everyone.
- Every search is **logged and auditable** (who, why, which case).
- **A human confirms** each match before anyone is approached.
- Footage kept for a **short time**; case data deleted after it's closed, except anonymised path statistics for the "Learn" step.
- Run **only by the official authorities** of the site.

---

## 5. Demo plan (with no access to real Hajj cameras)
1. **Film a mini-venue:** 6–10 phones or cameras placed around a campus (e.g. KAUST plaza, library, corridors), each one a "security camera", with a simple map image.
2. Volunteers walk around in a crowd. One "lost child" (an adult in a distinctive outfit is fine) walks a route through 5 cameras.
3. **Live demo:** someone speaks the report into a "radio" mic, in Urdu or Arabic for impact. The case card builds itself, sightings pop up on the map, the path draws, and a "guard" phone gets the alert.
4. **Finish with the Learn screen:** a pre-computed hotspot map from 30 simulated cases, with recommendations.

## 6. Building it in stages
- **MVP (1–2 weeks):** upload recorded clips from 6 cameras with tags → text report → agent searches → hits on a map in time order → simple dashboard.
- **v2:** voice reports in several languages, impossible-jump filtering, location prediction, alerts to a guard's phone.
- **v3:** live RTSP feeds, found-vs-lost matching, the Learn analytics.

## 7. Questions to check with the CreativAI API
- Can live-stream footage be **searched afterwards** (rolling archive), or only questioned live? If only live, use rolling recorded chunks.
- Can search be **filtered by tags/time** directly, or must results be filtered after they come back?
- **Search speed** on a collection of several hundred cameras.
- How fresh results can be: delay from recording → indexed → searchable.
