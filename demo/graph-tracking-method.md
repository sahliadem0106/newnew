# Graph-constrained tracking: how the system finds the child

## The idea in one sentence
We **can't search all cameras for all time** for a person, and appearance alone gives false matches. But people **walk along the camera graph**: from one camera they can only reach its neighbours, and only within a realistic time window. So we search **only where and when the person could physically be**, one hop at a time.

## Inputs
- **Camera graph** `G` (`mall_topology.json`): nodes = cameras, edges = walkways with a length.
- **Footage index:** every clip uploaded to one CreativAI collection, tagged with `camera` and `start_time`.
- **Report:** the parents at the security desk.

## Why clothing first, faces optional
- A guard "scans" the parent by **taking a photo at the desk**. The parent is wearing the same clothes as in all of today's footage.
- A vision model turns the photo into an **appearance signature** in words: *"man, white thobe, red-and-white checkered shemagh, black sandals, dark green shopping bag"*. CreativAI's search works on exactly this kind of text.
- Clothing is visible from behind, from far away and from high angles, where faces aren't.
- Privacy: no face database. The family consents to their own photo for this case only.
- In our AI-generated demo, faces change between clips, but clothing stays the same. A face-based method would break; this one doesn't.

## Step by step

### Step 1: Anchor
The guard's photo plus the current camera and time: `FATHER @ INF-01, 14:27`. That's the first node of the parents' track.

### Step 2: Trace the parents backwards through the graph
From a sighting at camera `c`, starting at time `t`:
1. For each neighbour `n` of `c` (walkway length `d`), the person must have been at `n` in the window
   `[t − d / v_min, t − d / v_max]` (with `v` the walking speeds in the topology file).
2. Search CreativAI for the appearance signature, **keeping only hits from camera `n` in that window**.
3. Score each hit: `score = appearance_similarity × transit_plausibility`. The plausibility is highest when the implied walking speed is normal and drops for speeds that are too fast or too slow.
4. Keep the best few candidates (beam search) and repeat from them.
5. If no neighbour has a hit, it's a **blind spot**: allow a two-hop jump with a wider window and a lower score.

The result is the parents' full path:
`ENT-01 → ATR-01 → COR-W → STR-A → COR-W → ATR-01 → STR-B → ATR-01 → COR-E → INF-01`

### Step 3: Find the separation moment
For every sighting on the parents' path, ask CreativAI **"Is a small child walking with them or holding their hand?"** (a question column on those segments).
- Last sighting **with** the child: `STR-B 14:16–14:23` (the child is there and leaves at 14:19).
- First sighting **without** the child: `ATR-01 14:23:50`.
- So the separation happened **inside STR-B**. Search STR-B for "child walking away alone" and it lands on **14:19:10**.

### Step 4: Learn what the child looks like from the parents' footage
We don't need a photo of the child. The earliest family sighting (`ENT-01 14:02`) shows him with his parents. A vision model describes him: *"boy about 6, bright red t-shirt, blue jeans, white sneakers"*. That becomes the child's signature, and the parents only have to confirm it.

### Step 5: Trace the child forwards from the separation point
Same graph search as Step 2, but **forward in time**, starting at `STR-B 14:19:10` with child walking speeds:
`STR-B → ATR-01 (14:20) → COR-W (14:21) → FC-01 (14:22) → FC-02 (14:23, still there)`

- **Decoys are rejected by the graph.** The boy in red at FC-01 sitting with his parents has the right shirt, but the question *"Is the child alone?"* says no, and his own path doesn't connect back to STR-B. The orange-shirt boy at ENT-01 fails on appearance.
- **Current location:** the last sighting is FC-02 with no exit seen. The prediction is *"still in the food court"*, with FC-01 and COR-W the next most likely spots if he moves.

### Step 6: Dispatch + the cause
- The guard nearest to FC-02 gets an alert: last sighting, clip, path.
- The parents searched **east** (COR-E) while the child went **west**. The graph shows this immediately; without it they would have kept searching the wrong half of the mall.
- Case record: *separated in an electronics store while both parents were distracted; the child left through the main door unseen*. Across many cases, this shows which places and situations cause separations.

## How CreativAI is used

| Need | CreativAI |
|---|---|
| Store footage per camera with time | `media.upload_file` + `confirm_upload(tags={"*": ["cam:STR-B", "start:14:16:40"]})` |
| "Find this person" | `search.query(cid, signature, search_type="vision")`, then filter by camera tag and time window |
| "Is a child with them? Is the child alone?" | `data_plates` + `knowledge_extraction.add_columns` on the returned segments |
| "Child walking away alone" (separation) | `search.query` limited to the separation camera |
| Guard asks questions | `agentic_chat`: "Where was the boy at 14:21?" |
| Brain | Claude agent via CreativAI MCP: runs the graph search, explains each step |

## Things to confirm with the API
- Whether `search.query` can filter by tags directly or we filter after. Either works for a 12-camera demo.
- That each hit returns the clip name and `start_time`, so absolute time = clip start + offset.
- Whether an **image** can be used as a query. If yes, the guard's photo can be searched directly instead of being described in words first.
