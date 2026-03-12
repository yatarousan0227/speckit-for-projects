# SpecKit for Projects 基本設計書 v1

- 文書状態: Draft
- 作成日: 2026-03-11
- 対象: `SpecKit for Projects` OSS コア開発者
- 正本形式: Markdown

## 背景と課題

日本の SI 現場では、要件から実装までの間に複数種類の設計書を作成し、顧客説明、社内レビュー、実装分担、変更影響分析に利用することが多い。一方で、既存の Spec-Driven Development ツールは、機能仕様から実装計画とタスクへ落とす流れには強いが、SI で日常的に使われる基本設計書と詳細設計書の束を一次成果物として扱う前提にはなっていない。

`SpecKit for Projects` はこのギャップを埋めるための OSS である。`github/spec-kit` の「曖昧な要求を構造化し、成果物を連鎖生成する」という思想は継承するが、互換性を主目的にはしない。v1 では、SI 設計リーダーが案件または機能単位の入力から設計書束を一貫生成し、要件追跡と文書間整合を保ったまま実装タスクへ接続できることを目的とする。

本書は `SpecKit for Projects` 自体の基本設計書であり、OSS の目的、対象利用者、ワークフロー、CLI 外部仕様、生成物モデル、v1 の境界を定義する。内部モジュール責務、テンプレート DSL、永続化方式、差分更新アルゴリズムは本書の対象外とし、次フェーズの詳細設計で扱う。

## 対象ユーザーと利用シナリオ

主対象ユーザーは、SI 案件で基本設計と詳細設計の整備責任を持つ設計リーダーである。補助的な利用者として、設計書レビュー担当者と、設計書を受け取って実装タスクへ落とし込む開発エンジニアを想定する。

### 主要ユーザー

| ユーザー | 主な責務 | `SpecKit for Projects` に期待すること |
| --- | --- | --- |
| SI 設計リーダー | 案件/機能の設計方針確定、文書整備、レビュー主導 | 入力から設計書束を素早く作り、要件漏れと文書不整合を減らす |
| レビュー担当 | 設計妥当性、粒度、トレーサビリティ確認 | 文書間の役割境界と変更影響を追いやすくする |
| 実装エンジニア | 設計読解、実装分解、作業計画 | 設計書束からタスク化しやすい構造を得る |

### 利用シナリオ

1. 設計リーダーが `sdd init --ai <agent>` を実行し、対象 AI エージェント向けのコマンドテンプレートと共通統制文書をプロジェクトへ導入する。
2. 設計リーダーが AI エージェント内で `/sdd.brief` を実行し、設計の起点となる `brief` を作成する。
3. 設計リーダーが AI エージェント内で `/sdd.design` を実行し、基本設計と詳細設計を跨ぐ設計書束、UI 成果物束、シーケンス成果物束、テスト成果物束を同一設計束として生成する。
4. レビュー担当が設計書束、シーケンス図、テスト設計、`traceability.yaml` を使って、要件ごとの反映先と不足箇所を確認する。
5. 実装エンジニアが AI エージェント内で `/sdd.tasks` を実行し、要件と設計書、シーケンス図、テスト成果物に紐づいた実装タスク兼実行台帳を得る。
6. 実装エンジニアが AI エージェント内で `/sdd.implement` を実行し、選択した `TASK-xxx` だけを実装し、検証結果を `tasks.md` に反映する。
7. 途中で要件変更が入った場合、設計リーダーが `/sdd.brief` と `/sdd.design` を再実行し、上書き差分を `git diff` で確認しながら影響箇所を再レビューする。

## プロダクト提供価値

`SpecKit for Projects` の v1 提供価値は次の 6 点に集約する。

1. 1 回の入力起点から、SI 現場で使う設計書束を一貫生成できる。
2. 設計書ごとの役割境界を固定し、同じ内容が複数文書に無秩序に重複する状態を減らせる。
3. `traceability.yaml` を正規成果物に含めることで、要件から設計書、シーケンス図、テスト成果物、タスクまでの追跡を維持できる。
4. 実装前に「文書整合」と「要件追跡」を正規フローへ組み込み、設計レビューを単なる文章レビューではなく構造レビューへ寄せられる。
5. シーケンス図を設計束に含めることで、画面/API/バッチ/内部処理の責務境界と処理順序を明示できる。
6. テスト設計とテスト計画を必須成果物に含めることで、要件をどう検証するかを設計段階で固定できる。

