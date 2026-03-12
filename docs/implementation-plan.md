# SpecKit for Projects 実装計画 v1

- 文書状態: Draft
- 作成日: 2026-03-11
- 参照元: `docs/basic-design.md`
- 対象: `SpecKit for Projects` OSS コア開発者

## 1. 実装方針サマリ

`SpecKit for Projects` v1 は、SI 設計リーダー向けの CLI OSS として実装する。CLI 本体の正式コマンドは `sdd init` と `sdd check` に絞り、`brief/design/tasks/implement` は AI エージェント向け command template として配布する。成果物の正本は Markdown / YAML / HTML とする。

v1 の中心価値は、案件または機能単位の入力から、共通統制文書、設計書束、UI 成果物束、シーケンス成果物束、テスト成果物束、トレーサビリティ、タスクまでを一貫生成できることに置く。差分更新や高度な AI 生成品質最適化よりも、まずは成果物の構造、追跡性、再現性を優先する。

実装戦略は greenfield ではなく、`github/spec-kit` の実装基盤を土台にした派生実装とする。CLI 骨格、テンプレート展開、プロジェクト初期化、ファイル生成、テスト基盤などは `spec-kit` から最大限流用し、`brief / design bundle / traceability / UI / sequence / test artifacts` に関わるドメイン層は `SpecKit for Projects` 用に再設計する。

### 1.1 流用方針

流用対象は次の 2 層に分ける。

- そのまま、または軽微な名前変更で流用する層
  - CLI アプリケーション骨格
  - コマンド登録方式
  - プロジェクト初期化フロー
  - テンプレート配置とレンダリングの仕組み
  - ファイル生成/更新ユーティリティ
  - テスト実行基盤、fixture 構成、golden test の枠組み
  - agent-specific command files の配布構造
- `SpecKit for Projects` 用に再設計する層
  - `/sdd.brief` `/sdd.design` `/sdd.tasks` `/sdd.implement` のドメイン意味
  - `spec -> plan -> tasks` 前提の内部モデル
  - 成果物の種類と生成順序
  - `traceability.yaml` の構造
  - UI モック、シーケンス図、テスト成果物の生成ロジック
  - 共通統制文書の扱い

### 1.2 取り込み方式

v1 は `spec-kit` のコードを参照しながら、必要な実装をこのリポジトリへ選択的に持ち込む。サブモジュールやランタイム依存として接続するのではなく、 `SpecKit for Projects` のコードベース内に必要部分を取り込んだうえで、ドメイン層を置き換える。

理由は以下の通りである。

- v1 の成果物モデルは `spec-kit` と互換ではなく、直接依存するとドメイン変更の自由度が落ちる。
- ランタイム時に `spec-kit` の内部構造へ依存すると、上流変更の影響を強く受ける。
- 生成物の設計が大きく異なるため、内部実装の再利用と公開仕様の独立を両立するには、選択的取り込みが最も現実的である。
- v1 は CLI 内蔵 LLM を持たず、AI エージェント側 command template 実行へ寄せるほうが `spec-kit` の配布モデルと整合する。

## 2. 技術選定

### 2.1 採用スタック

v1 の実装スタックは以下で固定する。

| 項目 | 採用 |
| --- | --- |
| 言語 | Python 3.12 |
| パッケージ管理 | `uv` |
| CLI フレームワーク | `Typer` |
| 設定/データモデル | `Pydantic v2` |
| YAML 処理 | `ruamel.yaml` |
| テンプレート | `Jinja2` |
| テスト | `pytest` |
| スナップショット/ゴールデン | `pytest` + fixture 比較 |
| 品質ツール | `ruff`, `mypy` |

### 2.2 採用理由

- Python は CLI とファイル生成系 OSS の実装速度が高く、 `spec-kit` の実装基盤を流用しやすい。
- Typer は CLI 仕様を簡潔に定義でき、ヘルプや引数整理がしやすい。
- Pydantic を使うことで、 `brief`、 `traceability.yaml`、共通統制文書の内部モデルを型付きで扱える。
- Jinja2 によって Markdown / HTML / YAML のテンプレートを同じ仕組みで生成できる。
- YAML は項目定義やトレーサビリティで機械可読性が必要なため、コメントや順序保持に強い `ruamel.yaml` を使う。

### 2.3 非採用

