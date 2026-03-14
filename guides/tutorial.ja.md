# SpecKit for Projects チュートリアル

この文書は、`SpecKit for Projects` を初めて使う人向けの日本語チュートリアルです。空のリポジトリに `SpecKit for Projects` を導入し、`brief -> clarify -> design -> tasks -> analyze -> implement` を 1 回通すところまでを扱います。

## このチュートリアルで作るもの

題材は次の小さな案件です。

- バックオフィス担当者が申請を検索できるレビュー画面
- 検索結果から詳細画面へ遷移できる
- 既存の顧客 API は再利用する

最終的に、次の成果物が揃う状態を目指します。

- `.specify/` の共通標準とテンプレート
- `briefs/001-...md`
- `designs/common_design/` の共有設計
- `designs/specific_design/001-.../` の設計束
- `designs/specific_design/001-.../tasks.md`

## 事前準備

必要条件は次のとおりです。

- Python 3.12 以上
- `uv`
- 使いたい AI エージェント

このリポジトリ自身を触る場合は、まず開発依存を入れます。

```bash
uv sync --dev
uv run sdd --help
```

普段使いではツールインストールでも構いません。

```bash
uv tool install -e .
sdd --help
```

## 1. 作業用リポジトリを用意する

新しいディレクトリを作る場合:

```bash
mkdir portal-demo
cd portal-demo
```

現在のディレクトリをそのまま使う場合は、以降の `init` に `--here` を付けます。

## 2. `sdd init` で初期化する

Codex を使う例:

```bash
sdd init --here --ai codex --ai-skills
```

Claude を使う例:

```bash
sdd init --here --ai claude --ai-skills
```

汎用エージェントへ自分で出力先を決める例:

```bash
sdd init --here --ai generic --ai-commands-dir .myagent/commands
```

このコマンドで主に次が生成されます。

- `.specify/project/` の共通標準
- `.specify/templates/commands/` の AI ワークフローテンプレート
- `.specify/templates/artifacts/` の成果物雛形
- エージェント別の prompt / command ファイル
- `briefs/`
- `designs/`

Codex では `.codex/prompts/*.md` は slash command にはなりません。`--ai-skills` を付けておくと、Codex から見つけやすい `speckit-for-projects-analyze`、`speckit-for-projects-brief`、`speckit-for-projects-clarify` などの skill も併せて入ります。

## 3. `sdd check` で導入状態を確認する

```bash
sdd check --ai codex
```

想定どおりなら、共有 scaffold とエージェント設定が有効だと表示されます。`warning` は実行時ランタイム不足、`failure` は必須ファイル欠落です。

`generic` を使った場合は出力先も渡します。

```bash
sdd check --ai generic --ai-commands-dir .myagent/commands
```

## 4. 共通標準を最小限だけ埋める

AI に文書生成を依頼する前に、最低でも次のファイルを案件向けに編集します。

- `.specify/project/tech-stack.md`
- `.specify/project/coding-rules.md`
- `.specify/project/architecture-principles.md`
- `.specify/project/domain-map.md`
- `.specify/glossary.md`

迷った場合は、[examples/project-standards/todo-app-ja/README.md](/Users/iwasakishinya/Documents/hook/general_sdd/examples/project-standards/todo-app-ja/README.md) を参考にしてください。

複数 feature で共有する画面一覧や標準遷移を先に固めたい案件なら、`designs/common_design/ui/` も整備対象です。

ここで重要なのは、project 層と feature 層を混ぜないことです。プロジェクト全体ルールは `.specify/project/`、共有設計は `designs/common_design/`、feature 固有設計は後続の `designs/specific_design/` に分けます。

補足として、リポジトリには `src/speckit_for_projects/templates/project/design-system.md.j2` と `src/speckit_for_projects/templates/project/ui-storybook/` もあります。これらは `sdd init --project-design-system` を付けたときだけ配置されます。`shadcn/ui` のような外部デザインシステム採用案件では不要になりうるため、このチュートリアルでも必須前提にはしていません。

## 5. AI で `brief` を作る

ここから先は CLI ではなく、AI エージェント側のワークフローです。Codex なら `speckit-for-projects-brief` skill を使うか、`.codex/prompts/sdd.brief.md` を開いて使います。

入力例:

```text
バックオフィス担当者向けの申請レビュー画面を作りたい。
検索条件は申請者名とステータス。
一覧から詳細画面へ遷移したい。
既存の顧客 API を再利用する。
支払い処理は対象外。
```

期待する出力は `briefs/001-screened-application-portal.md` のようなファイルです。最低限、次が含まれていることを確認してください。

- 背景と目的
- Scope In / Scope Out
- 利用者や外部連携先
- 制約
- `REQ-001` 形式の要件

参考例は [examples/screen-centric/briefs/001-screened-application-portal.md](/Users/iwasakishinya/Documents/hook/general_sdd/examples/screen-centric/briefs/001-screened-application-portal.md) です。

## 6. AI で `clarify` を使って曖昧さを詰める

`brief` が作れたら、すぐに `design` へ進めるとは限りません。要件が曖昧、`CD-*` が不足、domain 境界が怪しい、という場合は `sdd.clarify` 相当のワークフローを先に使います。

Codex なら `speckit-for-projects-clarify` skill を使うか、`.codex/prompts/sdd.clarify.md` を開きます。

この段階で見たいポイント:

