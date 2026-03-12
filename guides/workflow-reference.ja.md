# SpecKit for Projects ワークフロー詳細

この文書は、`brief -> common-design -> design -> tasks -> implement` の流れと、各段階の責務境界を詳しく説明します。

## 1. 全体像

標準フローは次の順です。

1. `sdd init`
2. 共通標準を整備
3. `sdd check`
4. AI で `sdd.brief`
5. 必要なら AI で `sdd.common-design`
6. AI で `sdd.design`
7. AI で `sdd.tasks`
8. AI で `sdd.implement`
9. `git diff` とレビュー

重要なのは、各段階が別の正本を持つことです。

- `brief`: 何を満たすか
- `common_design`: 何を共有契約として再利用するか
- `specific_design`: その feature をどう設計するか
- `tasks`: 実装単位にどう分解するか
- `implement`: 実際に何を変えてどう検証したか

## 2. Step 0: 共通標準を整える

AI に設計生成を依頼する前に、最低でも次を埋めます。

- `.specify/project/tech-stack.md`
- `.specify/project/coding-rules.md`
- `.specify/project/architecture-principles.md`
- `.specify/project/domain-map.md`
- `.specify/glossary.md`

この層に書く内容:

- 採用技術と禁止技術
- 命名規約とレビュー規約
- レイヤ境界
- 業務ドメイン境界
- 用語定義

この層に書かない内容:

- ある 1 画面だけの入力項目
- ある 1 feature だけの sequence flow
- 個別タスクの実装順

## 3. Step 1: `brief`

### 3.1 役割

`brief` は要求の正本です。feature または initiative を 1 件ずつ扱います。

### 3.2 brief に入れるもの

- 背景
- 目的
- Scope In
- Scope Out
- 利用者 / 外部 actor
- 制約
- Domain Alignment
- Common Design References
- `REQ-001` 形式の要件

### 3.3 brief に入れすぎないもの

- 共有 API の詳細インターフェース
- 共有データモデルの正本
- 実装タスクの詳細分解
- テスト手順の具体化

### 3.4 運用の要点

- `brief-id` は `001-kebab-slug` 形式で採番します
- 要件は `REQ-001` から連番にします
- 共通設計に依存する場合だけ `CD-*` を書きます
- 共有設計がまだないなら `none` でも構いません

## 4. Step 2: `common-design`

### 4.1 役割

`common_design` は、複数 brief / specific design が再利用する共有契約の正本です。

対象は次の 4 種です。

- API
- Data
- Module
- UI

### 4.2 common_design に置くべきもの

- 複数 feature が共通利用する API 契約
- 複数 feature が参照するデータ定義
- 複数 feature で責務境界を共有する module 設計
- 複数 feature で安定して再利用する画面一覧や遷移ルール

### 4.3 common_design に置かないもの

- 1 feature だけに閉じた画面状態
- 実装 helper や util クラス
- feature 固有の test plan
- feature 固有の batch 事情

### 4.4 ID と配置先

- `CD-API-001-*` -> `designs/common_design/api/`
- `CD-DATA-001-*` -> `designs/common_design/data/`
- `CD-MOD-001-*` -> `designs/common_design/module/`
- `CD-UI-001-screen-catalog.md` -> `designs/common_design/ui/`
- `CD-UI-002-navigation-rules.md` -> `designs/common_design/ui/`

## 5. Step 3: `design`

### 5.1 役割

`specific_design` は、1 つの brief を feature 実装可能な設計束へ落とし込む段階です。

### 5.2 生成対象

最低限、次の成果物が揃います。

- `overview.md`
- `ui-storybook/README.md`
- `ui-storybook/package.json`
- `ui-storybook/.storybook/main.ts`
- `ui-storybook/.storybook/preview.ts`
- `ui-storybook/.storybook/preview.css`
- `ui-storybook/stories/SCR-*.stories.js`
- `ui-storybook/components/SCR-*.html`
- `ui-fields.yaml`
- `common-design-refs.yaml`
- `sequence-flows/core-flow.md`
- `batch-design.md`
- `test-design.md`
- `test-plan.md`
- `traceability.yaml`

### 5.3 `design` で必ず解決すべきこと