`spec-kit` との差分は以下の通りである。

| 観点 | `spec-kit` | `SpecKit for Projects` v1 |
| --- | --- | --- |
| 中心成果物 | 機能仕様書、実装計画、タスク | SI 設計書束、シーケンス図、テスト成果物、トレーサビリティ、タスク |
| 実行主体 | CLI の `init/check` + AI コマンド | CLI の `init/check` + AI コマンド |
| 基本フロー | `specify init` 後に `spec/plan/tasks` 系コマンドを AI で実行 | `sdd init` 後に `brief/design/tasks/implement` 系コマンドを AI で実行 |
| 重視点 | 実装可能な仕様化 | 設計書体系化、文書整合、要件追跡 |
| 互換方針 | 自身が基準 | UX と配布モデルは継承し、コマンド名と成果物は再設計 |

## ワークフロー全体像

### 標準フロー

1. `sdd init`
   - プロジェクトに `SpecKit for Projects` 用の規約、用語集、テンプレート設定、共通統制文書、AI エージェント向けコマンドテンプレート、雛形ディレクトリを配置する。
2. `sdd check`
   - 対象 AI エージェントの導入状況と、配布済みテンプレート/共通統制文書の整合性を確認する。
3. AI エージェント内で `/sdd.brief`
   - 案件/機能の目的、業務背景、対象範囲、前提制約、主要要件を入力し、共通統制文書を参照しながら設計起点文書を作成する。
4. AI エージェント内で `/sdd.design`
   - `brief` と共通統制文書をもとに、設計書束、UI 成果物束、シーケンス成果物束、テスト成果物束、`traceability.yaml` を生成または更新する。
   - v1 は上書き再生成を正式運用とし、差分確認は `git diff` を前提とする。
5. AI エージェント内で `/sdd.tasks`
   - 設計書束、トレーサビリティ情報、共通統制文書をもとに、実装タスク兼実行台帳を生成する。
6. AI エージェント内で `/sdd.implement`
   - `design-id` と `TASK-xxx` を指定し、対象 task のコード変更、ローカル検証、`tasks.md` 実行台帳更新を行う。

### 成果物配置

```text
.specify/
├── glossary.md
├── conventions/
├── templates/
│   └── commands/
│       ├── brief.md
│       ├── design.md
│       ├── tasks.md
│       └── implement.md
└── project/
    ├── tech-stack.md
    ├── coding-rules.md
    └── architecture-principles.md

briefs/
└── <brief-id>.md

designs/
├── common_design/
│   ├── api/
│   │   └── CD-API-001-*.md
│   ├── data/
│   │   └── CD-DATA-001-*.md
│   ├── module/
│   │   └── CD-MOD-001-*.md
│   └── ui/
│       ├── CD-UI-001-screen-catalog.md
│       └── CD-UI-002-navigation-rules.md
└── specific_design/
    └── <design-id>/
        ├── overview.md
        ├── ui-storybook/
        │   ├── README.md
        │   ├── package.json
        │   ├── .storybook/
        │   │   ├── main.ts
        │   │   ├── preview.ts
        │   │   └── preview.css
        │   ├── stories/
        │   │   └── SCR-001-*.stories.js
        │   └── components/
        │       └── SCR-001-*.html
        ├── ui-fields.yaml
        ├── sequence-flows/
        │   ├── SEQ-001-*.md
        │   └── SEQ-002-*.md
        ├── common-design-refs.yaml
        ├── batch-design.md
        ├── test-design.md
        ├── test-plan.md
        ├── traceability.yaml
        └── tasks.md
```

### フロー上の原則

