# persona/ — 対話型ペルソナ（自己分析）

`/persona` スキルが対話を通じて構築し、`/journal` と `/weekly-review` が参照する。

- `chapters/` — ライフステージ別（childhood / adolescence / early-career / growth / current）
- `dimensions/` — 横断テーマ（values / thinking-patterns / emotions / motivations / relationships）
- `insights/` — 日々の気づきの自動抽出（`YYYY-MM-DD.md`）
- `profile.yaml` — 進捗管理（not_started → in_progress → draft → reviewed）

記録ルールは [`.claude/rules/persona.md`](../.claude/rules/persona.md) 参照。

> ⚠️ 自己分析の本文はこのテンプレートには含めていません（`.gitignore` で除外）。最も機微度が高い領域なので、自分で運用する際は private リポジトリを強く推奨します。実名など第三者の個人情報は `*.local.md`（git 除外）に分離してください。
