#!/usr/bin/env python3
"""
Tier-2 memory recall hook (UserPromptSubmit).

送信プロンプト(JSON)を標準入力で受け取り、gitignore された memory/*.md を
frontmatter の tags / description のキーワード重なりでスコアリングして、
関連する上位だけをコンテキストへ注入する。

設計方針:
- memory/ が無い・空・無マッチなら *何も出力せず* exit 0（ストアが育つまでコストゼロ）。
- 例外時も必ず exit 0（ユーザーのプロンプトを絶対にブロックしない）。
- 索引(MEMORY.md)には載せない高頻度ストアを、必要時だけ薄く引くための仕組み。

配線（settings.json）:
    {
      "hooks": {
        "UserPromptSubmit": [
          { "hooks": [ { "type": "command",
              "command": "python3 .claude/hooks/memory-recall.py" } ] }
        ]
      }
    }

memory ファイルの形式:
    ---
    date: 2026-07-06
    tags: [料理, 段取り, 好み]
    description: 一覧で意味が分かる一行（呼び出しの鍵）
    ---
    本文（やり取りの要点）。tags と description がマッチの入口になる。
"""
import sys
import os
import json
import re

MAX_HITS = 5          # 注入する最大エントリ数
BODY_CHARS = 600      # 各本文の最大注入文字数
MIN_SCORE = 1         # これ未満は無視


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except Exception:
        return 0

    prompt = (data.get("prompt") or "")
    if not prompt.strip():
        return 0

    proj = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    mem_dir = os.path.join(proj, "memory")
    if not os.path.isdir(mem_dir):
        return 0

    prompt_l = prompt.lower()

    hits = []
    for name in sorted(os.listdir(mem_dir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(mem_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue

        fm, body = parse(text)
        tags = fm.get("tags", [])
        terms = build_terms(fm)

        score = 0
        for t in terms:
            tl = t.lower()
            if len(tl) < 2:
                continue
            weight = 2 if t in tags else 1
            if is_ascii(tl):
                # ascii は語境界一致（部分一致の誤爆を避ける）
                if re.search(r"(?<![a-z0-9])" + re.escape(tl) + r"(?![a-z0-9])", prompt_l):
                    score += weight
            else:
                # CJK は部分一致（語境界が無いため）
                if tl in prompt_l:
                    score += weight

        if score >= MIN_SCORE:
            hits.append((score, fm, body))

    if not hits:
        return 0

    hits.sort(key=lambda h: h[0], reverse=True)
    hits = hits[:MAX_HITS]

    out = ['<recalled-memory source="Tier-2 / injected only when relevant / unverified store">']
    for hit in hits:
        fm, body = hit[1], hit[2]
        date = fm.get("date", "")
        desc = fm.get("description", "")
        tags = ",".join(fm.get("tags", []))
        b = " ".join(body.split())
        if len(b) > BODY_CHARS:
            b = b[:BODY_CHARS] + "…"
        head = f"- [{date}] {desc}".rstrip()
        if tags:
            head += f" (tags: {tags})"
        out.append(head)
        if b:
            out.append(f"  {b}")
    out.append("</recalled-memory>")

    sys.stdout.write("\n".join(out) + "\n")
    return 0


def is_ascii(s):
    try:
        s.encode("ascii")
        return True
    except Exception:
        return False


def parse(text):
    """超軽量フロントマター parser（PyYAML 非依存・stdlib のみ）。"""
    fm = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end]
            body = text[end + 4:]
            for line in block.splitlines():
                line = line.strip()
                if not line or ":" not in line:
                    continue
                k, _, v = line.partition(":")
                k = k.strip()
                v = v.strip()
                if k == "tags":
                    fm["tags"] = parse_list(v)
                else:
                    fm[k] = v
    return fm, body


def parse_list(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
    items = [x.strip().strip("'\"") for x in v.split(",")]
    return [x for x in items if x]


def build_terms(fm):
    """マッチ候補語: tags + 説明中の ascii 語 + 説明中の短い CJK 連。"""
    terms = list(fm.get("tags", []))
    desc = fm.get("description", "")
    for w in re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", desc):
        terms.append(w)
    for run in re.findall(r"[぀-ヿ一-鿿]{2,6}", desc):
        terms.append(run)
    seen = set()
    ordered = []
    for t in terms:
        if t not in seen:
            seen.add(t)
            ordered.append(t)
    return ordered


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
