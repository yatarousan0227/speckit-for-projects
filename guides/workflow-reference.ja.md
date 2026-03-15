# SpecKit for Projects ワークフロー詳細

この文書は、`brief -> clarify -> common-design -> design -> tasks -> analyze -> implement -> debug -> reflect` の流れと、各段階の責務境界を詳しく説明します。

## 1. 全体像

標準フローは次の順です。

1. `sdd init`
2. 共通標準を整備
3. `sdd check`
4. AI で `sdd.brief`
5. 必要なら AI で `sdd.clarify`
6. 必要なら AI で `sdd.common-design`
7. AI で `sdd.design`
8. AI で `sdd.tasks`
9. `sdd analyze`
10. 予定された task 実装は AI で `sdd.implement`
11. 不具合起因の修正は AI で `sdd.debug`
12. 手動コード差分の文書追随は AI で `sdd.reflect`
13. `git diff` とレビュー

重要なのは、各段階が別の正本を持つことです。

- `brief`: 何を満たすか
- `clarify`: 何が曖昧で、設計前に何を確定すべきか
- `common_design`: 何を共有契約として再利用するか
- `specific_design`: その feature をどう設計するか
- `tasks`: 実装単位にどう分解するか
- `analyze`: 生成済み bundle に整合崩れがないか
- `implement`: 実際に何を変えてどう検証したか
- `debug`: 不具合修正と設計同期をどう完了させたか
- `reflect`: 手動コード差分へ設計書をどう追随させたか

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

## 4. Step 2: `clarify`

### 4.1 役割

`clarify` は、`brief` 作成直後または `design` 着手直前に、曖昧な要求や不足前提を質問化する段階です。

### 4.2 何を詰めるか

- `Domain Alignment` が `.specify/project/domain-map.md` と矛盾していないか
- `Common Design References` に不足や過剰参照がないか
- 利用者、外部連携、境界条件、運用制約が抜けていないか
- `REQ-*` が testable な文になっているか

### 4.3 出力の扱い

`clarify` の初版は read-only です。`briefs/*.md` や `designs/common_design/` を直接更新せず、次を返します。

- blocking な質問
- non-blocking な tightening 提案
- requirement wording の言い換え案
- 次に進むべき step

### 4.4 `analyze` との違い

- `clarify`: 設計前の曖昧さを質問化する
- `analyze`: 生成済み bundle の整合崩れを検査する

`clarify` は `brief` の代替ではなく、`design` 前の品質調整ステップです。

## 5. Step 3: `common-design`

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

## 6. Step 4: `design`

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

## 7. Step 5: `tasks`

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

## 8. Step 6: `analyze`

### 7.1 役割

`sdd analyze` は、生成済みの `specific_design` bundle が review 可能な状態かを機械的に再検査する段階です。

### 7.2 `sdd check` との違い

- `sdd check`: scaffold と agent 設定を見る
- `sdd analyze`: feature ごとの成果物 bundle 整合を見る

### 7.3 何を確認するか

- bundle 必須ファイルの有無
- `traceability.yaml` の構造と参照整合
- `tasks.md` が brief の `REQ-*` をカバーしているか
- `common-design-refs.yaml` の構造と shared design 解決可否
- brief にある `CD-*` が bundle へ反映されているか

### 7.4 実行タイミング

少なくとも次のタイミングで実行します。

- `sdd.design` の直後に bundle 構造を確認したいとき
- `sdd.tasks` の直後に requirement coverage まで含めて確認したいとき
- 複数 bundle の整合をまとめて再確認したいとき

### 7.5 基本例

```bash
sdd analyze 001-screened-application-portal
sdd analyze --all
```

## 9. Step 7: `implement`

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

## 10. Step 8: `debug`

### 10.1 役割

`debug` は不具合起因の作業を一連で扱う段階です。

- バグの再現確認または不具合シグナルの特定
- 必要なコード修正
- テストや検証コマンドの実行
- 影響した `specific_design`、`common_design`、`tasks.md` の同期

### 10.2 `implement` との違い

- `implement`: 既存 `TASK-xxx` を中心に予定作業を進める
- `debug`: バグ修正を起点に、必要なら task 定義の補強まで行う

### 10.3 更新境界

- `briefs/*.md` は更新しない
- `tasks.md` は execution ledger だけでなく task 定義の再生成や拡張が必要になることがある
- shared truth が変わった場合だけ `designs/common_design/` を更新する

## 11. Step 9: `reflect`

### 11.1 役割

`reflect` は current working tree diff を truth source として扱い、手動コード修正へ設計書と task 文書を追随させる段階です。

### 11.2 何を確認するか

- 変更コードがどの `design-id` に影響するか
- `specific_design` の記述が現行コードとずれていないか
- `common_design` の shared truth が変わっていないか
- `tasks.md` が差分を説明できる状態か

### 11.3 `debug` との違い

- `debug`: バグ修正そのものも担当する
- `reflect`: すでに存在する差分へ文書側を追随させる

## 12. 再生成ポリシー

段階ごとの再生成方針は次です。

- `brief`: full-file overwrite
- `common-design`: 対象ファイルの full-file overwrite
- `design`: bundle 配下の managed artifact を full-file overwrite
- `tasks`: task 定義は再生成、execution ledger は保持
- `implement`: 選択 task の execution ledger だけ更新
- `debug`: 必要なコード修正に加えて、影響文書と task 定義を同期
- `reflect`: current diff に合わせて設計書と task 文書を同期

### 12.1 手修正を残したいとき

設計束の生成物へ直接ルールを書き足すのは弱い運用です。残したいなら、次のいずれかへ戻します。

- `.specify/project/*.md`
- `.specify/glossary.md`
- `briefs/*.md`
- `designs/common_design/*.md`

### 12.2 差分確認の順番

1. `briefs/*.md`
2. `designs/common_design/`
3. `designs/specific_design/<design-id>/traceability.yaml`
4. `designs/specific_design/<design-id>/overview.md`
5. `designs/specific_design/<design-id>/tasks.md`
6. `sdd analyze` の failure detail
7. 実装コード

## 13. レビュー観点

### 13.1 brief レビュー

- Scope Out が明示されているか
- 要件がテスト可能か
- 共通設計依存が漏れていないか

### 13.2 design レビュー

- 要件漏れがないか
- 共有設計への参照が正しいか
- feature 固有設計が shared truth を再定義していないか

### 13.3 tasks レビュー

- 依存順が妥当か
- 各 task の設計根拠が明記されているか
- 実装不能な task 分割になっていないか

### 13.4 analyze レビュー

- failure category が妥当な場所に出ているか
- `traceability.yaml` と `tasks.md` の要件漏れがないか
- shared design 参照切れがないか

### 13.5 implement レビュー

- 変更ファイルが task と一致しているか
- 実施コマンドと結果が記録されているか
- 対象外 task を巻き込んでいないか

### 13.6 debug / reflect レビュー

- 設計書更新がコード差分を正しく説明しているか
- `tasks.md` に新しい実装経緯や修正経緯が残っているか
- `briefs/*.md` を不要に触っていないか

## 14. 関連ドキュメント

- [guides/cli-reference.ja.md](cli-reference.ja.md)
- [guides/artifact-reference.ja.md](artifact-reference.ja.md)
- [guides/troubleshooting.ja.md](troubleshooting.ja.md)
