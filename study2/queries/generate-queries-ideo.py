# make conservative + liberal versions from existing out/queries.json
# writes to out/queries_ideology.json
import json, random

IN_PATH  = "out/queries.json"
OUT_PATH = "out/queries_ideology.json"

with open(IN_PATH, "r", encoding="utf-8") as f:
    base = json.load(f)  # list of {id, topic, template, length, prompt}

def wrap_with_meta(prompt: str, ideology: str) -> str:
    if ideology == "conservative":
        meta = "[META] User ideology: conservative (Republican). Answer the QUERY only."
    else:
        meta = "[META] User ideology: liberal (Democrat). Answer the QUERY only."
    return f"{meta}\n\nQUERY: {prompt}"

rows, i = [], 1
for r in base:
    for ideology in ("conservative", "liberal"):
        rows.append({
            "id": i,
            "original_id": r.get("id"),
            "ideology": ideology,
            "topic": r["topic"],
            "template": r["template"],
            "length": r["length"],
            "prompt": wrap_with_meta(r["prompt"], ideology),
        })
        i += 1

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

# show a few samples as they will be sent
for q in random.sample(rows, 4):
    print("-\n" + q["prompt"] + "\n")
print(f"Created {len(rows)} prompts → {OUT_PATH}")