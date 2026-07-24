#!/usr/bin/env python3
"""Unit / integration tests for .claude/hooks/memory-recall.py

外部依存なし（stdlib の unittest のみ）。実行:

    python3 -m unittest discover -s tests
    # または
    python3 tests/test_memory_recall.py

memory-recall.py はハイフンを含むファイル名で import 不可なため、
importlib で明示的にロードする（`__main__` ガードにより import 時に main() は走らない）。

issue #1 が固定化を求める 3 ケース:
  1. frontmatter 形式のパース          -> ParseTest
  2. ASCII 語境界一致（部分一致の誤爆回避） -> RecallScoringTest.test_ascii_match_respects_word_boundary
  3. CJK 部分一致                       -> RecallScoringTest.test_cjk_substring_match
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOK_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".claude", "hooks", "memory-recall.py")
)

_spec = importlib.util.spec_from_file_location("memory_recall", HOOK_PATH)
assert _spec is not None and _spec.loader is not None
mr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mr)


class ParseTest(unittest.TestCase):
    def test_extracts_frontmatter_and_body(self):
        text = (
            "---\n"
            "date: 2026-07-06\n"
            "tags: [料理, 段取り, 好み]\n"
            "description: 一覧で意味が分かる一行\n"
            "---\n"
            "本文の要点。"
        )
        fm, body = mr.parse(text)
        self.assertEqual(fm["date"], "2026-07-06")
        self.assertEqual(fm["tags"], ["料理", "段取り", "好み"])
        self.assertEqual(fm["description"], "一覧で意味が分かる一行")
        self.assertIn("本文の要点。", body)
        # 本文に frontmatter が混ざっていないこと
        self.assertNotIn("description:", body)

    def test_no_frontmatter_returns_full_body(self):
        text = "見出しなしの素の本文。"
        fm, body = mr.parse(text)
        self.assertEqual(fm, {})
        self.assertEqual(body, text)

    def test_unterminated_frontmatter_is_not_parsed(self):
        # 閉じ --- が無い場合はパースせず全文を body にフォールバック
        text = "---\ndate: 2026-07-06\ntags: [a]\n本文だけで閉じない"
        fm, body = mr.parse(text)
        self.assertEqual(fm, {})
        self.assertEqual(body, text)


class ParseListTest(unittest.TestCase):
    def test_bracketed_and_quoted(self):
        self.assertEqual(mr.parse_list("[料理, 段取り, 好み]"), ["料理", "段取り", "好み"])
        self.assertEqual(mr.parse_list("a, 'b', \"c\""), ["a", "b", "c"])

    def test_empty_variants(self):
        self.assertEqual(mr.parse_list("[]"), [])
        self.assertEqual(mr.parse_list(""), [])
        self.assertEqual(mr.parse_list("[ , ]"), [])


class BuildTermsTest(unittest.TestCase):
    def test_includes_tags_ascii_words_and_cjk_runs(self):
        # ascii/空白で区切られた CJK 連は、その塊がそのまま 1 語になる
        fm = {"tags": ["料理"], "description": "Docker kubernetes 段取り"}
        terms = mr.build_terms(fm)
        self.assertIn("料理", terms)          # tag
        self.assertIn("Docker", terms)        # ascii 語（3文字以上）
        self.assertIn("kubernetes", terms)    # ascii 語
        self.assertIn("段取り", terms)         # CJK 連（2〜6文字）
        # 2文字未満の ascii は拾わない
        self.assertNotIn("k", terms)

    def test_cjk_run_is_greedy_not_word_segmented(self):
        # 実装は形態素解析をせず、連続する CJK/かな列を最大6字の 1 run として拾う。
        # よって "の段取りメモ" は "段取り" 単体には分割されない（既知の挙動を固定化）。
        fm = {"tags": [], "description": "Docker の段取りメモ"}
        terms = mr.build_terms(fm)
        self.assertIn("の段取りメモ", terms)
        self.assertNotIn("段取り", terms)

    def test_dedups_preserving_first_order(self):
        fm = {"tags": ["cat", "dog"], "description": "cat と dog の話"}
        terms = mr.build_terms(fm)
        self.assertEqual(terms.count("cat"), 1)
        self.assertEqual(terms.count("dog"), 1)
        # tag が先、初出順を保つ
        self.assertLess(terms.index("cat"), terms.index("dog"))


class IsAsciiTest(unittest.TestCase):
    def test_ascii_and_non_ascii(self):
        self.assertTrue(mr.is_ascii("docker"))
        self.assertTrue(mr.is_ascii("k8s-2"))
        self.assertFalse(mr.is_ascii("料理"))


def run_hook(prompt, mem_files):
    """一時 project dir に memory/ を作り、フックをサブプロセスで実行して stdout を返す。

    mem_files: {ファイル名: 本文} の dict。None を渡すと memory/ を作らない。
    """
    with tempfile.TemporaryDirectory() as proj:
        if mem_files is not None:
            mem_dir = os.path.join(proj, "memory")
            os.makedirs(mem_dir)
            for fname, content in mem_files.items():
                with open(os.path.join(mem_dir, fname), "w", encoding="utf-8") as f:
                    f.write(content)
        env = dict(os.environ)
        env["CLAUDE_PROJECT_DIR"] = proj
        proc = subprocess.run(
            [sys.executable, HOOK_PATH],
            input=json.dumps({"prompt": prompt}),
            capture_output=True,
            text=True,
            env=env,
        )
        return proc.stdout


CAT_MEMO = (
    "---\n"
    "date: 2026-07-06\n"
    "tags: [cat]\n"
    "description: 猫の世話メモ\n"
    "---\n"
    "餌やりの記録。"
)

RYORI_MEMO = (
    "---\n"
    "date: 2026-07-06\n"
    "tags: [料理]\n"
    "description: 段取りメモ\n"
    "---\n"
    "作り置きの記録。"
)


class RecallScoringTest(unittest.TestCase):
    def test_ascii_match_respects_word_boundary(self):
        # "cat" は "cat" に一致し、注入される
        out = run_hook("I have a cat", {"cat.md": CAT_MEMO})
        self.assertIn("recalled-memory", out)
        self.assertIn("猫の世話メモ", out)

    def test_ascii_no_match_on_substring(self):
        # "cat" は "category" の部分一致では誤爆しない（語境界一致）
        out = run_hook("Pick a category please", {"cat.md": CAT_MEMO})
        self.assertEqual(out.strip(), "")

    def test_cjk_substring_match(self):
        # CJK は語境界が無いため部分一致。"料理" が prompt 中に含まれれば注入
        out = run_hook("今日は料理をした", {"ryori.md": RYORI_MEMO})
        self.assertIn("recalled-memory", out)
        self.assertIn("段取りメモ", out)

    def test_cjk_no_match_when_absent(self):
        out = run_hook("今日は散歩をした", {"ryori.md": RYORI_MEMO})
        self.assertEqual(out.strip(), "")

    def test_output_contains_tags_and_date(self):
        out = run_hook("今日は料理をした", {"ryori.md": RYORI_MEMO})
        self.assertIn("[2026-07-06]", out)
        self.assertIn("tags: 料理", out)

    def test_no_memory_dir_is_silent(self):
        out = run_hook("I have a cat", None)
        self.assertEqual(out.strip(), "")

    def test_empty_prompt_is_silent(self):
        out = run_hook("   ", {"cat.md": CAT_MEMO})
        self.assertEqual(out.strip(), "")

    def test_invalid_json_is_silent(self):
        # 壊れた JSON でも例外を握りつぶして無出力（プロンプトをブロックしない）
        with tempfile.TemporaryDirectory() as proj:
            env = dict(os.environ)
            env["CLAUDE_PROJECT_DIR"] = proj
            proc = subprocess.run(
                [sys.executable, HOOK_PATH],
                input="not json at all",
                capture_output=True,
                text=True,
                env=env,
            )
        self.assertEqual(proc.stdout.strip(), "")
        self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
