# Skill Expansion Plan

- 文書状態: Draft
- 作成日: 2026-03-12
- 対象: `SpecKit for Projects`
- 比較対象: `github/spec-kit` README 2026-03-12 確認時点

## 1. 目的

この文書は、`spec-kit` の現行ワークフローと比較したときに `SpecKit for Projects` へ追加すべき skill / command / CLI 機能を整理し、実装順序と受け入れ条件を固定するための拡張計画である。

特に、既存実装にすでに存在する整合検査ロジックを AI ワークフローへ露出し、`brief -> common-design -> design -> tasks -> implement` の間に不足している補助ステップを補うことを目的とする。

## 2. 比較前提

2026-03-12 時点で確認した `spec-kit` の README では、標準コマンド群は次の構成になっている。

- Core Commands:
  - `/speckit.constitution`
  - `/speckit.specify`
  - `/speckit.plan`
  - `/speckit.tasks`
  - `/speckit.implement`
- Optional Commands:
  - `/speckit.clarify`
  - `/speckit.analyze`
  - `/speckit.checklist`

一方、`SpecKit for Projects` で AI 向けに明示的に配布しているのは次の 5 本である。

- `sdd.brief`
- `sdd.common-design`
- `sdd.design`
- `sdd.tasks`
- `sdd.implement`

現状の差分は、`SpecKit for Projects` が成果物モデルと生成テンプレートでは強い一方で、`spec-kit` が持つ「生成前後の曖昧さ除去」「成果物横断検査」「レビュー補助」の補助コマンドが薄い点にある。

## 3. 現状整理

### 3.1 すでに存在する実装資産

- `src/speckit_for_projects/services/consistency_checker.py`
  - `validate_design_bundle()`
  - `ensure_valid_design_bundle()`
  - `missing_shared_paths()`
- `src/speckit_for_projects/services/environment_checker.py`
  - shared scaffold と agent command 配置の検査
- `src/speckit_for_projects/commands/check.py`
  - `sdd check` の CLI 入口
- `src/speckit_for_projects/services/agent_template_installer.py`
  - AI 向け command / skill の配布定義

### 3.2 現状の不足

- `validate_design_bundle()` は存在するが、CLI から直接呼べない
- `validate_design_bundle()` は存在するが、skill としても露出していない
- `sdd check` は shared scaffold 検査中心で、specific design bundle の検査を扱わない
- `brief` 生成後に曖昧さを詰める専用ステップがない
- 設計文書レビューを補助する checklist 生成ステップがない
- `.specify/project/*.md` を AI 主導で整備する専用 skill がない
- `common_design` 変更時の影響範囲を洗う補助機能がない

## 4. 方針

- `spec-kit` のコマンド名と責務は参考にするが、そのまま互換を目指さない
- `SpecKit for Projects` では既存の成果物モデルに自然に接続できる責務へ寄せる
- まずは既存ロジックを再利用できる `analyze` 系から着手する
- CLI と skill の両方へ露出し、AI ワークフロー専用機能に閉じない
- 追加 skill の source of truth は既存方針どおり `src/speckit_for_projects/templates/commands/*.j2` とする

## 5. 追加候補と優先順位

### 5.1 P1: `sdd.analyze`

最優先候補。`spec-kit` の `/speckit.analyze` に最も近い位置づけであり、既存の `validate_design_bundle()` を土台にできる。

想定責務:

- `brief` と `specific_design` の対応を検査する
- `traceability.yaml` の構造と coverage を検査する
- `tasks.md` が requirement を十分にカバーしているか検査する
- `common-design-refs.yaml` と `designs/common_design/` の整合を検査する
- specific design bundle の構造違反を検査する
- 必要に応じて `designs/specific_design/` 全件を一括検査する

想定ユーザー体験:

- AI skill: `speckit-for-projects-analyze`
- saved prompt / command: `sdd.analyze`
- CLI: `sdd check --bundle <design-id>` または `sdd analyze <design-id>`