- `Domain Alignment` が `.specify/project/domain-map.md` と矛盾していないか
- `Common Design References` が不足または過剰になっていないか
- `REQ-*` が testable な文になっているか
- `design` に進む前に答えるべき blocking question がないか

`clarify` は read-only です。直接 `brief` を上書きするのではなく、返ってきた質問と tightening 提案を見て `brief` や shared design の正本側を直します。

## 7. AI で `design` を作る

次に `brief-id` を指定して `sdd.design` 相当のワークフローを実行します。入力では「対象 brief は `001-screened-application-portal`」のように明示すると安定します。

この段階では、brief の `Common Design References` にある `CD-*` を実在する共有設計へ解決できる状態にしておく必要があります。共有契約がまだないなら、先に `sdd.common-design` 相当のワークフローで `designs/common_design/` を整備してください。

期待される主な出力:

- `designs/common_design/`
- `designs/specific_design/<design-id>/overview.md`
- `designs/common_design/ui/CD-UI-001-screen-catalog.md`
- `designs/common_design/ui/CD-UI-002-navigation-rules.md`
- `designs/specific_design/<design-id>/ui-storybook/`
- `designs/specific_design/<design-id>/ui-fields.yaml`
- `designs/specific_design/<design-id>/common-design-refs.yaml`
- `designs/specific_design/<design-id>/sequence-flows/core-flow.md`
- `designs/specific_design/<design-id>/batch-design.md`
- `designs/specific_design/<design-id>/test-design.md`
- `designs/specific_design/<design-id>/test-plan.md`
- `designs/specific_design/<design-id>/traceability.yaml`

まずは `overview.md` と `traceability.yaml` を確認します。

- brief の要件が抜けていないか
- 非対象範囲が紛れ込んでいないか
- 主要フローが説明できる形になっているか
- brief に書いた `CD-*` が `common-design-refs.yaml` に反映されているか

参考例:

- [examples/screen-centric/designs/specific_design/001-screened-application-portal/overview.md](/Users/iwasakishinya/Documents/hook/general_sdd/examples/screen-centric/designs/specific_design/001-screened-application-portal/overview.md)

UI 成果物をブラウザで見たい場合は、生成された Storybook を起動します。

```bash
cd designs/specific_design/<design-id>/ui-storybook
npm install
npm run storybook
```

成果物を配布前に固めて確認したい場合:

```bash
npm run build-storybook
```

## 8. AI で `tasks.md` を作る

次に `design-id` を指定して `sdd.tasks` 相当のワークフローを実行します。

期待する状態:

- `TASK-001` 形式で実装項目が並ぶ
- 各 task に `requirement_ids` がある
- `artifact_refs` に参照元設計書がある
- 共有設計に依存する task には `common_design_refs` がある
- `Execution Status` や `Verification Results` の実行台帳欄がある

参考例:

- [examples/screen-centric/designs/specific_design/001-screened-application-portal/tasks.md](/Users/iwasakishinya/Documents/hook/general_sdd/examples/screen-centric/designs/specific_design/001-screened-application-portal/tasks.md)

この段階では、task の粒度と依存順序を人間が確認してください。設計レビュー前に task を確定させすぎると、後で差し戻しが大きくなります。

## 9. `sdd analyze` で bundle 整合を確認する

`sdd.clarify` が設計前の曖昧さ整理なのに対し、`sdd analyze` は scaffold ではなく生成済み成果物 bundle 自体を確認します。

```bash
sdd analyze 001-screened-application-portal
```

複数 bundle をまとめて確認したい場合:

```bash
sdd analyze --all
```

ここで確認したいポイント:

- `traceability.yaml` に brief の `REQ-*` 漏れがないか
- `tasks.md` が要件をカバーしているか
- `common-design-refs.yaml` の `CD-*` が実在 shared design を指しているか
- bundle 内の必須ファイルが欠けていないか

`failure` が出たら、まず `traceability.yaml`、`common-design-refs.yaml`、`tasks.md` を見直してから次へ進みます。

## 10. AI で一部タスクを実装する

最後に `design-id` と `TASK-xxx` を指定して `sdd.implement` 相当のワークフローを実行します。

例:

```text
design-id は 001-screened-application-portal。
TASK-001 を実装して。
変更したファイル、実行した検証コマンド、結果要約を tasks.md に反映して。
```

期待する状態:

- コード差分ができる
- テストまたは検証コマンドが実行される
- `designs/specific_design/<design-id>/tasks.md` の対象 task だけが更新される

## 11. 再生成時の見方

`SpecKit for Projects` は再生成を前提にしています。文書を更新したあとに見るべきポイントは次のとおりです。

- `git diff` で brief / design / tasks の差分を確認する
- `sdd analyze` の結果で category ごとの issue を確認する
- `traceability.yaml` から要件漏れが出ていないか見る
- `tasks.md` の task 定義と実行台帳が不自然に壊れていないか見る

特に `design` は上書き再生成が前提です。人手で微修正した内容を残したい場合は、先に共通標準か brief 側へ正本として戻してください。

## 12. 次に読む文書

通しで 1 回動かせたら、次は分割ガイドを読むと運用しやすくなります。

- [guides/manual.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/manual.ja.md)
- [guides/cli-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/cli-reference.ja.md)
- [guides/workflow-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/workflow-reference.ja.md)
- [guides/artifact-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/artifact-reference.ja.md)
- [guides/troubleshooting.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/troubleshooting.ja.md)
