# Showcase ideas built on CreativAI

## What CreativAI is

[CreativAI](https://creativ-ai.com) is a video intelligence platform led by Prof. Mohamed Elhoseiny (KAUST, Vision-CAIR group). It makes video **searchable and queryable**: you upload or import footage, index it once, and then:

| Capability | API surface | What it gives you creatively |
|---|---|---|
| Natural-language moment search | `search.query(cid, "...", search_type="hybrid" \| "vision" \| "audio")` | Exact moments (video + `start_time`) matching any sentence, by what is seen **or heard** |
| Agentic chat | `agentic_chat.chat(session, "...")` (SSE: thinking → search → answer) | An assistant that reasons over a whole library and cites moments |
| Data plates + knowledge extraction | `data_plates.*`, `knowledge_extraction.add_columns(...)` | Turns every segment into a spreadsheet row; you add AI "question columns" (text/boolean) → CSV, charts, Q&A |
| Live streams | `live_stream.stream_webrtc / rtmp / rtsp` + `add_questions([...])` | Real-time answers about a live feed, including a **browser webcam** over WebRTC |
| Web / YouTube import | `start_youtube_search`, `start_online_search`, `transfers.start(url)` | Builds a corpus from public video in minutes |
| MCP server (62 tools) | hosted at `ws.creativai-apis.com/api/v2/mcp` | Claude or any agent can drive the whole platform |

The default demos are industrial (dashcams, PPE checks, forklift incidents). The ideas below use the same API for art, play and storytelling instead.

---

## 1. "Say It in Cinema": sentence-to-montage machine ⭐ top pick

A visitor types a sentence: *"A lonely man walks in the rain, then finds a dog and laughs."* The site splits it into beats, runs a search for each beat across a large indexed archive (public-domain films, Prelinger archives, YouTube travel vlogs), and plays the clips back to back as a montage. It ends with a shareable link.

- **Why it impresses:** it feels like video generation, but every frame is real footage. Hybrid search lets a beat match on sound ("someone laughing", "thunder").
- **How:** Claude splits the sentence into beats → `search.query` per beat → take the top hit's `start_time` → play a fixed-length window in a browser player chain. Add a "reroll" button per beat that takes hit #2, #3 and so on.
- **Twist:** a "Poetry mode", where each line of a poem becomes a shot.

## 2. "The Mirror": your webcam, answered by film history

The visitor stands in front of a webcam (WebRTC live session). Live questions run continuously: *"What is the person holding?"*, *"What gesture are they making?"*, *"What emotion do they show?"*. Each answer becomes a search query on a film archive, so raising a cup brings up a wall of famous movie characters raising cups. Waving brings up 50 waves from 100 years of cinema.

- **Why it impresses:** it's a strong live installation for an expo or booth, and every visitor gets their own version.
- **How:** `live_stream.stream_webrtc` + `add_questions` → poll the answers → `search.query(archive_cid, answer)` → render a grid of clips.

## 3. "Atlas of Everyday Life": data art from 1,000 videos

Import hundreds of city walking tours (Tokyo, Cairo, Lagos, Riyadh, Paris, from the 1900s to today) through YouTube search. Build a data plate and add extraction columns such as *dominant color*, *is it raining?*, *what are people wearing?*, *mood of the street*, *loudest sound*. Then render the CSV as an interactive map or timeline where every dot is a clickable moment.

- **Why it impresses:** it reads as a research project and as an artwork at once ("how humanity walks"), and it uses the platform's most distinctive feature, structured extraction.
- **How:** `start_youtube_search` → `confirm_youtube_search` → `data_plates.create_from_collection` → `knowledge_extraction.add_columns` → `export_csv` → a D3 or Observable front end.

## 4. "Moment Hunt": a multiplayer search game

The site shows a 3-second clip from the archive. Players race to type a description that makes the search engine find that exact clip, and the closer the rank, the more points. Another mode, "Describe it in 5 words", rewards precise language.

- **Why it impresses:** it's addictive, it shows off search quality, and it teaches people how semantic search works.
- **How:** sample a segment from a data plate → players submit queries → score by the target's rank in `search.query` results.

## 5. "Memory Lane": talk to a family's home videos

A family uploads decades of home videos (Google Drive/Dropbox import is built in) and asks *"Show me every birthday where grandpa sang"* or *"When did Sara take her first steps?"*. Agentic chat answers with clips, and the site assembles a short "memory reel" automatically.

- **Why it impresses:** it's emotional, and anyone who has a phone full of video wants it.
- **How:** `upload_integrations.google_drive_transfer` → index → `agentic_chat` → stitch the cited moments.

## 6. "Claude, the editor": an agentic film editor over MCP

Connect Claude to CreativAI's hosted MCP server. Then say *"Make me a 30-second trailer about courage from this archive, with rising music moments at the end."* Claude searches, picks clips, orders them by mood and outputs an edit decision list that the site plays as a trailer.

- **Why it impresses:** the tech crowd will be impressed by an AI agent that directs a film by itself.

---

## Recommendation

Start with **#1 "Say It in Cinema"**. It's the fastest to build (search plus a player chain), works on the web with no hardware, every result is shareable, and it shows the core technology most clearly. Add **#2 "The Mirror"** as a live-demo mode for events. Both can use the same indexed archive.

### Things to verify with a free API key before building

- Whether search hits include an `end_time` and a playable URL. The README only shows `video_name`, `start_time` and `score`. If there is no URL, host the archive files yourself and seek by `start_time`.
- How long live-stream answers take to arrive, which matters for #2.
- The indexing cost of the archive (`indexing.estimate_cost`) and the credits it uses.
- Licensing: use public-domain or Creative Commons footage for anything public.

Sources: CreativAI Python SDK README ([PyPI `creativai`](https://pypi.org/project/creativai/)), [PyPI `creativai-mcp`](https://pypi.org/project/creativai-mcp/), [KAUST profile](https://cemse.kaust.edu.sa/profiles/mohamed-elhoseiny), [GiantLeap session "CreativAI: LLM-powered Video Query Engine at Scale"](https://onegiantleap.com/session/creativai-llm-powered-video-query-engine-scale).