本計画では、責務分離を明確にするため新規コマンド `sdd analyze` を第一候補とする。`sdd check` に bundle 検査を足す案は補完的に扱う。

### 5.2 P2: `sdd.clarify`

`brief` の曖昧さや不足情報を、`design` に進む前に詰める補助 skill。

想定責務:

- `Domain Alignment` の曖昧さを質問化する
- `Common Design References` の不足や過剰参照を洗う
- 非機能要件、運用制約、境界条件、レビュー前提を整理する
- `REQ-*` を testable な文に言い換える

`SpecKit for Projects` では、`brief` の質が後続成果物へ直結するため、`clarify` の実務価値は高い。

### 5.3 P3: `sdd.checklist`

設計レビュー向けのチェックリスト生成 skill。`spec-kit` の `/speckit.checklist` に相当する。

想定責務:

- brief 完全性チェック
- design bundle 横断レビュー観点の列挙
- tasks の分解妥当性レビュー観点の列挙
- shared design 参照、traceability、domain boundary のレビュー観点を固定化する

`analyze` が機械的検査、`checklist` が人間レビュー補助、という役割分担を明確にする。

### 5.4 P4: `sdd.project-standards`

`.specify/project/*.md` と `.specify/glossary.md` を整備・更新する skill。`spec-kit` の `/speckit.constitution` をそのまま移植するのではなく、`SpecKit for Projects` の文書分割モデルへ合わせる。

想定責務:

- `tech-stack.md`
- `coding-rules.md`
- `architecture-principles.md`
- `domain-map.md`
- `glossary.md`

単一の `constitution.md` を導入するより、既存の project 標準文書群を正本として維持する方針を継続する。

### 5.5 P5: `sdd.impact`

`common_design` や project 標準変更時の影響範囲を洗う補助機能。これは `spec-kit` との単純 parity ではなく、`SpecKit for Projects` 固有価値として追加する候補である。

想定責務:

- `CD-*` を参照する `brief/design/tasks` の逆引き
- `domain-map.md` の変更により再レビューすべき brief / design の洗い出し
- 共有 API / Data / UI 変更時の再生成候補一覧の提示

## 6. 実装順序

### Phase 1: `sdd.analyze` を追加

実装対象:

- `src/speckit_for_projects/templates/commands/analyze.md.j2`
- `src/speckit_for_projects/services/agent_template_installer.py`
- `src/speckit_for_projects/services/agent_skill_installer.py`
- `src/speckit_for_projects/commands/`
- `src/speckit_for_projects/cli.py`
- `tests/golden/`
- `tests/integration/`
- `tests/e2e/`

主な作業:

- command / skill 定義を追加する
- bundle 単体検査と全件検査の CLI 入口を追加する
- `validate_design_bundle()` の結果を人間が読める形に整形する
- Codex 向け note や `sdd init --ai codex --ai-skills` の生成物へ反映する
- `README*` と guide に analyze の利用位置を反映する

### Phase 2: `sdd.clarify` を追加

主な作業:

- `brief` 前後の利用タイミングをガイドへ明記する
- `brief` の曖昧さを整理する prompt / skill を追加する
- 代表的な質問カテゴリを固定化する

### Phase 3: `sdd.checklist` を追加

主な作業:

- brief / design / tasks 別のレビュー観点テンプレートを定義する
- AI が生成する checklist の section 順を固定する
- analyze と checklist の責務境界を guide に明記する

### Phase 4: `sdd.project-standards` を追加

主な作業:

- `.specify/project/*.md` の更新 workflow を定義する
- `brief` 以前に使うべき前提 skill として位置づける
- constitution 相当の説明を docs へ追加する

### Phase 5: `sdd.impact` を追加

主な作業:

- `CD-*` 逆引きロジックを service 化する
- 変更差分から再レビュー対象を洗う CLI / skill 入口を検討する
- `common_design` と `specific_design` の接続を文書化する

