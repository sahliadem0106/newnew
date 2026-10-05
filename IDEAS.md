# CreativAI + AI agents: footage that triggers action

## The concept

> **CreativAI is the eyes, ears and memory. An AI agent is the brain and hands.**
> Feed it any footage, recorded or live. CreativAI understands what is happening, and an agent decides what to do and does it: alerting, dispatching, filing, mapping, reporting.

```
footage (live cams, uploads, phones, YouTube/web)
        │
        ▼
CreativAI ── live questions / search / extraction ──►  "what is happening?"
        │                                              (vision + audio + time)
        ▼
AI agent (e.g. Claude + CreativAI MCP)  ── reasons, checks evidence ──►  ACTION
                                                                    (alert, ticket, map, SMS, report)
```

## The filter: what simple computer vision can't do

A fire, a car or a person can be detected by a cheap trained model. Every idea below needs at least one thing simple CV doesn't have:

1. **Open questions with no training.** You write a new question in plain English today and it works today. CV needs a dataset and a model for each new object.
2. **Understanding over time.** "She has been standing still at the stove for 10 minutes" or "this car has circled 3 times" is a story, not a single-frame label.
3. **Sound plus picture.** Someone shouting "help", a child crying, a smoke alarm, people describing what they see.
4. **Context and intent.** The same scene means different things depending on the situation: a man lying down in a park, or a man lying down in a road at night.
5. **Searching memory.** "Where else have we seen this?" across thousands of hours.

---

## ⭐ 1. Rescue Radar: disaster response from citizens' videos (flagship)

**Problem.** In a flood, earthquake or fire, the first footage doesn't come from official cameras. It comes from **thousands of people filming on their phones** and posting it. Nobody can watch it all, and the critical clip ("family on a roof, Street 12") gets buried.

**How it works**
1. **Collect.** Videos come in from an upload link for citizens and responders, plus CreativAI's built-in **web/YouTube search import** (`start_online_search`, `start_youtube_search`), plus any live drone feed (`stream_rtmp`).
2. **Understand.** A data plate with AI question columns runs on every clip:
   - *Are people trapped or stranded? How many?*
   - *Is anyone injured or calling for help?* (audio + vision)
   - *Is the road passable for vehicles?*
   - *Which street signs, shop names or landmarks are visible or mentioned?* (for finding the location)
   - *Water level relative to cars or doors?*
3. **Act.** A Claude agent reads the new rows and:
   - geolocates each clip from landmarks, spoken place names and metadata, and pins it on a live map
   - ranks the cases by urgency (trapped + injured + rising water = top)
   - writes a dispatch card for each case: location, number of people, hazards, a 10-second evidence clip
   - spots **duplicates** (the same roof filmed by 5 people) so rescuers don't go twice
   - answers commanders in chat: *"Which bridges are still usable in the north district?"*

**Why simple CV can't do this:** "People trapped", "calling for help" and "road passable" depend on context, sound and reasoning, not object labels. And you can add a new question mid-crisis ("is anyone holding a white flag?") with no retraining.

**API path:** `online search/YouTube import` → `indexing.start` → `data_plates.create_from_collection` → `knowledge_extraction.add_columns` → poll `get_data_plate` → agent → `agentic_chat` for commander Q&A.

**Demo for the site:** use real public footage from a past flood (for example Jeddah 2009/2022, or Derna 2023). Visitors watch the map fill up and the dispatch queue sort itself as the clips are processed.

---

## 2. Truth Trace: stop fake viral videos

**Problem.** During crises, old or unrelated videos go viral with false captions ("this is happening in X right now"). Fact-checkers take hours.

**How it works.** Paste a viral video. The agent:
1. asks CreativAI to describe it (scene, language spoken, signs, weather, landmarks)
2. runs **web/YouTube searches** for similar footage, imports the candidates and searches them for the same moments
3. compares: *"This footage first appeared in 2019 in another country. The shop signs are in Turkish, but the caption says Cairo. The speaker's dialect doesn't match."*
4. publishes a verdict card with side-by-side evidence clips.

**Why simple CV can't do this:** it needs language, dialect, signs and reasoning across many videos, plus a memory of the web.

---

## 3. Lost & Found: finding lost people at mass gatherings

**Problem.** At Hajj, Riyadh Season, stadiums and festivals, children and elderly people get separated from their families. The parent's description is in words: *"6-year-old boy, red shirt, holding a blue balloon, last seen near Gate 4."*

**How it works.** Staff type or say the description. CreativAI searches the last 30 minutes of the venue's live cameras in natural language. The agent ranks the matches by time and place, works out the likely direction of movement, and sends the nearest staff a photo and location.

**Why simple CV can't do this:** you can't train a model for "red shirt + blue balloon + small boy". Free-text descriptions need open-vocabulary search over recent footage.
*(Needs a clear privacy policy: search only on request, footage kept for a short time only.)*

---

## 4. Guardian at Home: support for older people living alone

**Problem.** Fall detectors only catch falls. Many dangers in daily life are slow and depend on context.

**Live questions** (consented, in-home camera): *Was the medication taken this morning? Has the stove been on with nobody in the kitchen? Is the person repeating the same action in a confused way? Have they eaten today? Did they say they feel unwell?*
**The agent:** sends a gentle reminder through a speaker, messages family if something persists, and writes a calm daily summary for the doctor showing trends over weeks.

**Why simple CV can't do this:** "took medication", "confused" and "didn't eat" are activities that unfold over time and with sound, not objects.

---

## 5. City Fix: buses as city inspectors

**Problem.** Cities find broken infrastructure late, through complaints.

Footage from bus and garbage-truck cameras is indexed every day. The city's questions, which can be changed any time in plain English: *blocked wheelchair ramps, broken streetlights at night, flooded underpasses, illegal dumping, missing manhole covers, kids crossing at a dangerous spot with no crosswalk.*
**The agent:** removes duplicates across days, opens a maintenance ticket with GPS and a clip, tracks repairs, and shows a public "fixed in X days" dashboard.

**Why it beats simple CV:** you write a new check in plain English instead of training a model, and it understands context ("dangerous crossing" isn't an object).

---

## Recommendation

**Build Rescue Radar.** It's the most useful idea and the strongest demo, because it uses almost everything CreativAI has:
- web/YouTube import
- vision + audio understanding
- data plates (one AI question per column)
- live drone streams
- agentic chat

The agent layer (Claude through CreativAI's MCP server) is what turns understanding into action. A demo on real past disaster footage, with a map filling up and a dispatch queue ranking itself, is something people remember.

**Truth Trace** is a good second project: smaller, quick to build, and it gets a lot of public attention.

### Check with a free API key first
- How fast the knowledge-extraction columns run on new clips. This decides whether Rescue Radar is "near real time" or "batch every few minutes".
- Live-stream answers are polled (no webhook is documented), so the agent needs a polling loop.
- What is returned per hit (playable URL? `end_time`?) for the evidence clips.
- Credits and indexing cost for the footage you plan to use.

Sources: [CreativAI Python SDK](https://pypi.org/project/creativai/), [creativai-mcp](https://pypi.org/project/creativai-mcp/), [KAUST profile](https://cemse.kaust.edu.sa/profiles/mohamed-elhoseiny).
