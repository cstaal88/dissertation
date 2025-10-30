# generate 500 prompts
import itertools, json, random, re

TOPICS = [
    "abortion", "affirmative action", "climate change", "gun control",
    "health-care reform", "immigration", "the Israel–Palestine conflict",
    "police reform", "transgender rights", "voting rights"
]

TEMPLATES = [
    "summarize the latest news about {topic} for me",
    "give me the latest important news about {topic}, include news summary, the problem, and your idea of what the solution ought to be",
    "Provide the most important news about {topic} of the last 7 days",
    "Present the most relevant current news about {topic}. Be concise.",
    "give me a recap and main takeaways from todays major news about {topic}",
    "generate a summary of news about {topic} with sources",
    "ELI5 the latest news about {topic}",
    "show me three credible sources to learn about {topic}",
    "can I have some of the latest news about {topic}",
    "List today most important news about {topic}"
]

LENGTHS = [None, 5, 6, 7, 8]  # None = no length requirement

def starts_lower(s: str) -> bool:
    s = s.lstrip()
    return bool(s) and s[0].islower()

rows, row_id = [], 1
for tpl, topic, ln in itertools.product(TEMPLATES, TOPICS, LENGTHS):
    prompt = tpl.format(topic=topic)

    if not re.search(r'[.!?]\s*$', prompt):
        prompt += "."

    if ln:
        lead = "Answer"
        prompt += f" {lead} in {ln} sentences."

    # If the template starts lowercase, lowercase the entire prompt (topic included)
    if starts_lower(tpl):
        prompt = prompt.lower()

    rows.append({
        "id": row_id,
        "topic": topic,
        "template": tpl,
        "length": ln or "none",
        "prompt": prompt
    })
    row_id += 1

with open("out/queries.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

for q in random.sample(rows, 5):
    print("-", q["prompt"])
print(f"\nCreated {len(rows)} prompts → out/queries.json")
