# .claude/rules/ — エージェントに注入する振る舞いのルール

スキルから参照される「振る舞いの規約」を置く。各スキルは必要なルールを読み込んでから動く。

## 含まれるルール

- [`mcp-vs-skills.md`](./mcp-vs-skills.md) — 新機能を Skill で作るか MCP で作るかの判別フロー
- [`journal.md`](./journal.md) — 日記のフォーマットと記録ルール
- [`ideas.md`](./ideas.md) — アイデアのディレクトリ構成とフォーマット
- [`projects.md`](./projects.md) — プロジェクトメタ情報のフォーマット
- [`persona.md`](./persona.md) — ペルソナデータの記録ルール
- [`unknown-term-lookup.md`](./unknown-term-lookup.md) — 不明な固有名詞を対話を止めずに裏取りする
- [`correction-rules/`](./correction-rules/README.md) — **補正ルール（AI に自分を「正しく」読ませる）**。書き方の型（5部構成）＋汎用の記入例1本。中身は一人ひとり固有なので雛形は配らず、自分の対話でズレを採取して育てる前提

## 補正ルールについて（差別化の核）

`correction-rules/` は、このフレームワークの差別化の核です。「AI は放っておくと人間を都合よく平板に要約する。それを自分の癖に合わせて先回りで直す」という設計で、`/journal`・`/persona`・`/weekly-review` が分析の前に読みます。性質上ひとりひとり中身が違うため、ここに置くのは**型と考え方、汎用の記入例まで**。設計の全文は記事 [Claude Code に「補正ルール」を渡す](https://zenn.dev/takotyan00/articles/claude-code-correction-rules) にあります。
