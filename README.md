# claude-code-life

> Claude Code で「人生を1つのリポジトリ」として運用するための、AIネイティブな個人運用フレームワーク（テンプレート）。

日記・自己分析・プロジェクト管理・アイデアを、**人間ではなく AI が第一読者**となる構造で1つのリポジトリにまとめ、用途ごとの Claude Code スキル（エージェント）で運用します。

設計思想の全体像はこちら → [リポジトリは人間のために書かない — Claude Code で日記・投資・育児まで運用する【全体像】](https://zenn.dev/takotyan00/articles/claude-code-life-repository)

## コンセプト

- **第一読者は AI**: ドキュメントを人間の可読性ではなく、AI の検索・横断性のために設計する。1ファイル1事実、frontmatter にメタデータ、ファイル名は「あとで AI が探せるか」を最優先にする。
- **1つの土台に束ねる**: 別々のツールに散らさず、1リポジトリに集約して文脈を共有させる。作るほど基盤が強くなる。
- **多エージェント運用**: 用途ごとのスキルが同じ知識ベースを参照し、1つの出力が別の入力になる。

## 構成

```
.
├── CLAUDE.md                     # Claude Code への共有指示テンプレート
├── journal/                      # 対話式日記（年/月/日.md）
├── ideas/                        # アイデアストック
├── projects/                     # 各プロジェクトのメタ情報
├── persona/                      # 対話型ペルソナ（自己分析）
└── .claude/
    ├── config/context.example.yaml  # 全スキルが共有するコンテキストの雛形
    ├── rules/                    # エージェントに注入する振る舞いのルール
    └── skills/                   # 用途別エージェント（/journal, /weekly-review, /persona）
```

## 含まれるもの（このテンプレートの範囲）

- `CLAUDE.md` — Claude Code への共有指示テンプレート
- `.claude/skills/` — 対話式日記 / 週次レビュー / ペルソナ構築の3スキル（汎用版）
- `.claude/rules/` — 方法論ルール（mcp-vs-skills）＋対話の振る舞いルール（unknown-term-lookup）＋各種フォーマットの型
- `.claude/config/context.example.yaml` — 全スキルが共有するコンテキストの雛形
- `journal/` `ideas/` `projects/` `persona/` — 各ディレクトリの役割を README で説明

## 使い方

1. このリポジトリを clone（またはテンプレートとして利用）する。
2. `.claude/config/context.example.yaml` を同じ場所に `.claude/config/context.yaml` としてコピーし、自分の関心・プロジェクトを記入する。
3. Claude Code で `/journal` `/weekly-review` `/persona` を起動する。
4. 自分の運用に合わせて `CLAUDE.md`・`rules`・`skills` を調整する。

## まだ入っていないもの（順次「おろしていく」）

- **補正ルール**（AI に自分を正しく読ませる）— 個人の例を含むため、汎用化してから順次公開します。設計の考え方は上記の記事と続編で書きます。
- finance / 趣味推薦などドメイン別のスキル。
- `/trend`（トレンド収集）・`/improve`（環境改善）などの周辺スキル — 本テンプレには未収録です。`context.yaml` の `sources` / `improvement_backlog` は、それらを自分で足したとき用の足場として置いてあります。

## プライバシー

日記・自己分析・実名・資産額などの個人データは**このリポジトリには含めていません**。自分で運用する際は、機微情報を `*.local.md`（git 除外）に分離するか、リポジトリを private にしてください。

## ライセンス

[MIT](./LICENSE)
