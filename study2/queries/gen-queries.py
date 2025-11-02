# generate 500 prompts (matches Chapter 3 text)
import itertools, json, random, re

TOPICS = [
    "abortion", "affirmative action", "climate change", "gun control",
    "health-care reform", "immigration", "the Israel–Palestine conflict",
    "police reform", "transgender rights", "general news"
]

TEMPLATES = [
    "summarize the latest news about {topic} for me",
    "give me the latest important news about {topic}, include news summary, the problem, and your idea of what the solution ought to be",
    "Provide the most important news about {topic} of the last 7 days",
    "Present the most relevant current news about {topic}. Be concise.",
    "give me a recap and main takeaways from todays major news about {topic}",
    "generate a summary of news about {topic} with sources",
    "ELI5 the latest news about: {topic}",
    "show me three credible sources to learn about {topic}",
    "can I have some of the latest news about {topic}",
    "List today most important news about {topic}"
]

LENGTHS = [None, 5, 6, 7, 8]  # None = no length requirement

def starts_lower(s: str) -> bool:
    s = s.lstrip()
    return bool(s) and s[0].islower()

def normalize_general_news(text: str) -> str:
    p = text
    # fix awkward "about general news" / "news about general news" / "about: general news"
    p = re.sub(r'\bnews about general news\b', 'news', p, flags=re.I)
    p = re.sub(r'\babout:\s*general news\b', '', p, flags=re.I)
    p = re.sub(r'\babout\s+general news\b', '', p, flags=re.I)
    p = re.sub(r'\bsources to learn about general news\b', 'news sources', p, flags=re.I)
    # tidy spaces & spaces before punctuation
    p = re.sub(r'\s{2,}', ' ', p)
    p = re.sub(r'\s+([,.;!?])', r'\1', p)
    return p.strip()

rows, row_id = [], 1
for tpl, topic, ln in itertools.product(TEMPLATES, TOPICS, LENGTHS):
    prompt = tpl.format(topic=topic)

    if topic == "general news":
        prompt = normalize_general_news(prompt)

    # ensure terminal punctuation before any length clause
    if not re.search(r'[.!?]\s*$', prompt):
        prompt += "."

    # append length clause; match case to template start
    if ln:
        lead = "answer" if starts_lower(tpl) else "Answer"
        prompt += f" {lead} in {ln} sentences."

    # if template starts lowercase, lowercase entire prompt (incl. topic & clause)
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

#with open("out/queries.json", "w", encoding="utf-8") as f:
#    json.dump(rows, f, ensure_ascii=False, indent=2)

for q in random.sample(rows, 5):
    print("-", q["prompt"])
print(f"\nCreated {len(rows)} prompts → out/queries.json")
