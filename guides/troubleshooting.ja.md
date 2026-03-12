# SpecKit for Projects トラブルシュート

この文書は、`SpecKit for Projects` 利用時によく出る warning / failure と、再生成運用で起きやすい問題の対処をまとめたものです。

## 1. `sdd check` で warning が出る

典型的には、対象 agent の CLI ランタイム不足です。

例:

- `codex` コマンドがない
- `claude` コマンドがない
- `gemini` コマンドがない

対処:

1. agent CLI をインストールする
2. PATH に乗っているか確認する
3. その後に `sdd check --ai <agent>` を再実行する

補足:

- warning は scaffold 欠落ではないため、文書自体は読めることがあります
- ただし agent 実行時に詰まりやすいので、先に解消した方がよいです

## 2. `sdd check` で failure が出る

failure は欠落や設定不整合です。warning より優先して解消します。

典型例:

- `.specify/project/domain-map.md` がない
- `.specify/templates/commands/tasks.md` がない
- `designs/common_design/module/` がない
- agent 用 `sdd.design.md` が出力先にない

対処の基本:

```bash
sdd init --here --ai codex --ai-skills
sdd check --ai codex
```

既存管理ファイルをテンプレートから戻したいなら:

```bash
sdd init --here --ai codex --ai-skills --force
```

## 3. `generic` で command が見つからない

`generic` は出力先を自動決定しません。

ありがちな原因:

- `init` で `--ai-commands-dir .myagent/commands` を使ったのに、`check` では省略した
- 別パスを指定してしまった

対処:

```bash
sdd init --here --ai generic --ai-commands-dir .myagent/commands
sdd check --ai generic --ai-commands-dir .myagent/commands
```

`init` と `check` で同じパスを使ってください。

## 4. Codex で `/sdd.brief` が使えない

仕様です。Codex は `.codex/prompts/*.md` を custom slash command としては登録しません。

対処:

- `.codex/prompts/sdd.brief.md` などを保存済み prompt として使う
- `sdd init --ai codex --ai-skills` で `speckit-for-projects-*` skill も入れる
- セッションを開き直して skill 認識を更新する

## 5. `--ai-skills` がエラーになる

原因はほぼ次のどちらかです。

- `--ai` を付けていない
- `generic` 用の `--ai-commands-dir` が足りない

正しい例:

```bash
sdd init --here --ai codex --ai-skills
```

## 6. 再生成で手修正が消える

これは `SpecKit for Projects` の運用で最も起きやすい事故です。

原因:

- `specific_design` の managed artifact に正本ルールを書いていた
- `--force` でテンプレート再配置した
- AI に full overwrite 前提の command を再実行した

対処:

- 共通ルールなら `.specify/project/` へ戻す
- 共有契約なら `designs/common_design/` へ戻す
- 要求の話なら `briefs/` へ戻す
- feature 設計だけなら再生成前に diff で吸い上げ先を決める

## 7. `design` 生成後に `traceability.yaml` が弱い

よくある症状:

- 一部 `REQ-*` がない
- `common_design_refs` が brief と一致しない
- `related_artifacts` が薄すぎる

対処観点:

- brief の `Requirements` を先に見直す
- brief の `Common Design References` が `none` のままになっていないか確認する
- `designs/common_design/` 側の `CD-*` が実在するか確認する

## 8. `tasks.md` の粒度が粗すぎる / 細かすぎる

粗すぎる例:

- 1 task で UI、API 連携、テスト、運用導線まで全部抱える

細かすぎる例:

- HTML 変更だけで 1 task
- 文言修正だけで 1 task

見直し基準:

- requirement と設計成果物を根拠に、レビュー可能な単位で切る
- `depends_on` が自然に表現できるかを見る
- 実装担当が 1 回の集中作業で終えられるかを見る

## 9. `implement` が対象外まで変更してしまう

原因:

- 対象 `TASK-xxx` を明示していない
- tasks 参照なしで実装を始めた
- task とコード配置の対応が曖昧

対処:

- `design-id` と `TASK-xxx` を必ず入力で明示する
- 実装前に `tasks.md` の対象 section を読む
- 変更後に `git diff` と `Changed Files` を照合する

## 10. Storybook が起動しない

まず `ui-storybook/` 配下で次を確認します。

```bash
cd designs/specific_design/<design-id>/ui-storybook
npm install
npm run build-storybook
```

確認点:

- Node / npm が入っているか
- `package.json` が生成されているか
- `.storybook/main.ts` など必須ファイルがあるか
- story と component が最低 1 組あるか

## 11. どこへ戻すべきか迷う

判断基準:

- プロジェクト全体のルール -> `.specify/project/`
- 共有 API / Data / Module / UI -> `designs/common_design/`
- feature 要求 -> `briefs/`
- feature 固有設計 -> `designs/specific_design/`
- 実装証跡 -> `tasks.md` execution ledger

## 12. 復旧の最小セット

状態が壊れたときは、まず次の順で戻すのが現実的です。

1. `git status` と `git diff` を確認する
2. `sdd check` で欠落を特定する
3. `sdd init --here [--ai ...]` で不足 scaffold を戻す
4. 必要なら `--force` で managed file を戻す
5. brief / common_design / specific_design の順で正本を見直す

## 13. 関連ドキュメント

- [guides/manual.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/manual.ja.md)
- [guides/cli-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/cli-reference.ja.md)
- [guides/workflow-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/workflow-reference.ja.md)