- Node.js ベース実装: HTML モック生成との相性は良いが、CLI 本体と構造化データ処理の一貫性で Python を優先する。
- Click 直利用: Typer のほうが v1 の CLI 仕様定義と保守性に向く。
- JSON 正本: 人間のレビューと編集性を優先し、YAML / Markdown を正本とする。

## 3. 実装対象と公開インタフェース

### 3.1 CLI コマンド

v1 で Python CLI として実装するのは以下の 2 コマンドとする。

#### `sdd init`

- 目的: プロジェクト初期化
- 主要動作:
  - `.specify/` 配下の共通統制文書、テンプレート、用語集、規約ディレクトリを作成する
  - `--ai <agent>` に応じた agent-specific command files を配置する
  - `briefs/` と `designs/` の親ディレクトリを作成する
- 成功条件:
  - 再実行しても破壊的にならない
  - 必須テンプレートがすべて配置される
  - `generic` 指定時は `--ai-commands-dir` へ出力できる

#### `sdd check`

- 目的: 利用前提となる AI 実行環境とテンプレート配置の検査
- 主要動作:
  - AI ツールの存在確認
  - `.specify/project/` と `.specify/templates/commands/` の欠落確認
  - 対象 AI 向け command files の整合確認
- 成功条件:
  - 成功/警告/失敗を区別して返す
  - 修復が必要な項目を列挙できる

### 3.2 AI エージェント向けコマンド

v1 では以下を agent-specific command files として配布する。

#### `/sdd.brief`

- 目的: 設計起点の生成
- 主要動作:
  - 案件/機能入力を受け取り `briefs/<brief-id>.md` を生成する
  - 要件 ID を採番する
  - 共通統制文書の参照欄を埋める
- v1 入力方式:
  - AI エージェントへの自然言語入力を受ける
  - 出力先は `briefs/<brief-id>.md`
  - `brief-id` は `001-kebab-slug` 形式の repo-local 連番とする

#### `/sdd.design`

- 目的: 設計束の生成/更新
- 主要動作:
  - `brief` と `.specify/project/` と `designs/common_design/` を読み込む
  - `designs/specific_design/<design-id>/` を生成または上書き更新する
  - specific design の必須成果物をすべて出力する
  - `traceability.yaml` を生成する
  - 必須成果物の存在と要件割当を検証する
  - 再生成後の差分確認は `git diff` を前提とする

#### `/sdd.common-design`

- 目的: 共有設計の生成/更新
- 主要動作:
  - `.specify/project/` と関連 brief を読み込む
  - `designs/common_design/api|data|module|ui/` に正本を生成する
  - 共有責務境界かどうかを確認し、 util や helper を排除する

#### `/sdd.tasks`

- 目的: 設計束からタスクを生成する
- 主要動作:
  - 設計束、シーケンス図、テスト成果物、共通統制文書を読み込む
  - `tasks.md` を生成または再生成する
  - 要件 ID と参照設計書を各タスクに付与する
  - `TASK-xxx` ごとに mutable execution ledger section を配置する
  - 再生成時は同じ `TASK-xxx` の execution ledger を保持する

#### `/sdd.implement`

- 目的: 選択 task の実装を実行し、`tasks.md` に結果を反映する
- 主要動作:
  - `design-id` と 1 個以上の `TASK-xxx` を解決する
  - 対象 task に必要な既存コード、テスト、build 設定を探索する
  - 選択 task に限定してコード変更とローカル検証を行う
  - `tasks.md` の execution ledger section のみ更新する
  - 実装基盤不足時は不足内容を列挙して停止する

### 3.3 初期 AI 対応セット

`sdd init --ai <agent>` の初期対応セットは `spec-kit` の現行サポート一覧に合わせる。

- `claude`
- `gemini`
- `copilot`
- `cursor-agent`
- `qwen`
- `opencode`
- `codex`
- `windsurf`
- `kilocode`
- `auggie`
- `roo`
- `codebuddy`
- `amp`
- `shai`
- `kiro-cli`
- `kiro`
- `agy`
- `bob`
- `qodercli`
- `vibe`
- `generic`

### 3.4 成果物

`/sdd.design` が生成する v1 必須成果物は以下で固定する。

- `overview.md`
- `ui-storybook/`
- `ui-fields.yaml`
- `sequence-flows/*.md`
- `common-design-refs.yaml`
- `batch-design.md`
- `test-design.md`
- `test-plan.md`
- `traceability.yaml`

