# SpecKit for Projects 実装タスクプラン v1

- 文書状態: Draft
- 作成日: 2026-03-11
- 参照元:
  - `docs/basic-design.md`
  - `docs/implementation-plan.md`
  - `docs/upstream-spec-kit-map.md`

## 1. 目的

この文書は、`SpecKit for Projects` v1 の実装を実行順に落としたタスクプランである。`implementation-plan.md` の各 Phase を、そのまま着手可能な粒度のタスクへ分解する。

## 2. 実行順サマリ

1. `spec-kit` 流用調査とベース移植
2. Python パッケージと品質基盤の初期化
3. ドメインモデルと I/O 基盤の実装
4. `sdd init` と `sdd check` の実装
5. AI command templates の実装
6. 設計成果物テンプレートの実装
7. 再生成運用とドキュメント整備
8. 検証、golden test、README 整備
9. `@storybook/html` 実行基盤の整備

## 3. フェーズ別タスク

### Phase 0: `spec-kit` 流用調査とベース移植

- [x] T001 `spec-kit` の参照コミット `56095f06d2b4b6f29b92dc3f4421da59f66a840b` を基準に流用対象を確定する
- [x] T002 `docs/upstream-spec-kit-map.md` の流用対象一覧とローカル配置先を最終レビューする
- [x] T003 `spec-kit` の CLI 骨格、command 配布、初期化処理、テスト基盤の流用候補を洗い出す
- [x] T004 `src/speckit_for_projects/foundations/` に取り込む共通基盤の責務境界を確定する
- [x] T005 upstream 由来コードで保持すべき MIT attribution の反映方針を README 側タスクへ接続する

完了条件:

- [x] C001 流用対象と差し替え対象が `docs/upstream-spec-kit-map.md` と一致している
- [x] C002 upstream へのランタイム依存を持たない方針が実装前提として確定している

### Phase 1: リポジトリ整備と品質基盤

- [x] T101 `pyproject.toml` を追加し、`SpecKit for Projects` の package 名、entrypoint、依存を定義する
- [x] T102 `src/speckit_for_projects/`、`tests/unit/`、`tests/integration/`、`tests/golden/` を作成する
- [x] T103 `ruff`、`mypy`、`pytest` の設定を追加する
- [x] T104 CLI entrypoint の空実装を追加する
- [x] T105 README に最小の導入手順セクションを追加する

完了条件:

- [x] C101 `uv run pytest` が通る
- [x] C102 `uv run ruff check .` が通る
- [x] C103 `uv run mypy src` が通る

### Phase 2: ドメインモデルと I/O 基盤

- [x] T201 `ProjectStandards`、`Brief`、`Requirement`、`DesignBundle`、`TraceabilityEntry`、`TaskItem` を Pydantic で定義する
- [x] T202 `brief-id` と `design-id` の `001-kebab-slug` 採番ロジックを実装する
- [x] T203 Markdown / YAML 読み書きユーティリティを実装する
- [x] T204 例外モデルと validation ルールを定義する
- [x] T205 AI command templates が参照する共通コンテキスト組み立てルールを定義する

完了条件:

- [x] C201 `Brief` と `TraceabilityEntry` の serialize / deserialize テストが通る
- [x] C202 ID 採番規則が unit test で固定される

### Phase 3: `sdd init` と `sdd check`

- [x] T301 `sdd init` コマンドを追加する
- [x] T302 `sdd check` コマンドを追加する
- [x] T303 `.specify/project/` 配下の共通統制文書を初期配置するロジックを実装する
- [x] T304 `.specify/templates/commands/` と agent-specific command files の配布ロジックを実装する
- [x] T305 `--ai`, `--ai-commands-dir`, `--here`, `--force`, `--no-git`, `--debug` を CLI 引数へ反映する
- [x] T306 `sdd check` で AI ツール存在確認、テンプレート欠落確認、共通統制文書欠落確認を実装する

完了条件:

- [x] C301 `sdd init --ai codex` で必要ファイルが生成される
- [x] C302 `sdd init --ai generic --ai-commands-dir <path>` が指定先へ出力する
- [x] C303 `sdd check` が未導入エージェントと欠落テンプレートを検出する
- [x] C304 `sdd init` 再実行で破壊的変更が起きない

### Phase 4: AI command templates 実装

- [x] T401 `/sdd.brief` template を実装する
- [x] T402 `/sdd.design` template を実装する
- [x] T403 `/sdd.tasks` template を実装する
- [x] T404 `/sdd.implement` template を実装する
- [x] T405 agent ごとの差し替えテンプレートまたはラッパを実装する
- [x] T406 command templates に `001-kebab-slug` 命名規約を埋め込む
- [x] T407 `brief/design` は full-file overwrite、`tasks.md` は ledger 保持再生成という運用を command templates に埋め込む

完了条件:

- [x] C401 Codex 系 command templates が配置・参照できる
- [x] C402 非 Codex 系で少なくとも 1 系統の command templates が配置・参照できる
- [x] C403 配布テンプレートが golden test と一致する

### Phase 5: 設計成果物テンプレート実装

