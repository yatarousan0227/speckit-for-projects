# P2 `sdd.clarify` 実装計画

- 文書状態: Draft
- 作成日: 2026-03-13
- 参照元:
  - `docs/skill-expansion-plan.md`
  - `docs/p1-analyze-implementation-plan.md`
  - `src/speckit_for_projects/services/agent_template_installer.py`
  - `src/speckit_for_projects/services/agent_skill_installer.py`
  - `src/speckit_for_projects/services/environment_checker.py`
  - `src/speckit_for_projects/templates/commands/brief.md.j2`
  - `src/speckit_for_projects/templates/commands/design.md.j2`

## 1. 目的

この文書は、P2 として定義した `sdd.clarify` / `speckit-for-projects-clarify` の実装を、着手可能な粒度へ分解した詳細計画である。

初版の狙いは次の 3 点に集約する。

- `brief` 作成前後の曖昧さを固定観点で洗い出す command / skill を追加する
- `sdd.design` へ進む前に、Domain / Shared Design / Requirement 品質の詰めを標準フローへ組み込む
- `sdd init --ai <agent> --ai-skills` の配布対象へ `clarify` を加える

## 2. 背景

現状の `SpecKit for Projects` では、`brief` の構造自体は `sdd.brief` template で規定されているが、次の不足が残っている。

- 要件が testable かどうかを `brief` 作成時に詰める専用ステップがない
- `Domain Alignment` の曖昧さを、`sdd.design` 着手前に系統的に露出する仕組みがない
- `Common Design References` の不足、過剰参照、参照漏れを対話的に整理する導線がない
- 非機能要件、運用制約、境界条件、レビュー前提が `brief` の自由記述へ埋もれやすい

この結果、`brief` の完成度が低いまま `sdd.design` へ進み、後段で次のような手戻りが起きやすい。

- `domain-map.md` と `brief` の境界認識が食い違う
- `CD-*` が未整備または過剰で、`common-design-refs.yaml` が不安定になる
- `REQ-*` が抽象的すぎて `traceability.yaml` や `tasks.md` の割当がぶれる
- review 時に「要件不足」と「設計不足」が混線する

`sdd.clarify` は、この手戻りを `design` 前に局所化するための補助 command / skill と位置づける。

## 3. スコープ

### 3.1 初版スコープに含めるもの

- 新規 command template `sdd.clarify`
- skill `speckit-for-projects-clarify`
- `brief` 未作成の入力を整理する `pre-brief` モード
- 既存 `brief` を点検する `pre-design` モード
- 固定質問カテゴリに基づく `clarify report`
- `readiness` 判定と次アクション提示
- `init/check` 系 note, guide, README 更新
- golden / integration test 追加

### 3.2 初版スコープに含めないもの

- Python CLI サブコマンド `sdd clarify`
- 対話セッション状態の保存
- `brief` / `domain-map.md` / `common_design` の自動書き換え
- `REQ-*` の機械的 lint や scoring ロジック
- `analyze` 相当の bundle 構造検査
- 回答収集 UI やフォーム生成

## 4. 責務境界

### 4.1 `sdd.brief`

役割は維持する。

- 要求の正本 `briefs/<brief-id>.md` を作成または再生成する
- `REQ-*` の採番と section 構造を固定する
- `Domain Alignment` と `Common Design References` を記録する

### 4.2 `sdd.clarify`

新規追加する。

- 曖昧な要求、欠落前提、曖昧な shared design 依存を質問化する
- `design` 前に詰めるべき論点と、後回しにしてよい論点を分ける
- `REQ-*` を testable な表現へ寄せるための修正案を出す
- `brief` の readiness を `ready` / `needs-input` / `blocked` で判定する

初版では「問題を明確にし、質問と修正提案を返す」責務に留める。成果物ファイルの書き換えは行わない。

### 4.3 `sdd.design`

役割は維持する。

- clarify 済みの `brief` を specific design bundle へ落とす
- 不整合が残る場合は停止または差し戻しを行う

### 4.4 `sdd.analyze`

役割は維持する。

- 生成済み bundle の機械的整合性を検査する
- clarify が扱う「質問化」と analyze が扱う「検査」は明確に分ける

結論として、`brief` は要求の正本、`clarify` は要求の詰め、`design` は設計化、`analyze` は機械検査、という責務分離を固定する。

## 5. 入出力仕様

### 5.1 command の入力形

`sdd.clarify` は agent command / saved prompt / skill として提供し、ユーザー入力は自然言語 1 本に寄せる。

