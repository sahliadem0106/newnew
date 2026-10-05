# Showcase ideas that prove CreativAI's value

## What CreativAI is

[CreativAI](https://creativ-ai.com) is a video intelligence platform led by Prof. Mohamed Elhoseiny (KAUST, Vision-CAIR group). It indexes video once, up to tens of thousands of hours. After that, everything in it can be **found, questioned and turned into data** using plain language.

## The rule for a good showcase

Each idea should make the visitor think: **"this would be impossible without CreativAI."**

So every idea is built around one of the product's five value points, and it shows the payoff on screen: how many hours were searched, how long it took, and how long a human would need.

| # | Value point | API surface |
|---|---|---|
| V1 | **Find any moment** in a huge library by describing it | `search.query(cid, "...")` |
| V2 | **Sees and hears**: matches on visuals, speech and sounds | `search_type="vision" \| "audio" \| "hybrid"` |
| V3 | **Video becomes data**: ask a question, get a column for every moment | `data_plates` + `knowledge_extraction.add_columns` → CSV, charts, Q&A |
| V4 | **Live understanding** of a feed as it happens | `live_stream.stream_webrtc/rtmp/rtsp` + `add_questions` |
| V5 | **Agent-ready**: an AI assistant can reason over the whole library | `agentic_chat` (SSE), 62-tool MCP server |

Its own demos are industrial (dashcams, safety gear). The ideas below show the same five strengths in a form anyone can enjoy.

---

## ⭐ 1. "The Haystack": human vs. CreativAI (flagship)

**Value shown: V1 + V2, plus scale.**

The landing page loads a huge archive, for example **2,000 hours** of public-domain films, newsreels and travel videos. A big counter shows it: *"2,000 hours, 83 days of nonstop video."*

The visitor types anything, e.g. *"a cat jumps onto a piano"*, *"someone whistling on a train"* or *"fireworks reflected in water"*. In about a second the page shows the exact moments, with a scoreboard:

> **Searched: 2,000 h · Time: 0.9 s · A human watching would need: 250 workdays**

Then comes the creative payoff: one click turns the results into a **montage**. A whole sentence can become a short film, with each part of the sentence becoming a shot ("A lonely man walks in the rain → finds a dog → laughs").

- **Why it proves value:** speed, scale and understanding are shown, not claimed. Sound-only queries ("whistling") show that it hears as well as sees.
- **How:** `search.query` for each part of the sentence → `start_time` of each hit → a chain of players in the browser. The "human time" comes from total archive hours ÷ 8 h per workday.

## 2. "Ask the Archive": a heritage film library you can talk to

**Value shown: V5 + V1, applied to a real culture problem.**

Index a cultural archive, such as decades of public broadcasts, film-festival collections or Saudi/Arab heritage footage. Visitors chat with it: *"How did weddings in Jeddah look in the 1970s?"* or *"Show me old souq scenes with traditional crafts."* The agent answers in text and backs every claim with **clickable moments**.

- **Why it proves value:** archives hold millions of hours that nobody can watch, and this makes them usable. It's a compelling story for museums, broadcasters and universities, which makes it a real customer pitch as well as a demo.
- **How:** `agentic_chat.create_session` → stream `thinking/search/answer` events. Showing the agent's search steps live is impressive in itself.

## 3. "Atlas of Everyday Life": 1,000 videos in a spreadsheet

**Value shown: V3, the feature competitors don't have.**

Import about 1,000 city walking tours from around the world with the built-in YouTube search. Add AI question columns such as *dominant color?*, *is it raining?*, *what are people wearing?*, *mood of the street?* and *loudest sound?*. A few minutes later every moment of every video is a data row. The site renders it as an interactive world map and timeline where each dot plays its clip, and visitors can ask questions like *"Which city has the most umbrellas?"*

- **Why it proves value:** it shows unstructured video becoming structured data that you can chart, query and export. That's the step from "search engine" to "research tool".
- **How:** `start_youtube_search` → `confirm_youtube_search` → `data_plates.create_from_collection` → `knowledge_extraction.add_columns` → `export_csv` / `chat_query` → D3 front end.

## 4. "The Mirror": a live installation for events

**Value shown: V4 + V1 together.**

A webcam watches the visitor (in the browser over WebRTC). CreativAI answers live questions: *"What is the person holding?"* and *"What gesture are they making?"*. Each answer instantly becomes a search over the film archive: raise a cup and a wall of movie characters raising cups appears, wave and you get 50 waves from 100 years of cinema.

- **Why it proves value:** in one loop, it shows live understanding feeding instant search over a big library. It draws a crowd at a booth.
- **How:** `live_stream.stream_webrtc` + `add_questions` → poll the answers → `search.query(archive_cid, answer)` → clip grid.

## 5. "Memory Lane": a family's home videos, searchable

**Value shown: V1 + V5 on content everyone has.**

A family connects Google Drive or Dropbox (the import is built in) and asks *"Every birthday where grandpa sang"* or *"Sara's first steps"*. The agent finds the moments and assembles a memory reel.

- **Why it proves value:** "20 years of home video that nobody can find anything in" is a problem everyone has, so the value is clear in a single sentence.
- **How:** `upload_integrations.google_drive_transfer` → index → `agentic_chat` → stitch the cited moments.

## 6. "Claude, the editor": an agent cuts a trailer

**Value shown: V5, CreativAI as infrastructure for AI agents.**

Claude is connected to CreativAI's hosted MCP server. You say *"Make a 30-second trailer about courage from this archive"*, and Claude searches, picks, orders and outputs an edit list that the site plays.

- **Why it proves value:** it positions CreativAI as the "eyes and ears" for any AI agent working with video, which appeals to a developer audience.

---

## Recommendation

Build **#1 "The Haystack"** first. It proves the core value (huge scale, instant results, sees and hears) in the first 10 seconds, the montage makes it fun and shareable, and it only needs search plus a video player.

Then add one of these, depending on the audience:
- **#3 Atlas**, for investors or technical judges: it shows the data-extraction moat.
- **#4 Mirror**, for a live event or booth.
- **#2 Ask the Archive**, for a KAUST or cultural audience: it shows real-world impact.

All of them can share **the same indexed archive**, so you only pay for indexing once.

### Things to verify with a free API key before building

- Whether search hits include an `end_time` and a playable URL. The README shows `video_name`, `start_time` and `score`. If there's no URL, host the files yourself and seek by `start_time`.
- The real search time on a large collection, which is the headline number in #1. Measure it; don't assume it.
- How long live answers take to arrive, which matters for #4.
- Indexing cost for the archive (`indexing.estimate_cost`) against your credits.
- Licensing: use public-domain or Creative Commons footage for anything public.

Sources: [CreativAI Python SDK (PyPI)](https://pypi.org/project/creativai/), [creativai-mcp (PyPI)](https://pypi.org/project/creativai-mcp/), [KAUST profile](https://cemse.kaust.edu.sa/profiles/mohamed-elhoseiny), [GiantLeap session "CreativAI: LLM-powered Video Query Engine at Scale"](https://onegiantleap.com/session/creativai-llm-powered-video-query-engine-scale).
