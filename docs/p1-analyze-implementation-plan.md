# P1 `sdd.analyze` 実装計画

- 文書状態: Draft
- 作成日: 2026-03-12
- 参照元:
  - `docs/skill-expansion-plan.md`
  - `src/speckit_for_projects/services/consistency_checker.py`
  - `src/speckit_for_projects/services/agent_template_installer.py`
  - `src/speckit_for_projects/commands/check.py`

## 1. 目的

この文書は、P1 として定義した `sdd.analyze` / `speckit-for-projects-analyze` の実装を、着手可能な粒度へ分解した詳細計画である。

初版の狙いは次の 3 点に集約する。

- 既存の `validate_design_bundle()` を CLI と AI workflow から呼べるようにする
- `sdd check` とは別責務の成果物整合検査コマンドを追加する
- `sdd init --ai <agent> --ai-skills` の配布対象へ `analyze` を加える

## 2. 背景

現状の `SpecKit for Projects` には、specific design bundle の整合検査ロジックがすでに存在する。

- `validate_design_bundle()`
- `ensure_valid_design_bundle()`

ただし、それらは内部 service と unit test / e2e test からしか使われておらず、利用者が直接使う導線がない。

現状の不足は次の通り。

- CLI から bundle 整合検査を実行できない
- `sdd init` で配布される command / skill に analyze がない
- `README` と workflow guide に analyze ステップが存在しない
- Codex 向け note でも analyze が案内されない

このため、設計生成後に `traceability.yaml` や `tasks.md` の整合性を機械的に再検査する運用が、実装としては存在していても UX 上は成立していない。

## 3. スコープ

### 3.1 初版スコープに含めるもの

- 新規 CLI コマンド `sdd analyze`
- command template `sdd.analyze`
- skill `speckit-for-projects-analyze`
- bundle 単体検査
- `designs/specific_design/` 全件一括検査
- `validate_design_bundle()` の結果を人間が読める形式へ整形
- `init/check` 系の note, guide, README 更新
- golden / integration / e2e test 追加

### 3.2 初版スコープに含めないもの

- `sdd check` への `--bundle` / `--all-designs` 統合
- issue の自動修正
- `brief` 単体検査専用コマンド
- `common_design` 変更影響範囲の逆引き
- warning と failure の高度な重要度分類

## 4. 責務境界

### 4.1 `sdd check`

役割は維持する。

- shared scaffold の存在確認
- agent command file の配置確認
- agent runtime の存在確認

### 4.2 `sdd analyze`

新規追加する。

- `brief` と `specific_design` の対応確認
- `traceability.yaml` の構造検査
- `tasks.md` の requirement coverage 検査
- `common-design-refs.yaml` と `designs/common_design/` の整合検査
- bundle 構造違反の検査

結論として、`check` は環境と scaffold、`analyze` は成果物 bundle の整合、という責務分離を固定する。

## 5. CLI 仕様

### 5.1 コマンド形

初版では次を採用する。

```bash
sdd analyze <design-id-or-path>
sdd analyze --all
```

`<design-id-or-path>` は次のどちらでも受け付ける。

- `001-feature-slug`
- `designs/specific_design/001-feature-slug`

### 5.2 オプション

初版では最小限に絞る。

- `target`: 引数。`design-id` または bundle path
- `--all`: `designs/specific_design/` 配下の全 bundle を対象にする
- `--debug`: 追加情報を表示する

### 5.3 引数バリデーション

- `target` と `--all` は同時指定不可
- `target` 未指定かつ `--all` なしはエラー
- `target` が存在しない path かつ `design-id` としても解決できない場合は failure
- `designs/specific_design/` が存在しない場合、`--all` は failure

### 5.4 終了コード

- `0`: 対象 bundle すべて整合
- `2`: 1 件以上の bundle に issue あり、または入力不正

初版では `warning` 専用終了コードは導入しない。現行 `validate_design_bundle()` が返す issue は、すべて failure とみなす。

## 6. 出力仕様

### 6.1 単体検査出力

出力は bundle ごとの table またはセクション形式とし、最低でも次を含める。

- 対象 bundle path
- `success` または `failure`
- issue category ごとの件数
- issue 詳細一覧

issue category は `BundleValidationResult` に合わせて次を表示する。

- `missing_files`
- `missing_requirements`
- `uncovered_task_requirements`
- `invalid_traceability_entries`
- `invalid_common_design_entries`
- `invalid_structure_entries`

### 6.2 全件検査出力

全件検査では次を含める。

- 検査件数
- success 件数
- failure 件数
- failure bundle 一覧

### 6.3 表示方針

- `rich` を継続利用する
- summary と detail を分ける
- エラー文言の source of truth は既存 service の issue message を尊重する
- CLI 層では issue を再解釈せず、分類と表示のみを担当する