想定する入力例:

```text
sdd.clarify 001-application-portal
sdd.clarify briefs/001-application-portal.md
sdd.clarify 求人応募ポータルで、一次審査通過者だけが面接予約できるようにしたい
```

初版では追加オプションを導入しない。入力から mode を自動判定する。

### 5.2 mode 判定

初版では次の 2 mode を持つ。

- `pre-brief`
  - 入力が feature 説明、要件メモ、企画文などで、既存 `brief` を一意に解決できない場合
- `pre-design`
  - 入力が `brief-id` または `brief` path として一意に解決できる場合

判定ルール:

- `briefs/<brief-id>.md` が一意に解決できれば `pre-design`
- それ以外は `pre-brief`
- 複数 brief が候補になる場合は停止し、どれを対象にするか確認する

### 5.3 Required Context

`pre-brief` では少なくとも次を読む。

- `.specify/project/tech-stack.md`
- `.specify/project/architecture-principles.md`
- `.specify/project/domain-map.md`
- `.specify/glossary.md`
- `designs/common_design/`
- `.specify/templates/artifacts/brief.md`

`pre-design` では加えて次を読む。

- 対象 `brief`
- `brief` が参照する `CD-*` に対応する `designs/common_design/` 配下の文書

### 5.4 出力形式

出力は会話返答として返し、初版ではファイルを書かない。

section 順は固定する。

```markdown
# Clarify Report: <target>

- mode: pre-brief | pre-design
- readiness: ready | needs-input | blocked
- target: <freeform input or brief-id>

## Blocking Questions
1. <answer がないと design に進めない質問>

## Recommended Tightening
- <requirements / domain / shared design / constraints の修正提案>

## Candidate Requirement Rewrites
- <REQ-xxx or draft requirement> -> <testable wording>

## Proposed Next Step
- <brief を作る / brief を更新する / common_design を先に起こす / design へ進む>
```

### 5.5 readiness 判定

- `ready`
  - `design` に進むうえで blocking な曖昧さがない
- `needs-input`
  - 曖昧さはあるが、数個の回答で解消できる
- `blocked`
  - domain 競合、共有設計未整備、前提不足などにより `design` 着手が危険

### 5.6 質問カテゴリ

初版では質問カテゴリを固定する。

- `Domain Alignment`
- `Common Design References`
- `Actors / External Interfaces`
- `Scope / Boundary Conditions`
- `Non-Functional / Operations`
- `Requirement Testability`
- `Review / Approval Preconditions`

質問数は最大 5 件を推奨とし、blocking なものから優先する。非 blocking 項目は質問ではなく `Recommended Tightening` へ回す。

## 6. command template 仕様

`sdd.clarify` template には最低でも次を含める。

- 入力から `pre-brief` / `pre-design` を判定する手順
- `.specify/project/`、`.specify/glossary.md`、`designs/common_design/` の参照指示
- `pre-design` の場合は対象 `brief` と `CD-*` 解決を必須にする指示
- 不明点を invented assumption にせず、質問または block として返す指示
- `REQ-*` または draft requirements を testable な文へ言い換える指示
- `Blocking Questions` / `Recommended Tightening` / `Candidate Requirement Rewrites` / `Proposed Next Step` の固定出力

補足方針:

- `clarify` は analyze のような検査レポートではなく、対話的な問い直しを主眼に置く
- `clarify` は `brief` の代替ではなく、`brief` の品質を上げる前段または中間段階であることを明記する
- `pre-design` では `brief` の全文再生成を指示しない

## 7. 実装方針

### 7.1 service 再利用方針

初版では新規 Python service を作らず、shared command template と installer の追加で実現する。

再利用する既存資産:

- `AgentTemplateInstaller` の command 配布モデル
- `AgentSkillInstaller` の skill 派生生成
- `EnvironmentChecker._codex_note()` のスキル案内
- `brief` / `design` template にすでに入っている `Domain Alignment` と `Common Design References` の構造

### 7.2 Python コード変更方針

初版の Python 実装変更は最小限に留める。

- `COMMAND_SPECS` に `sdd.clarify` を追加する
- Codex 向け note の skill 一覧へ `speckit-for-projects-clarify` を追加する
- `check/init` の期待値とテストを更新する

新規 CLI サブコマンドや parser helper は導入しない。

### 7.3 配布方針

`clarify` は既存 command と同じ配布モデルに乗せる。

