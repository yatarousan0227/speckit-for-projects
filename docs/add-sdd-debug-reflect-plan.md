# Add `sdd.debug` And `sdd.reflect`

- 文書状態: Implemented Plan
- 作成日: 2026-03-15
- 対象: `SpecKit for Projects`

## 1. 目的

この文書は、既存の prompt / skill 配布機構へ `sdd.debug` と `sdd.reflect` を追加する実装計画を固定するための maintainer 向けメモである。

今回の追加は新しい Typer サブコマンドを増やすものではなく、`.specify/templates/commands/*.md` を正本とした agent prompt / saved prompt / `SKILL.md` の生成対象拡張として扱う。

## 2. 追加するコマンドの責務

### 2.1 `/sdd.debug`

`/sdd.debug` は不具合修正時の実行系コマンドとして扱う。

- `design-id` と `TASK-xxx` が明示されていればそれを優先して使う
- 明示が無ければ bug summary、changed paths、working tree diff から影響 bundle を推定する
- 必要なコード修正、テスト更新、検証実行を進める
- 修正結果に合わせて `designs/specific_design/`、`designs/common_design/`、`tasks.md` を更新する
- 既存 `tasks.md` に十分な task 定義が無ければ task 定義の再生成または拡張を許容する
- `briefs/*.md` は更新しない

### 2.2 `/sdd.reflect`

`/sdd.reflect` は開発者が手動で入れた code diff を設計文書へ反映する同期系コマンドとして扱う。

- truth source は current working tree diff
- 変更コードから影響する `designs/specific_design/`、`designs/common_design/`、`tasks.md` を解決する
- 文書更新が不足または不完全なら自動で補正する
- 複数 bundle にまたがる場合は全候補を更新対象にする
- task 定義が不足していれば report-only ではなく追加・再生成できる前提にする
- `briefs/*.md` は更新しない

## 3. 実装方針

- source of truth は既存どおり `src/speckit_for_projects/templates/commands/*.j2`
- `sdd init` が `.specify/templates/commands/*.md` へ配布できるよう `MANAGED_TEMPLATES` を更新する
- agent prompt 配布と skill 配布は `COMMAND_SPECS` 追加だけで既存 installer を再利用する
- Codex 向け note、README、golden、integration/e2e tests は新コマンド列挙へ追従させる

## 4. 変更対象

- `src/speckit_for_projects/templates/commands/debug.md.j2`
- `src/speckit_for_projects/templates/commands/reflect.md.j2`
- `src/speckit_for_projects/services/agent_template_installer.py`
- `src/speckit_for_projects/services/project_initializer.py`
- `src/speckit_for_projects/services/environment_checker.py`
- `.specify/templates/commands/debug.md`
- `.specify/templates/commands/reflect.md`
- `README.md`
- `README.ja.md`
- `tests/integration/`
- `tests/e2e/`
- `tests/golden/expected/`

## 5. 受け入れ条件

- `sdd init --here` で `.specify/templates/commands/debug.md` と `.specify/templates/commands/reflect.md` が生成される
- 各 agent 向け prompt wrapper に `sdd.debug.md` と `sdd.reflect.md` が生成される
- `--ai codex --ai-skills` で `speckit-for-projects-debug` と `speckit-for-projects-reflect` の `SKILL.md` が生成される
- `check` の Codex note に 2 つの新 skill 名が含まれる
- README 英日両方の command 一覧と workflow 説明が実装と一致する
- 既存の keep / force overwrite ルールは維持される

## 6. 非対象

- `sdd debug` / `sdd reflect` という Typer 実コマンドの追加
- `briefs/*.md` を自動更新する仕組み
- `sdd.analyze` や `sdd.check` の振る舞い変更