## 7. `sdd.analyze` の詳細計画

### 7.1 目的

生成済みの specific design bundle と task ledger に対して、機械的に判定できる整合性を集中的に検査する。

### 7.2 最小スコープ

初版では次を対象にする。

- design bundle 必須ファイル存在確認
- `traceability.yaml` の shape 検査
- brief の `REQ-*` と traceability の coverage 検査
- `tasks.md` と requirement coverage の検査
- `common-design-refs.yaml` と brief の `CD-*` 整合検査
- `designs/common_design/` 上の実ファイル解決可否
- legacy artifact 混入検査

### 7.3 CLI 案

候補 A:

```bash
sdd analyze 001-feature-slug
sdd analyze designs/specific_design/001-feature-slug
sdd analyze --all
```

候補 B:

```bash
sdd check --bundle 001-feature-slug
sdd check --all-designs
```

推奨は候補 A とし、`sdd check` は shared scaffold 用、`sdd analyze` は成果物整合用、と責務を分ける。

### 7.4 skill 案

- skill 名: `speckit-for-projects-analyze`
- command 名: `sdd.analyze`
- 入力:
  - `design-id`
  - design bundle path
  - `--all` 相当の全件対象指定
- 出力:
  - `success` / `warning` / `failure`
  - issue category ごとの一覧
  - 可能なら修正順序の提案

### 7.5 期待される利用位置

標準フローを次へ更新する。

1. `sdd init`
2. 共通標準を整備
3. `sdd check`
4. AI で `sdd.brief`
5. 必要なら AI で `sdd.clarify`
6. 必要なら AI で `sdd.common-design`
7. AI で `sdd.design`
8. AI で `sdd.tasks`
9. AI または CLI で `sdd.analyze`
10. AI で `sdd.implement`
11. `git diff` とレビュー

## 8. 受け入れ条件

### 8.1 `sdd.analyze`

- `sdd init --ai codex --ai-skills` で `sdd.analyze` と `speckit-for-projects-analyze` が配布される
- `design-id` 指定で 1 bundle を検査できる
- 全 bundle 一括検査ができる
- `validate_design_bundle()` の各 issue category が CLI 出力へ反映される
- 終了コードが success / warning / failure を判別可能である
- golden test が追加される
- integration test で CLI 入口を確認する
- e2e でサンプル bundle を検査できる

### 8.2 `sdd.clarify`

- `brief` の曖昧さを詰める固定 section を持つ
- `Domain Alignment` と `Common Design References` の確認を必須観点に含む
- `REQ-*` の testable 化を確認項目に含む

### 8.3 `sdd.checklist`

- brief / design / tasks の少なくとも 3 種の checklist モードを持つ
- traceability と shared design 参照の観点を含む
- analyze の重複出力ではなく、人間レビュー観点へ寄せる

## 9. 非目標

今回の拡張計画では、次は初期スコープに含めない。

- `spec-kit` との command 互換性確保
- `constitution.md` 単独ファイルモデルへの移行
- LLM 内蔵型の自動文書生成 CLI
- GitHub release 取得や remote marketplace 連携
- shared design の自動再生成

## 10. 実装メモ

- source of truth は引き続き shared command template とし、checked-in skill を個別管理しない
- `sdd.analyze` の追加時に `EnvironmentChecker._codex_note()` の文言更新が必要になる
- `COMMAND_SPECS` 増加に伴い、golden fixture と `tests/integration/test_cli_init.py` の期待値更新が必要になる
- guide 類では `sdd check` と `sdd.analyze` の責務差分を明記する

## 11. 次アクション

実装着手時の最初の変更単位は次を推奨する。

1. `sdd.analyze` の command template を追加する
2. `COMMAND_SPECS` と skill installer の配布対象へ追加する
3. CLI 入口を追加する
4. `validate_design_bundle()` を流用した出力整形を追加する
5. golden / integration / e2e / docs を更新する