- shared command template: `.specify/templates/commands/clarify.md`
- agent command files:
  - `.codex/prompts/sdd.clarify.md`
  - `.claude/commands/sdd.clarify.md`
  - generic agent 配置先の `sdd.clarify.md`
- skill:
  - `.agents/skills/speckit-for-projects-clarify/SKILL.md`

## 8. 変更対象

### 8.1 コード

- `src/speckit_for_projects/services/agent_template_installer.py`
- `src/speckit_for_projects/services/environment_checker.py`
- `src/speckit_for_projects/services/agent_skill_installer.py`
  - 直接ロジック変更は想定しないが、`COMMAND_SPECS` 追加の影響を受ける

### 8.2 テンプレート

- `src/speckit_for_projects/templates/commands/clarify.md.j2`

### 8.3 テスト

- `tests/integration/test_cli_init.py`
- `tests/golden/test_scaffold_golden.py`
- `tests/golden/expected/shared/commands/clarify.md`
- `tests/golden/expected/agents/codex/sdd.clarify.md`
- `tests/golden/expected/agents/generic/sdd.clarify.md`
- `tests/golden/expected/agents/claude/sdd.clarify.md`
- `tests/golden/expected/skills/speckit-for-projects-clarify/SKILL.md`

### 8.4 ドキュメント

- `README.md`
- `README.ja.md`
- `guides/workflow-reference.ja.md`
- `guides/cli-reference.ja.md`
- `guides/tutorial.ja.md`
- `guides/manual.ja.md`

## 9. テスト方針

### 9.1 unit test

初版では unit test の追加は必須としない。`clarify` の中心価値は command template 配布と文面固定化にあるため、挙動担保は golden / integration を主に使う。

### 9.2 integration test

追加すべき観点:

- `sdd init --ai codex --ai-skills` で `sdd.clarify` と `speckit-for-projects-clarify` が配布される
- `sdd init --ai generic --ai-commands-dir ...` で `sdd.clarify.md` が出力される
- `kiro` など alias 系でも `clarify` prompt / skill が配置される

### 9.3 golden test

追加すべき観点:

- shared command template の本文が固定される
- Codex / generic / Claude 向け wrapper 結果が固定される
- skill wrapper 結果が固定される

### 9.4 E2E

初版では専用 E2E は必須にしない。理由は次の通り。

- `clarify` に CLI 実行主体がない
- command 実行結果は LLM 依存で deterministic な自動検証が難しい
- 初版の品質担保点は配布と文面で十分である

## 10. 実装タスク分解

### 10.1 Step 1: shared command template を追加

- `clarify.md.j2` を新規追加する
- mode 判定、Required Context、固定出力、停止条件を明記する
- `brief` / `design` の責務を侵食しない文面へ調整する

### 10.2 Step 2: installer の配布対象へ追加

- `COMMAND_SPECS` に `sdd.clarify` を追加する
- `description` と `skill_name` を既存命名規則へ合わせる
- Codex note の skill 一覧を更新する

### 10.3 Step 3: golden fixture を追加

- shared / codex / generic / claude / skill の expected ファイルを追加する
- 既存 fixture 配列の期待件数を更新する

### 10.4 Step 4: integration test を更新

- `test_cli_init.py` の `init` 成功ケースへ `clarify` を追加する
- `check` 系の note 文言が `clarify` 追加後も成立することを確認する

### 10.5 Step 5: 利用者向け文書を更新

- 標準フローを `brief -> clarify -> common-design/design` 前提へ更新する
- `clarify` が optional だが推奨ステップであることを説明する
- `analyze` との責務差分を guide に明記する

## 11. 受け入れ条件

- `sdd init --ai codex --ai-skills` で `sdd.clarify` と `speckit-for-projects-clarify` が配布される
- `clarify` template が `pre-brief` と `pre-design` の 2 mode を扱える
- `Domain Alignment` と `Common Design References` の確認が必須観点として含まれる
- `REQ-*` の testable 化を確認項目に含む
- blocking 質問と non-blocking 提案が分離されている
- 初版が read-only であることが template と guide に明記される
- golden / integration test が追加される

## 12. 将来拡張メモ

初版の外に置くが、次段階では検討価値がある。

- 回答を受けて `brief` 差分案を生成する `apply` mode
- `REQ-*` の曖昧表現辞書や lint helper の導入
- `domain-map.md` や `common_design` 不足を機械検知する補助 service
- `checklist` と連動した review packet 生成

## 13. タスクリスト

### Phase A: command template 設計

