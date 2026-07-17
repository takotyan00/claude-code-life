# journal/ — 対話式日記

年/月/日（`journal/YYYY/MM/DD.md`）形式で日々の記録を置く。`/journal` スキルが会話から自動整形して保存する。

- frontmatter: `date` / `tags` / `highlights` / `logged_at`
- フォーマットの詳細は [`.claude/rules/journal.md`](../.claude/rules/journal.md) 参照。

> ⚠️ 個人の日記本文はこのテンプレートには含めていません（`.gitignore` で `journal/**/*.md` を除外）。自分で運用する際は private リポジトリを推奨します。