- brief の全要件を設計へ落とせているか
- `Domain Alignment` と `domain-map.md` が矛盾していないか
- brief に書かれた `CD-*` が実在し、一意に引けるか
- `traceability.yaml` で全 `REQ-*` がどの成果物へ落ちたか説明できるか

### 5.4 `traceability.yaml` の意味

`traceability.yaml` は、要件と設計成果物の対応表です。レビューではかなり重要です。

見る観点:

- 全 `REQ-*` が載っているか
- `primary_artifact` が妥当か
- `related_artifacts` に主要設計書が含まれるか
- `common_design_refs` が brief と一致するか
- `project_standards` に必要な標準文書が入っているか

### 5.5 `common-design-refs.yaml` の意味

これは「共有設計のコピー」ではありません。役割は次のとおりです。

- この feature がどの `CD-*` を使うか示す
- 使い方の feature 固有メモを残す
- `specific_design` から `common_design` を辿りやすくする

## 6. Step 4: `tasks`

### 6.1 役割

`tasks.md` は単なる TODO ではなく、再生成可能な実装台帳です。

### 6.2 task 定義に必須のもの

- `TASK-001` 形式の task ID
- `requirement_ids`
- `artifact_refs`
- `common_design_refs`
- `depends_on`
- `implementation_notes`

### 6.3 execution ledger に含まれるもの

- `Execution Status`
- `Checklist`
- `Implementation Log`
- `Changed Files`
- `Verification Results`

### 6.4 再生成時の扱い

`sdd.tasks` は task 定義を再生成しますが、同じ `TASK-xxx` に対しては execution ledger を保持する前提です。

逆に保持しないもの:

- 古い requirement 紐付け
- 古い artifact 参照
- 古い dependency 定義

task 自体が消えた場合は、既存履歴を `Archived Execution History` へ移す運用です。

## 7. Step 5: `implement`

### 7.1 役割

`implement` は、選んだ `TASK-xxx` だけを対象にコード変更と検証を行い、結果を `tasks.md` へ戻す段階です。

### 7.2 入力で明示すべきもの

- `design-id`
- 対象 `TASK-xxx`
- 再実行かどうか

### 7.3 更新してよい範囲

`tasks.md` では、原則として次だけを更新します。

- `#### Execution Status`
- `#### Checklist`
- `#### Implementation Log`
- `#### Changed Files`
- `#### Verification Results`

task 定義部は書き換えません。

### 7.4 terminal state

対象 task は最後に次のいずれかで終わるべきです。

- `status: done`
- `status: blocked`
- `status: in_progress`

`in_progress` は、ユーザーが途中停止を明示したときだけが自然です。

## 8. 再生成ポリシー

段階ごとの再生成方針は次です。

- `brief`: full-file overwrite
- `common-design`: 対象ファイルの full-file overwrite
- `design`: bundle 配下の managed artifact を full-file overwrite
- `tasks`: task 定義は再生成、execution ledger は保持
- `implement`: 選択 task の execution ledger だけ更新

### 8.1 手修正を残したいとき

設計束の生成物へ直接ルールを書き足すのは弱い運用です。残したいなら、次のいずれかへ戻します。

- `.specify/project/*.md`
- `.specify/glossary.md`
- `briefs/*.md`
- `designs/common_design/*.md`

### 8.2 差分確認の順番

1. `briefs/*.md`
2. `designs/common_design/`
3. `designs/specific_design/<design-id>/traceability.yaml`
4. `designs/specific_design/<design-id>/overview.md`
5. `designs/specific_design/<design-id>/tasks.md`
6. 実装コード

## 9. レビュー観点

### 9.1 brief レビュー

- Scope Out が明示されているか
- 要件がテスト可能か
- 共通設計依存が漏れていないか

### 9.2 design レビュー

- 要件漏れがないか
- 共有設計への参照が正しいか
- feature 固有設計が shared truth を再定義していないか

### 9.3 tasks レビュー

- 依存順が妥当か
- 各 task の設計根拠が明記されているか
- 実装不能な task 分割になっていないか

### 9.4 implement レビュー

- 変更ファイルが task と一致しているか
- 実施コマンドと結果が記録されているか
- 対象外 task を巻き込んでいないか

## 10. 関連ドキュメント

- [guides/cli-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/cli-reference.ja.md)
- [guides/artifact-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/artifact-reference.ja.md)
- [guides/troubleshooting.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/troubleshooting.ja.md)