- [x] T501 `briefs/<brief-id>.md` template を実装する
- [x] T502 `.specify/project/tech-stack.md` template を実装する
- [x] T503 `.specify/project/coding-rules.md` template を実装する
- [x] T504 `.specify/project/architecture-principles.md` template を実装する
- [x] T505 `overview.md` template を実装する
- [x] T506 `ui-storybook/` template を実装する
- [x] T507 `ui-fields.yaml` template を実装する
- [x] T508 `@storybook/html` 用 stories / HTML template を実装する
- [x] T509 `api-design.md` template を実装する
- [x] T510 `data-design.md` template を実装する
- [x] T511 `batch-design.md` template を実装する
- [x] T512 `module-design.md` template を実装する
- [x] T513 `sequence-flows/*.md` template を実装する
- [x] T514 `test-design.md` template を実装する
- [x] T515 `test-plan.md` template を実装する
- [x] T516 `traceability.yaml` template と初期割当ルールを実装する
- [x] T517 `tasks.md` template を実装する
- [x] T518 必須成果物の存在確認と要件未割当検知を実装する

完了条件:

- [x] C501 `/sdd.design` 実行前提で `designs/<design-id>/` 配下に必須成果物が揃う
- [x] C502 `traceability.yaml` に全要件が掲載される
- [x] C503 画面中心、API 中心、バッチ中心の 3 ケースで生成結果が成立する

### Phase 6: 再生成運用と差分確認前提の整備

- [x] T601 `brief/design` の full-file overwrite と `tasks.md` の ledger 保持再生成を README に反映する
- [x] T602 `git diff` による差分確認手順を command templates に反映する
- [x] T603 managed blocks / in-place merge を v1 非対応として文書化する
- [x] T604 `design-id` 再生成時の同一パス上書き前提を利用者向け文書へ反映する

完了条件:

- [x] C601 再生成運用が README と command templates の両方に明記される
- [x] C602 差分確認手順が利用者から追える

### Phase 7: 検証と整備

- [x] T701 画面中心案件サンプルを追加する
- [x] T702 API 中心案件サンプルを追加する
- [x] T703 バッチ中心案件サンプルを追加する
- [x] T704 `sdd init --ai codex` の integration test を追加する
- [x] T705 `sdd init --ai generic --ai-commands-dir <path>` の integration test を追加する
- [x] T706 `sdd check` の integration test を追加する
- [x] T707 command templates 配布の golden test を追加する
- [x] T708 生成成果物の golden test を追加する
- [x] T709 README の手順を end-to-end で追える内容へ拡充する
- [x] T710 upstream 由来コードの attribution を README または関連文書へ反映する

完了条件:

- [x] C701 サンプル 3 ケースで `init -> AI commands -> generated outputs` の流れが確認できる
- [x] C702 README だけで初回利用者が再現できる
- [x] C703 `docs/upstream-spec-kit-map.md` と実コード配置が一致する

### Phase 8: `@storybook/html` 実行基盤の整備

- [x] T801 `ui-storybook/` 配下に `package.json` template を追加し、`storybook` / `build-storybook` scripts を定義する
- [x] T802 `ui-storybook/.storybook/preview` 系 template を追加し、design token / global styles / parameters の注入ポイントを用意する
- [x] T803 `ui-storybook/README.md` template を拡張し、`npm install` / `npm run storybook` / `npm run build-storybook` の手順を明記する
- [x] T804 `/sdd.design` command template を更新し、`@storybook/html` bundle を「起動確認可能な成果物」として生成指示する
- [x] T805 examples 3 ケースに Storybook 実行用 `package.json` と preview 設定を追加する
- [x] T806 `validate_design_bundle` に Storybook 実行基盤ファイルの存在確認を追加する
- [x] T807 generated artifact の golden test を Storybook 実行基盤込みで更新する
- [x] T808 CLI または subprocess ベースの E2E で `npm run build-storybook` 相当の疎通確認を追加する
- [x] T809 README / README.ja.md に「design bundle をローカル起動してレビューする手順」を追加する
- [x] T810 パッケージ生成物の更新手順を整理し、`src/speckit_for_projects.egg-info/` の stale metadata を再生成または非管理方針に統一する

完了条件:

- [x] C801 `designs/<design-id>/ui-storybook/` が追加セットアップなしで `@storybook/html` を起動できる
- [x] C802 examples 3 ケースすべてで Storybook build が成功する
- [x] C803 README の手順だけで UI レビュー用 Storybook を起動できる

## 4. 並行実行の目安

### 先行必須

- Phase 0 は全後続の前提
- Phase 1 は全後続の前提
- Phase 2 は Phase 3 以降の前提

### 並行化できる領域

- Phase 4 の command templates 3本は並行可能
- Phase 5 の成果物テンプレートは依存の薄いものから並行可能
  - `overview.md`
  - `ui-storybook/`
  - `api-design.md`
  - `data-design.md`
  - `batch-design.md`
  - `module-design.md`
  - `test-design.md`
  - `test-plan.md`
- Phase 7 のサンプル案件 3本は並行可能
- Phase 8 の Storybook 実行基盤整備は次を並行可能
  - `package.json` / `.storybook/preview`
  - examples 更新
  - README 更新
  - build E2E 追加

## 5. レビュー観点

- `spec-kit` の流用コードが `foundations/` に隔離されているか
- CLI 本体が `init/check` に限定され、LLM 実行主体を持ち込んでいないか
- `/sdd.brief`、`/sdd.design`、`/sdd.tasks`、`/sdd.implement` の command templates が `SpecKit for Projects` 用に置換されているか
- `brief-id` と `design-id` が `001-kebab-slug` 形式で一貫しているか
- `brief/design` の full-file overwrite と `tasks.md` ledger 保持方針が README と templates の双方に書かれているか
- 共通統制文書、設計成果物、UI、シーケンス、テスト、トレーサビリティがすべて揃うか
- `ui-storybook/` が単なる文書ではなく、`@storybook/html` として実行可能な bundle になっているか
