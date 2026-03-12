# SpecKit for Projects

[English version](README.md)

`SpecKit for Projects` は、SI 型開発向けの設計駆動ワークフローをリポジトリへ導入するための、軽量な CLI と scaffold テンプレート群です。CLI 自体は最小限に保ち、実際の文書生成はリポジトリ管理された prompt / skill / template を使って AI エージェント側で進めます。

## このツールの役割

`SpecKit for Projects` が担うのは主に次の 3 点です。

- 設計駆動開発に必要なディレクトリと雛形を初期配置する
- 使う AI エージェント向けの prompt / skill を配置する
- そのワークフローが成立する状態かを検査する

逆に、設計文書そのものを CLI が全部自動生成するわけではありません。`brief`、`common_design`、`specific_design`、`tasks`、`implement` は、`sdd init` で配置した agent 向け command / prompt / skill を使って進めます。

## 情報モデル

設計の正本は次の 3 層に分けます。

- `project`: リポジトリ全体で共有する標準
- `common_design`: 複数 feature で再利用する共有設計
- `specific_design`: 1 つの brief を具体化した feature 固有設計

この分離により、共有設計を feature ごとに重複定義せずに済みます。

## 現在の CLI 範囲

現行 CLI で直接実行するのは次の 3 つです。

- `sdd init`
- `sdd check`
- `sdd analyze`

その後の設計生成フローは、導入された agent 向け資材を使います。

- `sdd.analyze`
- `sdd.brief`
- `sdd.common-design`
- `sdd.design`
- `sdd.tasks`
- `sdd.implement`

責務分離は次のとおりです。

- `sdd check`: scaffold、ディレクトリ構成、agent 向け command、runtime 有無を確認する
- `sdd analyze`: `specific_design` 成果物 bundle の整合性を確認する

## インストール

Python 3.12 以上が必要です。開発・利用ともに `uv` を推奨します。

配布パッケージ名は `speckit-for-projects` です。CLI は引き続き `sdd`、内部 Python
module path は `speckit_for_projects` です。

ソースからそのまま実行する場合:

```bash
uv sync --dev
uv run sdd --help
```

ローカル checkout を CLI として入れる場合:

```bash
uv tool install --editable .
sdd --help
```

パッケージ名を指定して入れる場合:

```bash
uv tool install speckit-for-projects
sdd --help
```

サンプルの Storybook bundle も検証する場合は、Node.js と npm も必要です。

## 最短手順

Codex 向けに現在のリポジトリを初期化:

```bash
sdd init --here --ai codex --ai-skills
sdd check --ai codex
```

新規ディレクトリを作って初期化:

```bash
sdd init my-project --ai claude
```

generic agent を独自ディレクトリへ出力:

```bash
sdd init --here --ai generic --ai-commands-dir .myagent/commands
sdd check --ai generic --ai-commands-dir .myagent/commands
```

`designs/specific_design/<design-id>/tasks.md` まで作成したら、bundle 整合を確認します。

```bash
sdd analyze <design-id>
```

## 何が作られるか

`sdd init` で主に次が配置されます。

- `.specify/project/*.md`
- `.specify/glossary.md`
- `.specify/conventions/README.md`
- `.specify/templates/commands/*.md`
- `.specify/templates/artifacts/`
- `briefs/`
- `designs/common_design/`
- `designs/common_design/ui/`
- `designs/specific_design/`

運用の中で生成される代表成果物:

- `briefs/<brief-id>.md`
- `designs/common_design/api|data|module|ui/*.md`
- `designs/specific_design/<design-id>/overview.md`
- `designs/specific_design/<design-id>/common-design-refs.yaml`
- `designs/specific_design/<design-id>/traceability.yaml`
- `designs/specific_design/<design-id>/tasks.md`

## 標準フロー

1. `sdd init` を実行する
2. `sdd check` を実行する
3. `.specify/project/*.md` と `.specify/glossary.md` を埋める
4. `sdd.brief` で brief を作る
5. 必要な場合だけ `sdd.common-design` で共有設計を作る
6. `sdd.design` で feature 固有の設計束を作る
7. `sdd.tasks` で `tasks.md` を作る
8. `sdd analyze <design-id>` または `sdd analyze --all` で bundle 整合を確認する
9. `sdd.implement` で実装と execution ledger 更新を進める
10. 差分を確認する

## `sdd init` の実挙動

`sdd init` は、既存の管理対象ファイルを既定では上書きしません。

- 再実行しても既存の managed file は保持される
- 既存の agent command file は保持される
- 既存の skill も保持される
- `--force` を付けるとこれらを上書きする

また、対象ディレクトリに `.git` が無い場合は、`--no-git` を付けない限り `git init` を試みます。

## `sdd check` の実挙動

`sdd check` は次を確認します。

- `.specify/` 配下の共有 scaffold
- `briefs/` と `designs/` 配下の必須ディレクトリ
- `--ai` 指定時の agent 向け command file
- CLI 実行が必要な agent のローカル runtime 有無

終了コード:

- `0`: warning / failure なし
- `1`: warning のみ
- `2`: failure あり

