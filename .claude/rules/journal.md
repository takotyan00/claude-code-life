## 日記フォーマット

- ファイルパス: `journal/YYYY/MM/DD.md`
- frontmatter 必須: `tags`、`highlights`、`logged_at`

```yaml
---
date: 2026-03-12
logged_at: 2026-03-12T21:30   # /journal 起動時刻。次回の対象日ウィンドウ判定に使う
tags: [開発, アイデア]
highlights:
  - 新しいプロジェクトを構想した
---
```

## 記録ルール

- 会話から自動整形する際、ユーザーの言葉をなるべく残す（要約しすぎない）。
- 繰り返し出現するテーマにはタグを付与する（`context.yaml` の interests と照合）。
- 感情・気づき・不満・反復パターンに注目する。
- 3行以上書けばOK。完璧を求めない。