- `sdd init` と `sdd check` は Python CLI が担い、 `brief/design/tasks/implement` は AI エージェント向けコマンドとして提供する。
- `brief` は設計の唯一の案件入力であり、`design` はこれと共通統制文書を参照して設計書束を生成する。
- `design` は個別文書を独立生成するのではなく、同一 `design-id` の束として扱う。
- `tasks` は `overview.md` だけでなく、設計書束全体、UI 成果物束、シーケンス図、テスト成果物、`traceability.yaml`、共通統制文書を読んで生成される。
- タスク生成前に、文書欠落、要件未割当、主要文書間の矛盾を検出する運用を標準とする。
- 技術選定、コーディング規約、アーキテクチャ原則は案件単位の設計束に重複記述せず、 `.specify/project/` 配下を正本とする。
- `brief` と `design` の再生成は full-file overwrite を前提とし、`tasks.md` は `TASK-xxx` 単位で実行台帳を保持しながら再生成する。

## CLI 外部仕様

### コマンド一覧

| コマンド | 目的 | 主入力 | 主出力 |
| --- | --- | --- | --- |
| `sdd init` | プロジェクト初期化 | 実行対象ディレクトリ、AI 種別、初期設定 | `.specify/` 配下の設定、テンプレート、共通統制文書、agent command files |
| `sdd check` | 環境検査 | AI 種別、実行環境 | AI ツール存在確認、テンプレート整合確認、警告一覧 |

### AI エージェント向けコマンド

| コマンド | 目的 | 主入力 | 主出力 |
| --- | --- | --- | --- |
| `/sdd.brief` | 設計起点の作成 | 案件/機能概要、背景、制約、要件、共通統制文書 | `briefs/<brief-id>.md` |
| `/sdd.common-design` | 共有設計の生成/更新 | shared kind、関連 brief、共通統制文書 | `designs/common_design/` 配下の API/Data/Module/UI 設計 |
| `/sdd.design` | specific design 束の生成/更新 | `brief-id` または `brief` ファイル、共通統制文書、`common_design` | `designs/specific_design/<design-id>/` 配下の設計成果物と `traceability.yaml` |
| `/sdd.tasks` | 実装タスク兼実行台帳生成 | `design-id`、specific design、共通統制文書、`common_design` | `designs/specific_design/<design-id>/tasks.md` |
| `/sdd.implement` | 選択 task の実装実行 | `design-id`、`TASK-xxx`、specific design、共通統制文書、既存コード | コード差分と更新済み `designs/specific_design/<design-id>/tasks.md` |

### コマンド別仕様

#### `sdd init`

- 目的: `SpecKit for Projects` を利用するリポジトリに最低限の規約と雛形を導入する。
- 必須結果:
  - `.specify/glossary.md`
  - `.specify/conventions/`
  - `.specify/templates/`
  - `.specify/project/tech-stack.md`
  - `.specify/project/coding-rules.md`
  - `.specify/project/architecture-principles.md`
  - `.specify/templates/commands/brief.md`
  - `.specify/templates/commands/design.md`
  - `.specify/templates/commands/tasks.md`
  - `.specify/templates/commands/implement.md`
- v1 前提:
  - 設定はローカルファイル管理のみ
  - `--ai <agent>` に応じて agent-specific command files を配布する
  - `--ai-commands-dir` は `generic` 用の出力先指定に使う

#### `sdd check`

- 目的: 利用前提となる AI 実行環境とテンプレート配置を検証する。
- 確認対象:
  - 対象 AI ツールの存在確認
  - `.specify/templates/commands/` の欠落確認
  - `.specify/project/` 配下の必須文書確認
- 出力要件:
  - 成功/警告/失敗を区別して返す
  - 修復が必要な項目を列挙する

#### `/sdd.brief`

- 目的: 設計書生成の起点となる案件/機能の要約を構造化する。
- 最低限含める入力項目:
  - 背景と目的
  - 対象業務または対象機能
  - スコープ内 / スコープ外
  - 利用者または外部接続先
  - 主要要件一覧
  - 制約事項
- 参照前提:
  - `.specify/project/tech-stack.md`
  - `.specify/project/architecture-principles.md`
- 出力要件:
  - 各要件に一意な要件 ID を付与する
  - `design` が参照可能な安定フォーマットで保存する
  - `brief-id` は `001-kebab-slug` 形式の repo-local 連番とする

#### `/sdd.design`

