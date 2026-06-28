## プロジェクトファイルフォーマット

各プロジェクトファイル（`projects/{name}.md`）に以下を記載する:

```markdown
# {Project Name}

## 目的
何を解決するプロジェクトか

## 技術スタック
使用している技術

## リポジトリ
GitHub URL（あれば）

## ステータス
active / paused / planning / completed

## 現在の進捗
直近の状態

## 次のマイルストーン
次にやるべきこと
```

## ルール

- ステータス更新は開発進捗に応じて反映する。
- マイルストーン達成時は次のマイルストーンを設定する。
- 開発状況（development_status）と利用状況（user_facing）は別軸で扱い、混同しない。