## `sdd analyze` の実挙動

`sdd analyze` は `designs/specific_design/` 配下の生成済み bundle 整合を検査します。

- `sdd analyze <design-id>`: `design-id` 指定で 1 bundle を検査する
- `sdd analyze designs/specific_design/<design-id>`: path 指定で 1 bundle を検査する
- `sdd analyze --all`: `designs/specific_design/` 配下を全件検査する

主に次を確認します。

- bundle 内の必須ファイル
- `traceability.yaml` の構造と参照整合
- `tasks.md` の requirement coverage
- `common-design-refs.yaml` の構造と参照解決
- 対応する brief がある場合の要件・共有設計参照の一致

終了コード:

- `0`: 対象 bundle がすべて整合
- `2`: 1 件以上の bundle に issue がある、または入力不正

## ディレクトリ構成

```text
.specify/
├── glossary.md
├── conventions/
├── project/
│   ├── tech-stack.md
│   ├── domain-map.md
│   ├── coding-rules.md
│   └── architecture-principles.md
└── templates/
    ├── commands/
    │   ├── analyze.md
    │   ├── brief.md
    │   ├── common-design.md
    │   ├── design.md
    │   ├── tasks.md
    │   └── implement.md
    └── artifacts/
        ├── brief.md
        ├── common_design/
        └── design/
briefs/
designs/
├── common_design/
│   ├── api/
│   ├── data/
│   ├── module/
│   └── ui/
└── specific_design/
    └── 001-example/
```

## このリポジトリ自体の構成

パッケージの正本と、このリポジトリの作業用ファイルは分けて見る必要があります。

- `src/speckit_for_projects/`: CLI 実装と検証ロジック
- `src/speckit_for_projects/templates/`: `sdd init` が使う Jinja テンプレートの正本
- `guides/`: 利用者向け運用ドキュメント
- `docs/`: このリポジトリ自体の実装メモや設計メモ
- `examples/`: サンプル成果物と project-standards 例
- `tests/`: unit / integration / golden / e2e テスト
- `.specify/`: このリポジトリ自身を初期化した作業用 scaffold
- `.codex/` と `.myagent/`: このリポジトリ内で生成された agent 向け prompt 出力

重要:

- skills の正本は個別の `src/.../skills/` にはありません
- `SKILL.md` は `.specify/templates/commands/` か、その元になる `src/speckit_for_projects/templates/commands/*.j2` から生成されます

また、`src/speckit_for_projects/templates/` には存在していても、現行 `sdd init` では配備しないテンプレートがあります。現時点では次が該当します。

- `src/speckit_for_projects/templates/project/design-system.md.j2`
- `src/speckit_for_projects/templates/project/ui-storybook/*`
- `api-design.md.j2`、`data-design.md.j2`、`module-design.md.j2` などの legacy specific-design template

これらはソースツリーにはありますが、現行 CLI の managed scaffold には含まれていません。

## サンプルとガイド

- [examples/README.md](examples/README.md)
- [guides/manual.ja.md](guides/manual.ja.md)
- [guides/tutorial.ja.md](guides/tutorial.ja.md)
- [guides/cli-reference.ja.md](guides/cli-reference.ja.md)
- [guides/workflow-reference.ja.md](guides/workflow-reference.ja.md)
- [guides/artifact-reference.ja.md](guides/artifact-reference.ja.md)
- [guides/troubleshooting.ja.md](guides/troubleshooting.ja.md)

## 対応 AI エージェント

現行実装で受け付ける `--ai` の値は次です。

- `agy`
- `amp`
- `auggie`
- `bob`
- `claude`
- `codebuddy`
- `codex`
- `copilot`
- `cursor-agent`
- `gemini`
- `generic`
- `kilocode`
- `kiro-cli`
- `opencode`
- `qodercli`
- `qwen`
- `roo`
- `shai`
- `vibe`
- `windsurf`

alias:

- `kiro` は `kiro-cli` として扱われる

代表的な command 出力先:

- `codex`: `.codex/prompts/`
- `claude`: `.claude/commands/`
- `gemini`: `.gemini/commands/`
- `copilot`: `.github/agents/`
- `cursor-agent`: `.cursor/commands/`
- `kiro-cli`: `.kiro/prompts/`
- `generic`: `--ai-commands-dir` で指定したパス

skill の出力先:

- `codex`: `.agents/skills/`
- それ以外の多くの agent: `<agent-folder>/skills/`

Codex 補足:

- `.codex/prompts/*.md` は slash command ではなく saved prompt
- `--ai-skills` を付けると `.agents/skills/` に Codex から見つけやすい skill も入る

skill 実装上の補足:

- `src/` 配下に skill ごとの独立ソースは無い
- 生成される `SKILL.md` は共有 command template を wrapper したもの

## 開発者向け

推奨チェック:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Storybook サンプルの build 確認例:

```bash
cd examples/screen-centric/designs/specific_design/001-screened-application-portal/ui-storybook
npm install
npm run build-storybook
```

## OSS 向けドキュメント

- [LICENSE](LICENSE)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