- 目的: `brief` を設計書束へ展開する。
- 出力単位: `designs/specific_design/<design-id>/`
- 参照前提:
  - `briefs/<brief-id>.md`
  - `.specify/project/tech-stack.md`
  - `.specify/project/coding-rules.md`
  - `.specify/project/architecture-principles.md`
- 必須成果物:
  - `overview.md`
  - `ui-storybook/`
  - `ui-fields.yaml`
  - `sequence-flows/`
  - `common-design-refs.yaml`
  - `batch-design.md`
  - `test-design.md`
  - `test-plan.md`
  - `traceability.yaml`
- 完了条件:
  - 必須成果物がすべて存在する
  - 各要件 ID が `traceability.yaml` に登録されている
  - 文書ごとの役割境界に基づき、主要記述先が割り当てられている
  - 再実行時は同一 `design-id` 配下を上書き更新する

#### `/sdd.tasks`

- 目的: 設計書束から実装可能な作業単位を生成する。
- 入力前提:
  - `design` が完了している
  - `traceability.yaml` が存在し、要件未割当がない
  - `.specify/project/coding-rules.md` が存在する
- 出力要件:
  - 要件 ID と設計書参照先を含む
  - 実装順序または依存関係を表現できる
  - テスト成果物参照を含む
  - `Execution Status`、`Checklist`、`Implementation Log`、`Changed Files`、`Verification Results` を持つ mutable section を各 task に含む
  - 再生成時は同じ `TASK-xxx` の mutable section を保持できる

#### `/sdd.implement`

- 目的: 選択した `TASK-xxx` のコード変更とローカル検証を行い、`tasks.md` 実行台帳を更新する。
- 入力前提:
  - `tasks.md` が存在し、対象 `TASK-xxx` が定義されている
  - `traceability.yaml`、`common-design-refs.yaml`、`test-design.md`、`test-plan.md` が存在する
  - `.specify/project/tech-stack.md`、`.specify/project/coding-rules.md`、`.specify/project/architecture-principles.md` が存在する
- 出力要件:
  - 指定 task のみを対象に実装する
  - 関連するテストまたは検証コマンドを実行する
  - `tasks.md` の task 定義部分を変更せず、mutable section のみ更新する
  - 実装基盤が不足する場合は不足内容を列挙して停止する

## 設計書束の情報モデル

### 基本単位

- `project standards`: プロジェクト共通の技術選定、規約、原則を保持する統制文書群
- `brief`: 案件/機能の要求と制約を保持する起点文書
- `common design`: 複数 feature で共有する API/Data/Module/UI の設計正本
- `specific design`: 1 つの `design-id` に紐づく feature 固有の設計書束
- `requirement`: `brief` 内の一意な要件
- `design artifact`: 設計書束を構成する個別文書
- `traceability`: 要件と設計成果物の対応情報

### 設計書ごとの役割

| 文書 | 主目的 | 主入力 | 主な出力先 |
| --- | --- | --- | --- |
| `overview.md` | 業務/機能の全体像、対象範囲、主要フロー整理 | `brief` | 他成果物の前提 |
| `ui-storybook/` | `@storybook/html` による実行可能な UI review bundle。`package.json`、Storybook config、story、HTML template を含む | `overview.md`, `brief` | UI レビュー、UI 実装タスク |
| `ui-fields.yaml` | 画面項目定義、入出力、バリデーション、共有設計との対応整理 | `ui-storybook/`, `brief`, `common-design-refs.yaml` | Storybook 補足、UI 実装タスク、追跡情報 |
| `sequence-flows/*.md` | 主要処理の時系列、責務境界、呼び出し順序整理 | `ui-storybook/`, `common-design-refs.yaml`, `batch-design.md`, `brief` | 実装順序理解、レビュー、タスク分解 |
| `common-design-refs.yaml` | feature から参照する共有設計 ID と利用メモを整理 | `brief`, `designs/common_design/` | 追跡情報、タスク分解、実装参照 |
| `batch-design.md` | 定期処理、非同期処理、連携バッチ整理 | `overview.md`, `common-design-refs.yaml`, `brief` | バッチ実装タスク |
| `test-design.md` | 要件ごとの確認観点、正常/異常/境界、観点別の検証内容整理 | `brief`, `overview.md`, `ui-storybook/`, `common-design-refs.yaml`, `batch-design.md` | テストタスク、レビュー |
| `test-plan.md` | テストレベル、実施範囲、順序、体制、環境、進め方整理 | `test-design.md`, `brief`, 共通統制文書 | テスト実施計画、レビュー |