## 4. リポジトリ構成

以下の構成で実装する。`spec-kit` から流用した共通基盤と `SpecKit for Projects` 独自のドメイン実装を分離しやすい構成にする。

```text
docs/
├── basic-design.md
└── implementation-plan.md

pyproject.toml
README.md

src/
└── general_sdd/
    ├── __init__.py
    ├── cli.py
    ├── commands/
    │   ├── init.py
    │   └── check.py
    ├── domain/
    │   ├── models.py
    │   ├── ids.py
    │   └── validators.py
    ├── foundations/
    │   ├── app.py
    │   ├── templating.py
    │   ├── scaffolding.py
    │   └── generation.py
    ├── services/
    │   ├── project_initializer.py
    │   ├── agent_template_installer.py
    │   ├── environment_checker.py
    │   ├── context_assembler.py
    │   └── consistency_checker.py
    ├── renderers/
    │   ├── markdown.py
    │   ├── html.py
    │   └── yaml.py
    ├── templates/
    │   ├── project/
    │   ├── commands/
    │   └── agent-files/
    └── io/
        ├── filesystem.py
        ├── markdown_parser.py
        └── yaml_loader.py

tests/
├── unit/
├── integration/
└── golden/
```

## 5. 内部アーキテクチャ

### 5.1 設計原則

- CLI と生成ロジックを分離する
- `spec-kit` 由来の共通基盤と `SpecKit for Projects` 固有ドメインを分離する
- 成果物生成は agent command template 駆動にする
- ファイル I/O とドメイン処理を分離する
- 更新系コマンドは idempotent を基本とする
- 生成前後に最小限の整合チェックを必ず実施する

### 5.2 主要内部モデル

以下の Pydantic モデルを v1 の中心モデルとして定義する。

- `ProjectStandards`
  - `tech_stack`
  - `coding_rules`
  - `architecture_principles`
- `Brief`
  - `brief_id`
  - `title`
  - `background`
  - `scope_in`
  - `scope_out`
  - `constraints`
  - `requirements[]`
- `Requirement`
  - `id`
  - `summary`
  - `description`
  - `priority`
- `DesignBundle`
  - `design_id`
  - `brief_id`
  - `artifacts`
- `TraceabilityEntry`
  - `requirement_id`
  - `primary_artifact`
  - `related_artifacts[]`
  - `project_standards[]`
  - `status`
- `TaskItem`
  - `task_id`
  - `title`
  - `requirement_ids[]`
  - `artifact_refs[]`
  - `depends_on[]`

v1 では Python 側に LLM API 抽象層は持たない。LLM 呼び出しは agent-specific command template が担当し、Python 側はテンプレート配布、コンテキスト組み立て補助、初期化、検証を担う。

### 5.3 主要サービス責務

`foundations/` 配下は `spec-kit` からの流用または派生実装の受け皿とし、 `services/` と `domain/` は `SpecKit for Projects` 固有の責務を持つ。

- `project_initializer.py`
  - ディレクトリ生成
  - 共通統制文書テンプレート配置
  - agent-specific command template 配置
- `agent_template_installer.py`
  - `--ai` ごとの command files 変換
  - `generic` 向け出力先制御
- `environment_checker.py`
  - AI ツール存在確認
  - 配置済みテンプレート整合確認
- `context_assembler.py`
  - AI コマンドが参照する共通コンテキストの組み立て
- `consistency_checker.py`
  - 必須成果物の存在確認
  - 要件未割当検知
  - 主要反映先の欠落検知

## 6. 実装フェーズ

### Phase 0: `spec-kit` 流用調査とベース移植

- `spec-kit` の CLI 骨格、テンプレート展開、初期化処理、テスト基盤を調査する
- 流用対象ファイル一覧を確定する
- `SpecKit for Projects` に取り込む共通基盤コードを `foundations/` 中心に配置する
- 流用コードから `spec/plan/tasks` 固有名を排除し、基盤レイヤだけを残す

完了条件:

- 流用対象一覧が文書化される
- CLI 起動、テンプレート展開、ファイル出力の基盤コードが `SpecKit for Projects` 側で単独動作する
- `spec-kit` 固有ドメインへ直接依存しない状態になる

### Phase 1: リポジトリ整備と品質基盤

- `pyproject.toml` を追加
- `src/` / `tests/` 構成を整える
- `ruff`, `mypy`, `pytest` を設定する
- `README.md` に最小使用例を追加する

