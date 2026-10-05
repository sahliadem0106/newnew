# Guardian at Home: peace of mind for families far away

> *"How was Dad today?"* A son working abroad asks, and gets a real answer: he woke at 7, took his morning pills, had a visitor at 11, ate lunch late, napped, and seemed tired in the evening. One thing: he skipped the evening pill, so we reminded him and he took it at 9:20.

For older parents living alone while their children live in another city or country, people recovering after hospital, or early-stage dementia.

---

## 1. What it does

### ① "What happened today?": a chat with the day
The family chats with the agent in Arabic, English or anything else:
- "Did Mom eat today?" → *"Yes, breakfast at 8:10 and lunch around 14:00. No dinner yet."* + clip
- "Did anyone visit?" → *"Your aunt visited 16:00–17:30."*
- "Was he OK this week compared to last week?" → trend summary

Every answer can come with a **short clip as evidence**, but only if the parent has allowed clips to be shared. Otherwise it gives text only.

### ② Medication tracking & reminders ⭐
- The family enters the schedule: *blood-pressure pill 8:00, diabetes pill with lunch, 21:00 pill.*
- Live questions on the kitchen or pill-area camera: *"Did the person take a pill from the pill box? Did they drink water after?"*
- **Escalation ladder** if a dose is missed:
  1. +15 min → a gentle **voice reminder** on a home speaker, in their dialect ("Baba, time for the white pill")
  2. +30 min → a **phone call** from the agent to the parent
  3. +60 min → **message to the family** abroad
  4. Something serious (no movement for hours, a fall, a call for help) → **local contact / neighbour / emergency services**
- Catches **double dosing** too: "He took the 8:00 pill twice."

### ③ Daily & weekly health report
Every day is turned into data, one row per day:

| Date | Woke | Meals | Pills on time | Time active | Went outside | Visitors | Mood/energy note |
|---|---|---|---|---|---|---|---|

Trends over weeks are what doctors care about: *eating less, sleeping more, moving more slowly, fewer visitors, more confused moments.* The report can be shared with the doctor before a check-up.

### ④ Spotting the slow, quiet risks (beyond fall detection)
- Stove or kettle on with **no one in the kitchen** for 10+ minutes
- Front door **left open** at night
- **Confusion signs:** repeating the same action, wandering at 3 a.m., looking for something for a long time
- **Not drinking enough** on a hot day
- Speech: *"I feel dizzy"*, *"my chest hurts"* → immediate escalation

---

## 2. Why simple computer vision isn't enough
- "Took the medicine", "ate lunch", "seems confused" are **activities over time**, not objects in one frame.
- **Sound matters:** a call for help, a smoke alarm, the parent saying they feel unwell.
- **Open questions:** the family can add *"Did he do his physio exercises?"* in plain English, with no new model.
- **Memory:** "compare this week to last month" needs a searchable history, not a single alarm.

---

## 3. Mapping to CreativAI

| Feature | CreativAI API |
|---|---|
| Home camera | `live_stream.stream_webrtc` (an old phone or tablet as the camera) or `stream_rtsp` (an IP camera), into a collection per home |
| Pill / stove / door checks | `live_stream.add_questions(session, [...])`, with answers polled by the agent |
| "What happened today?" | `agentic_chat` over the day's footage |
| Daily table & trends | `data_plates` + `knowledge_extraction.add_columns` ("meals?", "pills taken?", "went outside?") → `get_plate_charts`, `export_csv` |
| Agent | Claude + CreativAI MCP + tools: WhatsApp/SMS, phone call, smart speaker TTS, schedule |

---

## 4. Privacy & dignity (central to the product)
- The **parent agrees** and controls it. A physical **privacy button / voice command** ("Guardian, pause") turns it off.
- Cameras only in **common areas** (kitchen, living room, entrance). **Never bedroom or bathroom.**
- **Text summaries by default**; clips shared only if the parent has agreed.
- Short retention for video; only the daily data rows are kept long-term.
- Tone: a **helper for the parent**, not a spy for the children. Reminders are kind and in their own dialect.

---

## 5. Demo plan
1. Film a **staged day** in an apartment: an actor plays "Grandpa". He wakes, has breakfast, takes his pills, *forgets* the evening pill, leaves the stove on once, gets a visitor and takes a nap.
2. **Live demo:** the audience plays the son abroad and asks in Arabic, "How was Dad today?" The agent answers with clips.
3. Show the **missed-pill moment:** a reminder plays from a speaker, then a WhatsApp message arrives on a phone on stage.
4. Show the **weekly report** with trend charts.

## 6. Building it in stages
- **MVP (1–2 weeks):** upload recorded day clips → data plate with 6 questions → daily report + chat for the family.
- **v2:** live webcam from a phone, pill schedule + voice/WhatsApp reminders + escalation ladder.
- **v3:** weekly trends, a report for the doctor, risk alerts (stove, door, "I feel dizzy").

## 7. Questions to check with the CreativAI API
- Delay of live-question answers: is a pill check seconds or minutes?
- Running cost for a 24/7 home stream versus uploading only motion-triggered chunks (probably much cheaper).
- Arabic (and dialect) support in audio search.