### Common Design 成果物束

| 成果物 | 主目的 | 位置づけ |
| --- | --- | --- |
| `designs/common_design/api/*.md` | 共有 API 契約の正本を保持する | 共有 API 設計の正本 |
| `designs/common_design/data/*.md` | 共有データモデルの正本を保持する | 共有データ設計の正本 |
| `designs/common_design/module/*.md` | 共有責務境界と公開 I/F を保持する | 共有モジュール設計の正本 |
| `designs/common_design/ui/*.md` | 共有画面一覧と共有遷移ルールの正本を保持する | 共有 UI 設計の正本 |

### UI 成果物束

| 成果物 | 主目的 | 位置づけ |
| --- | --- | --- |
| `ui-storybook/` | `@storybook/html` による UI story と HTML テンプレートを保持し、ローカル起動と build 検証ができる | feature 固有 UI レビュー bundle |
| `ui-fields.yaml` | 画面項目定義を構造化して保持する | 画面項目定義の正本 |

### シーケンス成果物束

| 成果物 | 主目的 | 位置づけ |
| --- | --- | --- |
| `sequence-flows/*.md` | 主要な業務処理やシステム間連携の順序を示す | 処理順序と責務境界の正本 |

### テスト成果物束

| 成果物 | 主目的 | 位置づけ |
| --- | --- | --- |
| `test-design.md` | 要件ごとの検証観点と確認内容を定義する | テスト設計の正本 |
| `test-plan.md` | テストの実施方針と進め方を定義する | テスト計画の正本 |

### 共通統制文書

| 成果物 | 主目的 | 位置づけ |
| --- | --- | --- |
| `.specify/project/tech-stack.md` | 採用技術、バージョン、利用制約を定義する | 技術スタックの正本 |
| `.specify/project/coding-rules.md` | 命名、構成、例外処理、ログ、テスト、レビュー規約を定義する | コーディング規約の正本 |
| `.specify/project/architecture-principles.md` | 依存方向、責務境界、設計原則を定義する | アーキテクチャ統制の正本 |

### 文書境界の原則

- `overview.md` は全体像と用語統制を担い、詳細な項目定義を持ち込まない。
- `ui-storybook/` は `@storybook/html` を使った feature 固有 UI レビュー bundle であり、共有画面一覧や共有遷移ルールの正本にはしない。
- `ui-fields.yaml` は画面項目定義の正本であり、 Storybook story や HTML template 内コメントを正本にしない。
- `sequence-flows/*.md` は処理順序と責務境界の正本であり、画面レイアウトや API 項目定義の正本にならない。
- `batch-design.md` は定期・非同期処理の正本であり、オンライン画面フローと混在させない。
- `designs/common_design/api/*.md` は外部 I/F の正本であり、画面の説明を主目的にしない。
- `designs/common_design/data/*.md` はデータ構造の正本であり、処理手順の説明を主目的にしない。
- `designs/common_design/module/*.md` は内部責務分割の正本であり、外部契約の再定義をしない。
- `designs/common_design/ui/*.md` は共有画面一覧と共有遷移ルールの正本であり、feature 固有の条件分岐や UI 状態を主記述先にしない。
- `test-design.md` は検証観点の正本であり、単なるタスクリストや実施日程表にしない。
- `test-plan.md` は実施方針の正本であり、個別要件の詳細確認観点を主記述先にしない。
- `.specify/project/tech-stack.md` は技術選定の正本であり、案件ごとの設計束に再定義しない。
- `.specify/project/coding-rules.md` はコーディング規約の正本であり、 `tasks.md` はこれを参照して作業規律と実装実行記録へ落とし込む。
- `.specify/project/architecture-principles.md` はアーキテクチャ統制の正本であり、設計束はこれに従って具体化する。