## 7. 実装方針

### 7.1 service 再利用方針

`validate_design_bundle()` はそのまま再利用する。

追加で必要になるのは次の補助のみとする。

- `design-id` から bundle path を解決する helper
- `designs/specific_design/` 配下の bundle 一覧を返す helper
- `BundleValidationResult` を CLI 表示用に整形する helper

### 7.2 既存 service への変更方針

`consistency_checker.py` のロジックは原則として大きく変更しない。

変更が必要な場合でも、目的は次に限定する。

- analyze CLI から使いやすい helper の追加
- bundle path 解決や一覧取得の共通化

検査意味論の変更は P1 では最小限に留める。

### 7.3 command / skill 配布方針

`analyze` は既存の 5 本と同じ配布モデルに乗せる。

- shared command template: `.specify/templates/commands/analyze.md`
- agent command files:
  - `.codex/prompts/sdd.analyze.md`
  - `.claude/commands/sdd.analyze.md`
  - generic agent 配置先の `sdd.analyze.md`
- skill:
  - `.agents/skills/speckit-for-projects-analyze/SKILL.md`

## 8. 変更対象

### 8.1 コード

- `src/speckit_for_projects/commands/analyze.py`
- `src/speckit_for_projects/cli.py`
- `src/speckit_for_projects/services/consistency_checker.py`
- `src/speckit_for_projects/services/agent_template_installer.py`
- `src/speckit_for_projects/services/agent_skill_installer.py`
- `src/speckit_for_projects/services/environment_checker.py`
- `src/speckit_for_projects/foundations/app.py`
  - 必要なら help 文言調整のみ

### 8.2 テンプレート

- `src/speckit_for_projects/templates/commands/analyze.md.j2`

### 8.3 テスト

- `tests/integration/test_cli_analyze.py`
- `tests/integration/test_cli_check.py`
- `tests/golden/test_scaffold_golden.py`
- `tests/e2e/test_cli_workflow_e2e.py`
- `tests/golden/expected/shared/commands/analyze.md`
- `tests/golden/expected/agents/codex/sdd.analyze.md`
- `tests/golden/expected/agents/generic/sdd.analyze.md`
- `tests/golden/expected/agents/claude/sdd.analyze.md`
- `tests/golden/expected/skills/speckit-for-projects-analyze/SKILL.md`

### 8.4 ドキュメント

- `README.md`
- `README.ja.md`
- `guides/workflow-reference.ja.md`
- `guides/cli-reference.ja.md`
- `guides/tutorial.ja.md`

## 9. command template 仕様

`sdd.analyze` template には最低でも次を含める。

- 対象 bundle の解決手順
- `briefs/`, `.specify/project/`, `designs/common_design/`, `designs/specific_design/<design-id>/` の参照指示
- `traceability.yaml`, `common-design-refs.yaml`, `tasks.md` の整合確認指示
- 既存の `validate_design_bundle()` と同じ観点を人間向けに説明した validation checklist
- 出力形式:
  - success / failure
  - issue category
  - 修正優先順位

AI による analyze は、文書修正そのものではなく「何が壊れているかを報告する」責務を優先する。

## 10. テスト方針

### 10.1 unit test

既存の `tests/unit/test_consistency_checker.py` を主たる検査ロジックの担保として継続利用する。P1 では unit test の主対象を CLI ではなく helper 追加分に絞る。

### 10.2 integration test

追加すべき観点:

- `sdd analyze <design-id>` が success を返す
- `sdd analyze <design-id>` が failure を返し、issue を表示する
- `sdd analyze <path>` が path 指定を受け付ける
- `sdd analyze --all` が全 bundle を対象にする
- `target` と `--all` の同時指定がエラーになる
- target 未指定がエラーになる

### 10.3 golden test

追加すべき観点:

- shared command template として `analyze.md` が配布される
- Codex prompt wrapper に `sdd.analyze` が追加される
- generic / claude wrapper にも `sdd.analyze` が追加される
- `--ai-skills` 時に `speckit-for-projects-analyze` が生成される

### 10.4 e2e test

追加すべき観点:

- sample design bundle に対して `sdd analyze` が成功する
- 壊した sample bundle に対して failure が返る

## 11. 受け入れ条件

- `sdd analyze <design-id>` が実行できる
- `sdd analyze --all` が実行できる
- `validate_design_bundle()` の issue category が CLI 出力に反映される
- `sdd init --ai codex --ai-skills` で analyze skill が生成される
- `sdd init --ai generic --ai-commands-dir <path>` で analyze command が生成される
- Codex note に analyze を含む使い方が反映される
- workflow guide に analyze ステップが追加される
- integration / golden / e2e test が追加される