完了条件:

- `uv run pytest` が通る
- `uv run ruff check .` が通る
- `uv run mypy src` が通る

### Phase 2: ドメインモデルと I/O 基盤

- Pydantic モデルを定義
- ID 採番ロジックを定義
- Markdown / YAML 読み書きユーティリティを実装
- 例外モデルを定義
- AI コマンドが使う共通コンテキスト組み立てルールを定義

完了条件:

- `Brief` と `TraceabilityEntry` のシリアライズ/デシリアライズが通る
- ID 採番規則が unit test で固定される

### Phase 3: `sdd init` と `sdd check`

- CLI エントリポイントを作る
- `sdd init` を実装する
- `sdd check` を実装する
- `.specify/project/` と agent-specific command templates を出力する

完了条件:

- 空ディレクトリで `sdd init --ai codex` 実行後、必須ファイルがすべて存在する
- `sdd init --ai generic --ai-commands-dir <path>` が期待先へ出力する
- `sdd check` が未導入エージェントと欠落テンプレートを検出する
- 再実行しても既存ファイルを不正に壊さない

### Phase 4: AI コマンドテンプレート実装

- `/sdd.brief`、`/sdd.design`、`/sdd.tasks`、`/sdd.implement` の command templates を作る
- AI ごとの差し替えテンプレートを配置する
- `brief-id` と `design-id` の命名規約をテンプレートへ反映する

完了条件:

- Codex 系と少なくとももう 1 系統で command templates が正しくインストールされる
- `001-kebab-slug` 形式の ID 規約がテンプレート内で固定される
- 配布テンプレートが golden test と一致する

### Phase 5: 設計成果物テンプレート実装

- `brief/common-design/design/tasks/implement` 向けの成果物テンプレートと command template を実装する
- `common_design` と `specific_design` の成果物テンプレートを実装する
- `traceability.yaml` の初期割当ルールをテンプレートへ反映する
- 一貫性チェックを実装する

完了条件:

- `designs/specific_design/<design-id>/` 配下に必須成果物がすべて作られる
- `traceability.yaml` に全要件が掲載される
- 画面中心、API 中心、バッチ中心の 3 サンプルで生成が通る

### Phase 6: 再生成運用と差分確認前提の整備

- `brief` / `design` は full-file overwrite、`tasks.md` は ledger 保持再生成という運用を README と command template に明記する
- `git diff` 確認前提のガイドを追加する
- managed blocks / in-place merge を v1 非対応として固定する

完了条件:

- `designs/specific_design/<design-id>/` 再生成時に full-file overwrite が行われる前提が文書化される
- 差分確認手順が README と command templates に含まれる

### Phase 7: 検証と整備

- サンプルプロジェクトを追加する
- README の使用例を拡充する
- 既知制約を文書化する

完了条件:

- サンプル 3 ケースで `init -> AI commands -> generated outputs` の運用が通る
- README の手順どおりに再現できる

## 7. テンプレート実装順序

テンプレートは以下の順で作る。

1. `.specify/project/tech-stack.md`
2. `.specify/project/coding-rules.md`
3. `.specify/project/architecture-principles.md`
4. `.specify/templates/commands/brief.md`
5. `.specify/templates/commands/design.md`
6. `.specify/templates/commands/tasks.md`
7. `briefs/<brief-id>.md`
8. `overview.md`
9. `ui-storybook/`
10. `ui-fields.yaml`
11. `@storybook/html` stories / HTML templates
12. `common-design-refs.yaml`
13. `batch-design.md`
14. `sequence-flows/*.md`
15. `test-design.md`
16. `test-plan.md`
17. `traceability.yaml`
20. `tasks.md`

この順序にする理由は、共通統制文書と AI コマンド配布を先に固定し、その後に `brief`、業務概要、UI、API/データ、処理順序、テスト、追跡、タスクの順で依存方向を揃えるためである。

## 8. `spec-kit` からの流用対象

v1 では以下を優先流用対象とする。

- CLI アプリケーション初期化コード
- コマンド配線
- テンプレート探索とレンダリング機構
- プロジェクト初期化時のファイル展開ロジック
- ファイル書き込みの共通処理
- テスト fixture と golden test の共通パターン
- `templates/commands/*.md` 配布モデル

以下は参考にするが、実装は `SpecKit for Projects` 用に再構築する。

