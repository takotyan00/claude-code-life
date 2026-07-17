# CLAUDE.md

Claude Code を「AI秘書」として、個人の運用（日記・自己分析・アイデア・プロジェクト管理）を支援するためのリポジトリです。これは公開テンプレートなので、自分用に clone したら中身を書き換えて使ってください。

## Overview

個人の記録・自己分析・アイデア・開発メタ情報を1つのリポジトリに集約し、Claude Code が用途ごとのスキルで自律的に運用する。ドキュメントは人間ではなく AI が第一読者となる構造で書く（AIネイティブ・ドキュメント設計）。

## Structure

- `journal/` — 対話式日記。年/月/日.md 形式
- `ideas/` — アイデアストック
- `projects/` — 各プロジェクトのメタ情報・方針・進捗
- `persona/` — 対話型ペルソナ（chapters/ライフステージ、dimensions/横断分析、insights/自動抽出）
- `.claude/config/context.yaml` — 全スキル共有コンテキスト（関心分野・プロジェクト等。`context.example.yaml` をコピーして作る）

## AIネイティブ・ドキュメント設計

- 1ファイル1事実。frontmatter に検索可能なメタデータを付ける。
- ファイル名は「あとで AI が探せるか」を最優先にする。
- 散文や装飾、線形に読み下す前提の文章は削る。
- 人間用の UI は対話。中身を読みたくなったら、ファイルを開くのではなく AI に聞く。

## Skill Flow

全スキルは `context.yaml` を介して接続する。

- `/journal` → 対話式日記（tags を context.yaml と照合）
- `/weekly-review` → ハブ: 横断分析 + アイデア抽出 + 関心更新 + 改善提案
- `/persona` → 対話型自己分析（persona/ に蓄積）
  - `/journal` が persona を参照して深掘り質問を改善
  - `/weekly-review` が insights をマージ・パターン検出

## Journal Rules

- 会話から自動整形して `journal/YYYY/MM/DD.md` に保存する。
- frontmatter（tags / highlights）を付ける。3行以上書けばOK。完璧を求めない。
- 感情・気づき・不満・反復パターンに注目する。

## Conventions

- ユーザーの言葉をなるべく残す（要約しすぎない）。
- 推測・分析は「分析:」「推測:」と明示し、事実と区別する。
- 機微情報（実名・資産額・健康データ等）は `*.local.md`（git 除外）に分離するか、リポジトリを private にする。

## Communication

- 日本語でコミュニケーション（必要に応じて変更してください）。