## 12. リスクと対策

### 12.1 `sdd check` との役割混同

リスク:

- 利用者が `check` と `analyze` の違いを理解しにくい

対策:

- README と CLI help に責務差分を明記する
- `check` は scaffold / environment、`analyze` は generated bundle consistency と固定表現にする

### 12.2 bundle 解決ルールの曖昧さ

リスク:

- `design-id` と path 指定が曖昧だと UX がぶれる

対策:

- `001-kebab-slug` は常に `designs/specific_design/<id>` として解決する
- path は存在する場合のみ path として扱う

### 12.3 既存 note / tests の期待値崩れ

リスク:

- 配布 command 数の増加で golden と integration の期待値が崩れる

対策:

- `COMMAND_SPECS` 更新時に test fixture 一式を同時更新する
- `EnvironmentChecker._codex_note()` の文言は analyze 追加込みで見直す

## 13. タスクリスト

### Phase A: CLI 基盤

- [ ] A101 `src/speckit_for_projects/commands/analyze.py` を追加し、`sdd analyze` の Typer command を実装する
- [ ] A102 `src/speckit_for_projects/cli.py` へ `analyze` command 登録を追加する
- [ ] A103 `target` / `--all` / `--debug` の option validation を実装する
- [ ] A104 `design-id` または path から bundle path を解決する helper を追加する
- [ ] A105 `designs/specific_design/` 配下の全 bundle 解決を実装する

完了条件:

- [ ] AC101 `sdd analyze <design-id>` が実行できる
- [ ] AC102 `sdd analyze --all` が実行できる

### Phase B: 出力整形

- [ ] B201 `BundleValidationResult` を CLI 表示へ変換する formatter を追加する
- [ ] B202 success / failure summary の表示を実装する
- [ ] B203 issue category ごとの detail 表示を実装する
- [ ] B204 全件検査時の summary 表示を実装する

完了条件:

- [ ] BC201 issue category ごとの件数と明細が表示される
- [ ] BC202 複数 bundle 検査時に失敗 bundle 一覧が表示される

### Phase C: command / skill 配布

- [ ] C301 `src/speckit_for_projects/templates/commands/analyze.md.j2` を追加する
- [ ] C302 `src/speckit_for_projects/services/agent_template_installer.py` の `COMMAND_SPECS` に `sdd.analyze` を追加する
- [ ] C303 `src/speckit_for_projects/services/agent_skill_installer.py` の配布対象へ analyze を追加する
- [ ] C304 `src/speckit_for_projects/services/environment_checker.py` の Codex note を analyze 含みへ更新する

完了条件:

- [ ] CC301 `sdd init --ai codex --ai-skills` で `speckit-for-projects-analyze` が生成される
- [ ] CC302 `.codex/prompts/sdd.analyze.md` が生成される
- [ ] CC303 generic / claude 系でも `sdd.analyze.md` が生成される

### Phase D: テスト

- [ ] D401 `tests/integration/test_cli_analyze.py` を追加する
- [ ] D402 `tests/integration/test_cli_check.py` の command file 期待値を analyze 追加後へ更新する
- [ ] D403 `tests/golden/test_scaffold_golden.py` を analyze 追加後へ更新する
- [ ] D404 `tests/golden/expected/` 配下の analyze fixture を追加する
- [ ] D405 `tests/e2e/test_cli_workflow_e2e.py` に analyze 実行ケースを追加する

完了条件:

- [ ] DC401 `uv run pytest tests/integration/test_cli_analyze.py` が通る
- [ ] DC402 `uv run pytest tests/golden/test_scaffold_golden.py` が通る
- [ ] DC403 `uv run pytest tests/e2e/test_cli_workflow_e2e.py` の analyze ケースが通る

### Phase E: ドキュメント

- [ ] E501 `README.md` に `sdd analyze` を追加する
- [ ] E502 `README.ja.md` に `sdd analyze` を追加する
- [ ] E503 `guides/workflow-reference.ja.md` に analyze ステップを追加する
- [ ] E504 `guides/cli-reference.ja.md` に analyze の CLI 仕様を追加する
- [ ] E505 `guides/tutorial.ja.md` に analyze 実行例を追加する

完了条件:

- [ ] EC501 `check` と `analyze` の責務差分が user-facing docs で説明される
- [ ] EC502 標準フローに analyze が追加される

## 14. 実装順序の推奨

1. Phase A: CLI 基盤
2. Phase B: 出力整形
3. Phase C: command / skill 配布
4. Phase D: テスト
5. Phase E: ドキュメント

この順序にする理由は、CLI 入口と出力仕様を先に固定しないと、template 文言、golden fixture、README 記述が確定しないためである。