- [x] A101 `src/speckit_for_projects/templates/commands/clarify.md.j2` を追加する
- [x] A102 `pre-brief` と `pre-design` の mode 判定手順を command 本文へ明記する
- [x] A103 `Blocking Questions` / `Recommended Tightening` / `Candidate Requirement Rewrites` / `Proposed Next Step` の固定出力を定義する
- [x] A104 `Domain Alignment` / `Common Design References` / `Requirement Testability` を必須確認観点として埋め込む
- [x] A105 read-only 初版であることと、`brief` / `design` の責務境界を command 本文へ明記する

完了条件:

- [x] AC101 `clarify.md.j2` 単体で `pre-brief` / `pre-design` の両方を説明できる
- [x] AC102 出力 section と停止条件が template 内で一意に読める

### Phase B: command / skill 配布

- [x] B201 `src/speckit_for_projects/services/agent_template_installer.py` の `COMMAND_SPECS` に `sdd.clarify` を追加する
- [x] B202 `description`、`template_name`、`source_name`、`skill_name` を既存命名規則に合わせて定義する
- [x] B203 `src/speckit_for_projects/services/environment_checker.py` の Codex note に `speckit-for-projects-clarify` を追加する
- [x] B204 `sdd init --ai <agent> --ai-skills` の配布結果に `clarify` が含まれる前提で期待値を見直す

完了条件:

- [x] BC201 `.codex/prompts/sdd.clarify.md` が生成対象になる
- [x] BC202 `.agents/skills/speckit-for-projects-clarify/SKILL.md` が生成対象になる
- [x] BC203 generic / claude / kiro 系でも `sdd.clarify.md` または対応 skill が生成対象になる

### Phase C: golden fixture 整備

- [x] C301 `tests/golden/expected/shared/commands/clarify.md` を追加する
- [x] C302 `tests/golden/expected/agents/codex/sdd.clarify.md` を追加する
- [x] C303 `tests/golden/expected/agents/generic/sdd.clarify.md` を追加する
- [x] C304 `tests/golden/expected/agents/claude/sdd.clarify.md` を追加する
- [x] C305 `tests/golden/expected/skills/speckit-for-projects-clarify/SKILL.md` を追加する
- [x] C306 `tests/golden/test_scaffold_golden.py` の fixture 一覧を `clarify` 追加後へ更新する

完了条件:

- [x] CC301 shared / agent / skill すべての expected fixture が揃う
- [x] CC302 `clarify` 追加後も golden 比較対象の件数と配置先が一貫している

### Phase D: integration test 整備

- [x] D401 `tests/integration/test_cli_init.py` の Codex 初期化ケースへ `sdd.clarify` と `speckit-for-projects-clarify` の生成確認を追加する
- [x] D402 generic 初期化ケースへ `sdd.clarify.md` の生成確認を追加する
- [x] D403 `kiro` alias 初期化ケースへ `clarify` prompt / skill の生成確認を追加する
- [x] D404 既存ファイル保持と `--force` 上書きの挙動が `clarify` 追加後も崩れないことを確認する
- [x] D405 必要なら `check` 系 integration test の command file 期待値を更新する

完了条件:

- [x] DC401 `uv run pytest tests/integration/test_cli_init.py` が通る
- [x] DC402 `clarify` 追加で既存 init 系ケースが壊れない

### Phase E: ドキュメント反映

- [x] E501 `README.md` に `sdd.clarify` の位置づけを追加する
- [x] E502 `README.ja.md` に `sdd.clarify` の位置づけを追加する
- [x] E503 `guides/workflow-reference.ja.md` の標準フローへ `clarify` を反映する
- [x] E504 `guides/cli-reference.ja.md` に「CLI ではなく agent command / skill として使う」ことを追記する
- [x] E505 `guides/tutorial.ja.md` に `brief` 前後で `clarify` を使う例を追加する
- [x] E506 `guides/manual.ja.md` に `analyze` との責務差分を追記する

完了条件:

- [x] EC501 `clarify` の利用タイミングが user-facing docs で一貫する
- [x] EC502 `brief` / `clarify` / `design` / `analyze` の責務差分が説明される

## 14. 実装順序の推奨

1. Phase A: command template 設計
2. Phase B: command / skill 配布
3. Phase C: golden fixture 整備
4. Phase D: integration test 整備
5. Phase E: ドキュメント反映

この順序にする理由は、`clarify` は CLI ロジックよりも template 契約が先に固定されるべき機能であり、配布・golden・guide のすべてがその本文を正本として参照するためである。