### 共通統制文書の最小管理項目

`tech-stack.md` には少なくとも次を保持する。

- 言語とバージョン方針
- 採用フレームワーク
- 利用許可/非推奨ライブラリ
- 実行基盤
- テスト基盤
- CI/CD 方針

`coding-rules.md` には少なくとも次を保持する。

- 命名規約
- ディレクトリ/レイヤ構成規約
- 例外処理方針
- ログ方針
- コメント方針
- テスト記述ルール
- レビュー観点

`architecture-principles.md` には少なくとも次を保持する。

- 依存方向
- レイヤ責務
- API/UI/DB の境界
- 同期/非同期処理原則
- 拡張時の原則

### UI 項目定義の最小管理項目

`ui-fields.yaml` には少なくとも次の項目を保持する。

- 画面 ID
- 項目 ID
- 項目名
- ラベル
- 種別
- 表示領域
- 入出力区分
- 必須/任意
- バリデーション
- 初期値
- 値の取得元
- API 項目との対応
- データ項目との対応
- 備考

### シーケンス図の最小管理方針

- 主要な画面起点処理、API 起点処理、バッチ起点処理ごとに少なくとも 1 本のシーケンス図を持つ。
- 各シーケンス図は `SEQ-xxx` の ID を持ち、対象要件 ID を辿れるようにする。
- 図の表現形式は v1 では Markdown 内の Mermaid `sequenceDiagram` を第一候補とする。
- 登場主体は利用者、画面、API、バッチ、外部システム、内部モジュールのいずれかで統一する。
- UI 要素の見た目ではなく、イベント発火、入力検証、外部呼び出し、永続化、結果返却を中心に記述する。

### Mermaid 図の活用方針

- Mermaid 図は文章、表、YAML の代替ではなく、関係性を圧縮して示す補助表現として使う。
- `overview.md` は `flowchart` 系で主要フローを、`designs/common_design/module/*.md` は依存関係を、`designs/common_design/data/*.md` は `erDiagram` で主要エンティティ関係を、`batch-design.md` は実行経路を表す。
- `.specify/project/domain-map.md` が存在する場合は `graph` 系で durable なドメイン依存を示す。
- 図に登場するノード名は `REQ-xxx`、`DOM-xxx`、`MOD-xxx`、`ENT-xxx`、`API-xxx` など本文の識別子と揃える。
- 図だけを正本にせず、図の下に同じ対象の構造化テキストを残す。
- 色や装飾は最小限とし、AI とレビュー担当が差分比較しやすい安定した記法を優先する。

### テスト成果物の最小管理方針

`test-design.md` には少なくとも次を保持する。

- 要件 ID ごとの確認観点
- 正常系、異常系、境界値観点
- 画面、API、バッチ、権限、データ整合などの観点分類
- 関連する設計書、シーケンス図への参照

`test-plan.md` には少なくとも次を保持する。

- テストレベル
- 実施範囲
- 実施順序
- 実施体制
- 実施環境
- 進行ルール

### `design-id` の扱い

- `design-id` は案件または機能単位の設計束を識別する ID とする。
- v1 では `001-kebab-slug` 形式の repo-local 連番を基本規約とする。
- 同一 `design-id` に対する `/sdd.design` の再実行は上書き更新扱いとし、新規束作成とは区別する。

## トレーサビリティ方針

`traceability.yaml` は v1 の正規成果物であり、単なる補助ファイルではない。要件、設計書、タスクの接続点として扱う。

### 管理対象

- 要件 ID
- 要件の主要反映先文書
- 関連する副次文書
- 関連するシーケンス図
- 関連するテスト成果物
- タスク生成時の参照先
- 共通統制文書との参照関係
- 未反映または要確認の状態

### v1 で保証したいこと

1. `brief` に記載された全要件が `traceability.yaml` に掲載される。
2. 各要件に少なくとも 1 つの主要反映先文書が割り当てられる。
3. `tasks` 生成時に、各タスクが参照すべき要件 ID と設計書、シーケンス図、テスト成果物を辿れる。
4. 要件変更時に、影響文書候補を一覧できる。

### 例示イメージ