- `spec` / `plan` / `tasks` の生成ロジック
- `brief/design/tasks/implement` の command semantics
- 生成物の種類と成果物依存
- ドメインモデル
- タスク分解ルール

Phase 0 の成果物として [upstream-spec-kit-map.md](/Users/iwasakishinya/Documents/hook/general_sdd/docs/upstream-spec-kit-map.md) を作成し、取り込み元コミット、流用対象、配置先、差し替え方針、attribution ルールを固定する。

## 9. テスト計画

### 9.1 Unit Test

- ID 採番
- Pydantic モデルのバリデーション
- YAML 読み書き
- テンプレートレンダリング
- トレーサビリティ生成

### 9.2 Integration Test

- `sdd init --ai codex` の新規実行
- `sdd init --ai generic --ai-commands-dir <path>` の実行
- `sdd init` の再実行
- `sdd check` の実行
- `designs/specific_design/<design-id>/` 再生成前提の overwrite 運用確認

### 9.3 Golden Test

以下の 3 ケースを固定サンプルとして用意する。

- 画面中心案件
- API 中心案件
- バッチ中心案件
- Codex 系 command template 配布
- 非 Codex 系 command template 配布

各ケースで、生成される Markdown / YAML / HTML の構造と主要フィールドを比較する。

### 9.4 受け入れ基準

- `sdd init --ai codex` で共通統制文書と agent command files が配置される
- `sdd init --ai generic --ai-commands-dir <path>` が期待先へ出力する
- `sdd check` が未導入エージェントと欠落テンプレートを検出する
- `traceability.yaml` から要件ごとの成果物参照が可能である
- `test-design.md` と `test-plan.md` が毎回生成される
- `ui-fields.yaml` と `traceability.yaml` が YAML として妥当である
- command templates が `git diff` 前提の再生成運用を案内する

## 10. リスクと対処

### リスク 1: テンプレートが重すぎて保守不能になる

対処:

- v1 はテンプレートを薄く保つ
- 共通説明を重複させず、参照前提に寄せる

### リスク 2: `brief` の入力粒度が足りず、設計生成が形骸化する

対処:

- `brief` の最小入力項目を厳密に固定する
- 追加記述欄は残すが、必須項目不足は警告する

### リスク 3: 要件と成果物の自動対応付けが不自然になる

対処:

- v1 は高精度自動推論を目指さず、標準割当ルールを実装する
- `traceability.yaml` は人手修正可能な形を維持する

### リスク 4: HTML モックが実装コード化して設計境界が崩れる

対処:

- HTML モックは静的モックに限定する
- API 呼び出しコードやビルド依存を入れない

### リスク 5: `spec-kit` 由来コードへの依存が深すぎて、独自進化しづらくなる

対処:

- 流用基盤を `foundations/` に隔離する
- `SpecKit for Projects` 固有ロジックは `domain/` と `services/` に閉じ込める
- 上流の内部構造に対する直接 import を避ける

## 11. 実装完了の定義

v1 実装完了は以下を満たした時点とする。

1. `sdd init` と `sdd check` の 2 コマンドが動作する。
2. `/sdd.brief`、`/sdd.design`、`/sdd.tasks`、`/sdd.implement` の AI command templates が配布される。
3. 共通統制文書、設計成果物、UI 成果物、シーケンス成果物、テスト成果物、`traceability.yaml`、`tasks.md` の ledger、実装実行結果を扱う前提が command templates に埋め込まれている。
4. Codex 系と少なくとももう 1 系統の AI command template 配布が通る。
5. [upstream-spec-kit-map.md](/Users/iwasakishinya/Documents/hook/general_sdd/docs/upstream-spec-kit-map.md) と実コード配置が一致する。
6. README だけで初回利用者が再現できる。

## 12. 実装時の前提

- v1 はローカル CLI 専用とし、Web UI は実装しない。
- v1 の価値は「実行可能な AI command template 配布 + 設計成果物テンプレート」であり、CLI 単体で全文生成を完結しない。
- Python CLI に OpenAI 互換 API 抽象層は持たない。
- 生成済み文書の高度なマージや意味的差分更新は後回しにし、`brief` / `design` は full-file overwrite + `git diff` 確認方針を採る。
- `tasks.md` だけは `TASK-xxx` 単位で execution ledger を保持する限定的な再生成を採る。
- 公開 OSS 名は引き続き `SpecKit for Projects` を仮称とする。
