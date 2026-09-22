# Chapter style — beginner first, then exam

Audience: someone new to AWS who wants to **understand** and pass **SAA-C03**.

## Required section order

1. **Title + pills + one short lede** (plain English, one or two sentences).
2. **`Start here — the W questions`** inside `<div class="fundamentals">` with a `.w-grid` of cards:
   - **Why** does this exist? (the human problem)
   - **What** is it? (simple definition, no jargon pile)
   - **Where** does it live? (global / Region / AZ / edge / VPC)
   - **Which** pieces matter for SAA? (3–6 named building blocks only)
3. **Core knowledge** — short subsections that teach foundations before features. Define every term the first time you use it.
4. **How it works** — prefer the flow from official AWS docs. Use `<div class="doc-figure">` + Mermaid that mirrors the AWS numbered steps, and link the official page in the caption. Invent a new diagram only when AWS has no clear overview.
5. **Use cases** — real “you need X when…” scenarios with a small diagram each if helpful.
6. **How to choose** — table of stem language → pick → not.
7. **Case studies** — 2–3 exam-style A/B/C/D with plain-English why wrong/right.
8. **Tricky points** — distractors, still explained simply.
9. **Official AWS docs** + **Related pages**.

## Writing rules

- Short paragraphs (2–4 sentences). Prefer “Route 53 is AWS’s DNS service” over dense clause stacks.
- Explain **why** before **how**. Never open with exam traps.
- When you must use a term (alias, TTL, Multi-AZ), define it in the same paragraph.
- Do not write cheat-sheet dumps or “memorize this list” walls.
- Links to AWS docs are required; captions should say which official concept the diagram follows.

## HTML snippets

```html
<div class="fundamentals">
  <h2>Start here — the W questions</h2>
  <div class="w-grid">
    <div class="w-card"><h3>Why</h3><p>...</p></div>
    <div class="w-card"><h3>What</h3><p>...</p></div>
    <div class="w-card"><h3>Where</h3><p>...</p></div>
    <div class="w-card"><h3>Which pieces matter</h3><p>...</p></div>
  </div>
</div>
```

```html
<div class="doc-figure">
  <div class="mermaid">...</div>
  <p class="caption">Follows the flow in <a href="..." target="_blank" rel="noopener">AWS docs: …</a>. Open that page to see AWS’s official diagram.</p>
</div>
```