```yaml
requirements:
  - id: BR-001
    summary: 申請一覧を画面で検索できる
    primary_artifact: ui-storybook/stories/SCR-002-list.stories.js
    related_artifacts:
      - ui-fields.yaml
      - ui-storybook/components/SCR-002-list.html
      - sequence-flows/SEQ-001-application-search.md
      - common-design-refs.yaml
      - test-design.md
      - test-plan.md
    project_standards:
      - .specify/project/tech-stack.md
      - .specify/project/coding-rules.md
    status: mapped
```

### レビュー観点

- 未割当要件が存在しないか
- 主要反映先が妥当か
- 画面/API/データ/バッチ/モジュールに過不足なく分配されているか
- 要件変更時の影響範囲が追えるか

## v1 スコープ / 非スコープ

### v1 スコープ

- Markdown 正本の設計書束生成
- HTML モックを含む UI 成果物束生成
- Markdown ベースのシーケンス図生成
- `test-design.md` と `test-plan.md` の生成
- `brief -> design -> tasks` ワークフローの定義
- 設計書束 + UI 成果物束 + シーケンス成果物束 + テスト成果物束モデルの固定
- テクノロジースタック、コーディング規約、アーキテクチャ原則を共通統制文書として管理
- `traceability.yaml` による要件追跡
- SI 設計リーダーを主対象とした CLI 指向の利用モデル

### v1 非スコープ

- Word / Excel / PDF エクスポート
- 運用設計、権限制御設計、非機能設計の必須生成
- Web UI や SaaS 提供
- `spec-kit` とのコマンド互換、テンプレート互換
- 自動レビュー承認ワークフロー

### 基本設計レビュー完了条件

- 新規案件 1 件を入力したとき、どのコマンド順で設計書束、UI 成果物束、シーケンス成果物束、テスト成果物束まで到達するかを第三者が迷わず説明できる。
- 各設計書の役割境界が重複せず、入力元と出力先が明確である。
- `brief` の 1 要件が `traceability.yaml` を介して各設計書、シーケンス図、テスト成果物へ追跡できる前提が文書内で成立している。
- 設計束が共通統制文書と矛盾せず、案件単位で技術選定や規約を再定義していない。
- 画面中心案件、API 中心案件、バッチ中心案件の 3 ケースで設計書束モデルが破綻しない。
- 主要処理について、画面/API/バッチ/内部モジュールの責務境界をシーケンス図で説明できる。
- 主要要件について、確認観点と実施方針を `test-design.md` と `test-plan.md` で説明できる。
- 実装者が Word/Excel 出力や運用設計まで v1 に含むと誤解しない。

### 受け入れシナリオ

1. SI 設計リーダーが新規案件を開始し、`sdd init --ai <agent>`、AI エージェント内の `/sdd.brief`、`/sdd.design` の順で共通統制文書、設計書束、UI 成果物束、シーケンス成果物束、テスト成果物束を起票できる。
2. `brief` 内の要件が変更されたとき、設計リーダーが `/sdd.design` を再実行し、`traceability.yaml` と `git diff` から影響文書を特定できる。
3. 実装エンジニアが AI エージェント内の `/sdd.tasks` を使い、設計書束、シーケンス図、テスト成果物、要件 ID に紐づく実装タスク兼実行台帳を取得できる。
4. 実装エンジニアが AI エージェント内の `/sdd.implement` を使い、指定 `TASK-xxx` のコード変更と検証結果を `tasks.md` に反映できる。

## 今後の詳細設計論点

- CLI の引数体系、対話モード、非対話モードの定義
- `brief`、設計書束、UI 成果物束のテンプレート詳細
- 共通統制文書のテンプレート詳細
- `sequence-flows/*.md` のテンプレート詳細と Mermaid 生成ルール
- `test-design.md` と `test-plan.md` のテンプレート詳細
- `traceability.yaml` の厳密なスキーマ
- 文書間整合チェックの実装方式
- 既存設計書更新時の差分反映ルール
- `tasks.md` の粒度、依存表現、優先順位付け方式
- テンプレート拡張ポイントと利用者カスタマイズ方法
- 将来的な非機能設計、権限制御設計、運用設計の追加方式
