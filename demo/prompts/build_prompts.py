"""Single source for all Lost & Found generation prompts.

Run:  python3 demo/prompts/build_prompts.py
Writes demo/prompts/prompts.json and demo/prompts/PROMPTS.md, and injects the
JSON into demo/game-plan.html between the DATA markers.
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- characters
CHARACTERS = {
    "FATHER_A": {
        "role": "the father", "case": "A", "tag": "@FatherA", "name": "Father (case A)",
        "look": "a tall, slim Saudi man in his early 40s with a short, neatly trimmed black beard, wearing a crisp ankle-length white thobe, a red-and-white checkered shemagh held by a black agal, black leather sandals and a silver wristwatch, carrying a dark green paper shopping bag with rope handles in his right hand",
    },
    "MOTHER_A": {
        "role": "the mother", "case": "A", "tag": "@MotherA", "name": "Mother (case A)",
        "look": "a Saudi woman in her mid-30s wearing a plain loose black abaya, a light grey hijab framing her face, black flat shoes, and a beige leather handbag on her left shoulder",
    },
    "BOY_A": {
        "role": "the boy", "case": "A", "tag": "@BoyA", "name": "Boy (case A)",
        "look": "a small 6-year-old boy with short black hair, wearing a plain bright red crew-neck t-shirt with no logo, mid-blue jeans and white sneakers",
    },
    "FATHER_B": {
        "role": "the father", "case": "B", "tag": "@FatherB", "name": "Father (case B)",
        "look": "a Saudi man in his mid-30s of average build with a full dark beard, wearing a light grey ankle-length thobe, a plain white ghutra held by a black agal, brown leather sandals, and a black backpack on one shoulder",
    },
    "MOTHER_B": {
        "role": "the mother", "case": "B", "tag": "@MotherB", "name": "Mother (case B)",
        "look": "a Saudi woman wearing a black abaya with dark navy embroidery along the sleeves and hem, a black hijab and black niqab, with a grey baby stroller carrying a baby under a white blanket",
    },
    "GIRL_B": {
        "role": "the girl", "case": "B", "tag": "@GirlB", "name": "Girl (case B)",
        "look": "a 7-year-old girl with long black hair in a high ponytail tied with a yellow hair tie, wearing a bright yellow hoodie, light pink leggings and white sneakers, holding a small purple plush bunny",
    },
    "LOOK_FATHER_A": {
        "role": "the other father", "case": "A", "tag": None, "name": "Lookalike father (trick, case A)",
        "look": "a Saudi man in his late 30s with a short black beard, wearing a white thobe and a red-and-white checkered shemagh with a black agal, empty-handed with no shopping bag",
    },
    "LOOK_MOTHER_A": {
        "role": "the other mother", "case": "A", "tag": None, "name": "Lookalike mother (trick, case A)",
        "look": "a woman in a plain black abaya with a light grey hijab",
    },
    "LOOK_BOY_A": {
        "role": "the other boy", "case": "A", "tag": None, "name": "Lookalike boy (trick, case A)",
        "look": "a 6-year-old boy with short black hair wearing a bright red t-shirt, black shorts and white sneakers",
    },
    "LOOK_GIRL_B": {
        "role": "the other girl", "case": "B", "tag": None, "name": "Lookalike girl (trick, case B)",
        "look": "a 7-year-old girl with long black hair in a ponytail, wearing a bright yellow hoodie, blue jeans and pink sneakers, holding no toy",
    },
    "LOOK_MOTHER_B": {
        "role": "her mother", "case": "B", "tag": None, "name": "Lookalike girl's mother (trick, case B)",
        "look": "a woman in a plain black abaya and black niqab carrying a white shopping bag",
    },
    "GUARD": {
        "role": "the guard", "case": "AB", "tag": "@Guard", "name": "Security guard (both cases)",
        "look": "a male mall security guard in his 30s wearing a dark navy security uniform jacket over a light blue shirt, black trousers, black shoes, a black walkie-talkie clipped to his chest and an ID badge",
    },
}

def character_image_prompts(c):
    look = c["look"]
    sheet = (
        f"Photorealistic full-body character reference sheet of {look}. "
        "Three views of the same person side by side on one image: front view, left side view, back view. "
        "Standing straight, arms relaxed, neutral expression, the whole body visible from head to shoes. "
        "Plain light grey studio background, soft even lighting, no shadows on the background, sharp focus, "
        "natural skin texture, realistic fabric folds. No text, no logos, no props other than those described."
    )
    front = (
        f"Photorealistic full-body photo of {look}, facing the camera, standing on a plain light grey studio background. "
        "Head to shoes in frame, soft even lighting, neutral expression, realistic fabric and skin detail, sharp focus. "
        "No text, no logos."
    )
    back = (
        f"Photorealistic full-body photo of {look}, seen from behind and slightly to the side, walking away, on a plain light grey studio background. "
        "Head to shoes in frame, soft even lighting, realistic fabric detail. No text, no logos."
    )
    return {"sheet": sheet, "front": front, "back": back}

# ---------------------------------------------------------------- camera look
CAMERA = (
    "Security-camera recording from a fixed camera mounted high on the ceiling, about four metres up, "
    "angled about forty degrees down, with a wide-angle lens and slight barrel distortion at the edges. "
    "Locked-off static shot: the camera does not pan, tilt, zoom or shake at any moment. "
    "Flat even LED mall lighting, slightly washed-out colours, mild digital noise and light video compression, "
    "everything in focus, no cinematic depth of field, real-time speed."
)
NEGATIVE = (
    "camera movement, pan, tilt, zoom, dolly, tracking shot, handheld shake, cuts, scene change, cinematic lighting, "
    "shallow depth of field, bokeh, slow motion, lens flare, text, subtitles, timestamp, watermark, logo, "
    "distorted faces, extra limbs, merged people, morphing clothes, clothes changing colour, flicker, cartoon, CGI look"
)

SCENES = {
    "ENT-01": "The inside of a modern Saudi shopping mall's main entrance. Tall glass sliding doors at the bottom of the frame with bright daylight outside. A wide polished beige marble floor, a walk-through security gate beside the doors, potted palm trees on both sides. The camera faces the doors, so people who come in walk toward and under the camera.",
    "ENT-02": "The inside of the mall's parking-level entrance at night. A pair of automatic glass doors at the bottom of the frame with a dim grey car park outside, a light grey tiled floor, an elevator lobby on the left, a pillar with a blank directory board on the right. The camera faces the doors, so people who come in walk toward and under the camera.",
    "STR-A": "Inside a women's clothing store in the mall. Long racks of dresses and abayas in rows, wall shelves of folded clothes, warm white light, a full-length mirror on the right, the glass store entrance at the bottom of the frame.",
    "STR-B": "Inside an electronics store in the mall. White display tables in rows with phones, tablets and laptops on them, bright white light, accessory shelves along the back wall, and the open glass store entrance on the right side of the frame leading to the mall corridor.",
    "STR-C": "Inside a toy store in the mall. Low colourful shelves full of plush toys and boxed toys, a small play table with large building blocks in the middle of the floor, bright cheerful lighting, a cashier counter at the top right, the store entrance at the bottom left of the frame.",
    "ATR-01": "A large two-storey mall atrium seen from high above. A round fountain in the centre with benches around it, escalators at the back, shopfronts around the edges, a cream marble floor with a geometric pattern.",
    "COR-W": "A long straight mall corridor stretching away from the camera, shopfronts with glass windows on both sides, a cream marble floor, rows of ceiling lights, a few decorative planters down the middle. The far end opens toward a food court.",
    "COR-E": "A long straight mall corridor stretching away from the camera, shopfronts with glass windows on both sides, a cream marble floor, rows of ceiling lights, pillars along the right side.",
    "FC-01": "A large busy mall food court seen from above. Rows of square tables with chairs, families eating, trays of food, a carpeted family section on the left, restaurant counters along the far wall.",
    "FC-02": "A row of fast-food counters in a mall food court. Illuminated menu boards above the counters with no readable text, queues of customers in front of each counter, a few tables in the foreground.",
    "INF-01": "The mall's information and security desk. A curved white desk with a monitor, a uniformed guard standing behind it, a small seating area to the side, a corridor in the background.",
}

CROWD_DAY = "A normal weekday-afternoon crowd moves through the background: other men in white thobes, women in black abayas, teenagers and families, so the main characters are not the only people in similar clothes."
CROWD_NIGHT = "A busy evening crowd moves through the background: many men in white and grey thobes, women in black abayas, families with children and strollers, so the main characters are not the only people in similar clothes."

# ---------------------------------------------------------------- clips
# id, case, cam, clock, priority(1 = must-have), role, title, cast, action beats, crowd, audio, why
CLIPS = [
    # ---------------- Case A (build set): afternoon, boy in red, separated in an electronics store
    ("A1", "A", "ENT-01", "14:02:00", 1, "fam", "The family arrives", ["FATHER_A", "MOTHER_A", "BOY_A"],
     ["0–3 s: shoppers come in through the glass doors in ones and twos.",
      "3–9 s: [FATHER_A], [MOTHER_A] and [BOY_A] walk in together through the doors. The boy holds his mother's hand on her right side; the father walks one step ahead.",
      "9–15 s: the three keep walking straight toward the camera and pass underneath it, out of the bottom of the frame. Their faces and clothes are clearly visible as they approach."],
     CROWD_DAY, "Ambient mall sound: footsteps, the doors sliding, distant chatter.",
     "Captures the whole family, and the boy's look, when they arrive."),
    ("A2", "A", "STR-A", "14:08:00", 1, "fam", "Shopping together", ["FATHER_A", "MOTHER_A", "BOY_A"],
     ["0–5 s: [MOTHER_A] slides dresses along a rack in the middle of the frame, looking at each one.",
      "5–10 s: [BOY_A] stands right next to her, holding the edge of her abaya, swinging slightly and looking around the store.",
      "10–15 s: [FATHER_A] waits two metres away near the mirror, holding the green shopping bag and checking his phone. The family stays together the whole time."],
     "Two or three other women browse the racks in the background.", "Quiet store ambience.",
     "Proves the boy is still with the family at 14:08."),
    ("A3", "A", "STR-B", "14:18:50", 1, "both", "The separation", ["FATHER_A", "MOTHER_A", "BOY_A"],
     ["0–4 s: [FATHER_A] stands at a display table in the centre, holding a phone and testing it with both hands. [MOTHER_A] stands behind him at the left, talking on her own mobile phone with her back half-turned to the boy.",
      "4–9 s: [BOY_A], standing beside the father, looks bored, lets go of the table and slowly wanders between the display tables toward the open store entrance on the right.",
      "9–13 s: the boy walks out through the entrance into the mall corridor and disappears from the frame.",
      "13–15 s: both parents are still busy with their phones and do not look up. The boy is no longer in the store."],
     "A salesman in a black polo shirt helps another customer at the back.", "Store ambience, faint phone ringtones.",
     "The key moment the system must find: the boy leaves the parents."),
    ("A4", "A", "ATR-01", "14:20:00", 1, "kid", "The boy alone", ["BOY_A"],
     ["0–4 s: shoppers cross the atrium in different directions around the fountain.",
      "4–11 s: [BOY_A] walks alone from the top right of the frame across the atrium toward the bottom left, past the fountain, looking left and right as if searching for someone. No adult is with him.",
      "11–15 s: he keeps walking and leaves the frame at the bottom left."],
     CROWD_DAY, "Ambient atrium sound: fountain water, footsteps, chatter.",
     "First sighting of the boy alone, heading west toward the food court."),
    ("A5", "A", "FC-02", "14:23:00", 1, "kid", "Lost at the food court", ["BOY_A"],
     ["0–5 s: customers queue at the counters and carry trays.",
      "5–12 s: [BOY_A] stands still alone in the open space beside a counter in the middle of the frame, turning his head around anxiously, rubbing his eyes as if about to cry. Adults walk past him without stopping.",
      "12–15 s: he stays in the same spot, alone, looking around."],
     CROWD_DAY + " Several other children are with their parents in the queues.", "Food court noise, a child sniffling.",
     "Where the boy is now: the answer the guard needs."),
    ("A6", "A", "FC-01", "14:24:00", 1, "trick", "Trick: lookalike family", ["LOOK_FATHER_A", "LOOK_MOTHER_A", "LOOK_BOY_A"],
     ["0–5 s: The other family sits together at a table in the centre of the frame eating burgers and fries; the other boy sits between his parents.",
      "5–11 s: The other boy stands up on his chair and laughs; the other mother helps him sit down again and the other father hands him a drink.",
      "11–15 s: The three keep eating together. The boy never leaves the table and is never alone."],
     CROWD_DAY, "Food court noise, cutlery, a child laughing.",
     "TRICK: a different family dressed almost like family A, with a boy in red. The system must say 'not our boy' (he is with his parents, wears shorts, and the real family is elsewhere at that time)."),

    # ---------------- Case B (BLIND TEST, sealed until the code is frozen): evening, girl in yellow, ends in the toy store
    ("B1", "B", "ENT-02", "19:10:00", 1, "fam", "The family arrives", ["FATHER_B", "MOTHER_B", "GIRL_B"],
     ["0–3 s: people come in through the automatic doors from the car park.",
      "3–9 s: [FATHER_B], [MOTHER_B] pushing the stroller, and [GIRL_B] walk in together. The girl holds the side of the stroller with one hand and her purple bunny in the other.",
      "9–15 s: they walk straight toward the camera and pass underneath it, out of the bottom of the frame. Their clothes and the stroller are clearly visible."],
     CROWD_NIGHT, "Doors sliding, footsteps, car park echo.",
     "Captures the family, the stroller and the girl's look on arrival."),
    ("B2", "B", "COR-W", "19:14:00", 1, "fam", "Walking to the food court", ["FATHER_B", "MOTHER_B", "GIRL_B"],
     ["0–4 s: the evening crowd walks in both directions along the corridor.",
      "4–12 s: [FATHER_B], [MOTHER_B] with the stroller, and [GIRL_B] walk together away from the camera down the middle of the corridor toward the food court. The girl skips beside the stroller.",
      "12–15 s: they get smaller in the distance, still together."],
     CROWD_NIGHT, "Corridor ambience.",
     "Proves the girl is still with the family at 19:14."),
    ("B3", "B", "FC-01", "19:21:00", 1, "both", "The separation", ["FATHER_B", "MOTHER_B", "GIRL_B"],
     ["0–4 s: the family sits at a table in the middle of the frame. [MOTHER_B] bends over the stroller beside the table, busy with the crying baby. [FATHER_B] stands up and walks away toward the restaurant counters at the far wall.",
      "4–9 s: [GIRL_B], sitting at the table, watches a group of children walk past, gets off her chair holding her purple bunny and follows them toward the right edge of the frame.",
      "9–13 s: she walks out of the frame on the right, toward the corridor, alone.",
      "13–15 s: the mother is still focused on the baby and the father is in the queue. The girl's chair is empty."],
     CROWD_NIGHT, "Food court noise, a baby crying.",
     "The key moment: the girl leaves while both parents are busy."),
    ("B4", "B", "ATR-01", "19:23:00", 1, "kid", "The girl alone", ["GIRL_B"],
     ["0–4 s: the evening crowd crosses the atrium around the fountain.",
      "4–11 s: [GIRL_B] walks alone from the bottom left of the frame across the atrium toward the top right, hugging her purple bunny, looking at the shops. No adult is with her.",
      "11–15 s: she keeps walking and leaves the frame at the top right, toward the east corridor."],
     CROWD_NIGHT, "Fountain water, footsteps, chatter.",
     "Same atrium camera as case A, opposite direction: the girl heads east."),
    ("B5", "B", "STR-C", "19:26:00", 1, "kid", "In the toy store", ["GIRL_B"],
     ["0–4 s: two other children play with their mother near the shelves at the back.",
      "4–12 s: [GIRL_B] walks in from the entrance at the bottom left, alone, goes to the play table in the middle and starts stacking the big building blocks, calm and absorbed. Nobody is with her.",
      "12–15 s: she keeps playing alone; the cashier at the counter does not notice her."],
     "A cashier stands behind the counter; one family browses the shelves.", "Store music, children's voices.",
     "Where the girl is now: calm, but alone in a toy store, a very common real case."),
    ("B6", "B", "COR-E", "19:30:00", 1, "trick", "Trick: false alarm", ["LOOK_GIRL_B", "LOOK_MOTHER_B"],
     ["0–4 s: The evening crowd walks along the corridor in both directions.",
      "4–9 s: The other girl walks quickly toward the camera down the middle of the corridor, alone, looking into the shop windows.",
      "9–13 s: Her mother hurries after her from behind, catches up and takes her hand; the girl smiles up at her.",
      "13–15 s: They walk on together, hand in hand, and pass under the camera out of the bottom of the frame."],
     CROWD_NIGHT, "Corridor ambience.",
     "TRICK: a girl in a yellow hoodie is briefly alone, but her mother catches up. The system must NOT raise an alarm or confuse her with the lost girl (who is in the toy store since 19:25)."),

    # ---------------- Extras: only if spare credits remain at the end (demo video)
    ("A7", "A", "INF-01", "14:27:00", 3, "ok", "Report to security", ["FATHER_A", "MOTHER_A", "GUARD"],
     ["0–4 s: [GUARD] stands behind the desk. [FATHER_A] and [MOTHER_A] arrive quickly at the desk.",
      "4–11 s: the mother speaks urgently, showing a child's height with her hand at waist level; the father points back toward the corridor.",
      "11–15 s: the guard nods, lifts his walkie-talkie and speaks into it."],
     "One or two people wait on the seating area.", "Urgent conversation, radio static.",
     "The moment the case starts in our website."),
    ("A8", "A", "FC-02", "14:33:00", 3, "ok", "Reunion", ["FATHER_A", "MOTHER_A", "BOY_A", "GUARD"],
     ["0–4 s: [BOY_A] stands alone beside the counter, as before.",
      "4–9 s: [GUARD] walks in from the bottom of the frame with [FATHER_A] and [MOTHER_A] right behind him.",
      "9–15 s: the mother runs to the boy, kneels and hugs him tightly; the father puts his hand on the boy's head; the guard stands next to them, relieved."],
     CROWD_DAY, "Food court noise.",
     "The happy ending for the demo video."),
]

def build_prompt(clip, use_tags):
    cid, case, cam, clock, prio, role, title, cast, beats, crowd, audio, why = clip
    def sub(text):
        for key in cast:
            text = text.replace(f"[{key}]", CHARACTERS[key]["role"])
        text = re.sub(r"([.:] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
        return text[0].upper() + text[1:] if text else text
    if use_tags:
        chars = " ".join(
            f"{CHARACTERS[k]['role'].capitalize()} is {CHARACTERS[k]['tag']}." if CHARACTERS[k]["tag"]
            else f"{CHARACTERS[k]['role'].capitalize()}: {CHARACTERS[k]['look']}."
            for k in cast)
    else:
        chars = " ".join(f"{CHARACTERS[k]['role'].capitalize()}: {CHARACTERS[k]['look']}." for k in cast)
    parts = [
        "Scene: " + SCENES[cam],
        "Characters: " + chars[0].upper() + chars[1:],
        "Action: " + " ".join(sub(b) for b in beats),
        "Background: " + crowd,
        "Camera and look: " + CAMERA,
        "Audio: " + audio,
    ]
    return "\n\n".join(parts)

# ---------------------------------------------------------------- CreativAI questions ("the Eyes")
# {child}, {family} and {child_short} are filled per case. The same templates are used for
# both cases: the code must not get case-specific wording.
QUERIES = [
    ("Q1", "search", "Find the family on arrival",
     "{family}, walking into the mall together"),
    ("Q2", "column", "Is the child still with them? (one answer per family clip)",
     "Is a small child walking, standing or sitting together with these adults in this clip? Answer yes or no. If the child leaves them, give the second it happens."),
    ("Q3", "search", "Find the separation moment",
     "a small child walking away alone while the parents are busy and do not notice"),
    ("Q4", "search", "Find the child alone",
     "{child}, alone, with no adult next to them"),
    ("Q5", "column", "Confirm it is really alone (filters out tricks)",
     "Is this child alone, with no parent or adult looking after them, for the whole clip? Answer yes or no, and say if an adult joins them later."),
    ("Q6", "column", "Describe the child (to compare with the report)",
     "Describe the child's clothes, hair and anything they are holding, in one sentence."),
    ("Q7", "chat", "Guard's question at the end",
     "Where is the {child_short} now, and how did they get there? Give the camera and time of each sighting."),
]
CASE_TERMS = {
    "A": {"family": "a man in a white thobe and red-and-white checkered shemagh carrying a dark green shopping bag, a woman in a black abaya and light grey hijab, and a small boy in a bright red t-shirt and blue jeans",
          "child": "a small boy of about 6 in a bright red t-shirt, blue jeans and white sneakers", "child_short": "boy in the red t-shirt"},
    "B": {"family": "a man in a light grey thobe and white ghutra with a black backpack, a woman in a black abaya and niqab with a grey baby stroller, and a small girl in a bright yellow hoodie and pink leggings",
          "child": "a small girl of about 7 in a bright yellow hoodie and light pink leggings holding a purple plush bunny", "child_short": "girl in the yellow hoodie"},
}

def main():
    data = {
        "camera": CAMERA, "negative": NEGATIVE,
        "characters": [
            {"key": k, **v, "images": character_image_prompts(v) if v["tag"] else None} for k, v in CHARACTERS.items()
        ],
        "clips": [
            {"id": c[0], "case": c[1], "cam": c[2], "clock": c[3], "priority": c[4], "role": c[5],
             "title": c[6], "cast": c[7], "why": c[11],
             "prompt_tags": build_prompt(c, True), "prompt_full": build_prompt(c, False)}
            for c in CLIPS
        ],
        "queries": [
            {"id": q[0], "kind": q[1], "purpose": q[2], "template": q[3],
             "A": q[3].format(**CASE_TERMS["A"]), "B": q[3].format(**CASE_TERMS["B"])}
            for q in QUERIES
        ],
    }
    for c in data["clips"]:
        assert len(c["prompt_full"]) <= 2500, (c["id"], len(c["prompt_full"]))
    (HERE / "prompts.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
    old = HERE / "PROMPTS.md"
    if old.exists():
        old.unlink()

    head = "_Generated by `build_prompts.py`. Edit the script, not this file._\n"
    # 01 characters
    md = ["# 01 · Character pictures\n", head,
          "Make these **before any video**. For each character: the reference sheet, then the front and back photos. "
          "In Kling (Higgsfield) create one **Element** per character from its pictures, named exactly with the tag.\n",
          "The strangers in the trick clips get **no pictures and no Elements**: they are described in full inside their clip prompt.\n"]
    for ch in data["characters"]:
        if not ch["images"]:
            continue
        md.append(f"## {ch['name']} → Element `{ch['tag']}`\n")
        for k, label in (("sheet", "Reference sheet"), ("front", "Front photo"), ("back", "Back photo")):
            md.append(f"**{label}**\n\n```\n{ch['images'][k]}\n```\n")
    (HERE / "01-characters.md").write_text("\n".join(md))

    def clip_md(title, intro, ids):
        out = [f"# {title}\n", head, intro]
        for c in data["clips"]:
            if c["id"] not in ids:
                continue
            out.append(f"## {c['id']} · {c['clock'][:5]} · {c['cam']} · {c['title']}\n")
            out.append(f"_Why:_ {c['why']}\n")
            out.append(f"**With Elements**\n\n```\n{c['prompt_tags']}\n```\n")
            out.append(f"**Without Elements**\n\n```\n{c['prompt_full']}\n```\n")
        return "\n".join(out)
    (HERE / "02-clips-case-A.md").write_text(clip_md(
        "02 · Case A clips (build set)",
        "Settings: Kling 3.0, 16:9, 15 s. Paste the negative prompt from `05-negative-prompt.txt` if there is a field for it.\n"
        "We build and tune the whole system on these 6 clips.\n",
        ["A1", "A2", "A3", "A4", "A5", "A6"]))
    (HERE / "03-clips-case-B-blind-test.md").write_text(clip_md(
        "03 · Case B clips (blind test)",
        "Generate these like the others, but **upload them only to `demo/raw/case-B/` and do not run anything on them** "
        "until the code is frozen (see `demo/test-plan.md`). Then the system gets one try.\n",
        ["B1", "B2", "B3", "B4", "B5", "B6"]))
    (HERE / "04-extras-if-credits-left.md").write_text(clip_md(
        "04 · Extras (only if spare credits remain)",
        "Not needed for testing. Nice for the demo video. Use leftover spare credits in this order: A7, then A8.\n",
        ["A7", "A8"]))
    (HERE / "05-negative-prompt.txt").write_text(NEGATIVE + "\n")

    q = ["# 06 · CreativAI questions (the Eyes)\n", head,
         "The system sends these to CreativAI. **Same templates for both cases**; only the description of the family and child "
         "is filled in from the guard's report. `search` = search.query, `column` = a knowledge-extraction column on a data plate, "
         "`chat` = agentic chat.\n"]
    for item in data["queries"]:
        q.append(f"## {item['id']} · {item['purpose']} ({item['kind']})\n")
        q.append(f"Template:\n\n```\n{item['template']}\n```\n")
        if item["A"] != item["template"]:
            q.append(f"Case A:\n\n```\n{item['A']}\n```\n\nCase B:\n\n```\n{item['B']}\n```\n")
    (HERE / "06-creativai-questions.md").write_text("\n".join(q))

    page = HERE.parent / "game-plan.html"
    if page.exists():
        html = page.read_text()
        blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        html, n = re.subn(r"/\*DATA\*/.*?/\*END\*/", lambda m: f"/*DATA*/{blob}/*END*/", html, flags=re.S)
        if n:
            page.write_text(html)
    print("clips:", len(data["clips"]), "max prompt chars:", max(len(c["prompt_full"]) for c in data["clips"]))

if __name__ == "__main__":
    main()
