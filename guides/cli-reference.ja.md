# SpecKit for Projects CLI リファレンス

この文書は `sdd init`、`sdd check`、`sdd analyze` の詳細リファレンスです。あわせて、CLI ではなく agent command / skill として使う `sdd.clarify` の位置づけも説明します。挙動は現行実装に合わせています。

## 1. コマンド一覧

現行 CLI で直接実行するのは次の 3 つです。

- `sdd init`
- `sdd check`
- `sdd analyze`

`sdd.brief`、`sdd.clarify`、`sdd.common-design`、`sdd.design`、`sdd.tasks`、`sdd.implement` は、`init` で配置した agent 向け prompt / command / skill として使います。`sdd.analyze` だけは CLI サブコマンドとしても、agent 向け command としても提供されます。

## 2. `sdd init`

### 2.1 役割

`sdd init` は、対象ディレクトリへ次を導入します。

- `.specify/` 配下の管理対象 scaffold
- `briefs/`
- `designs/common_design/`
- `designs/specific_design/`
- 指定 agent 向けの command / prompt ファイル
- 必要に応じて `SKILL.md` 群

### 2.2 基本例

現在のリポジトリへ導入:

```bash
sdd init --here --ai codex --ai-skills
```

新しいディレクトリを作りつつ導入:

```bash
sdd init my-project --ai claude
```

`generic` agent へ独自出力先で導入:

```bash
sdd init --here --ai generic --ai-commands-dir .myagent/commands
```

### 2.3 引数とオプション

- `project_name`: 作成対象ディレクトリ。`--here` と併用不可
- `--here`: 現在ディレクトリへ導入する
- `--ai <name>`: agent 種別を指定する
- `--ai-commands-dir <path>`: `generic` 用の command 出力先
- `--ai-skills`: command 本文を `SKILL.md` としても配置する
- `--no-git`: `.git` がない場合の `git init` を行わない
- `--force`: 管理対象ファイルと agent 出力物を上書きする
- `--debug`: 追加診断を出す

### 2.4 オプション組み合わせの制約

- `--ai-skills` は `--ai` なしでは使えません
- `--ai-commands-dir` は `--ai generic` のときだけ使えます
- `--ai generic` では `--ai-commands-dir` が必須です
- `project_name` と `--here` は同時指定できません

### 2.5 実際に生成される主要パス

`sdd init` が管理対象として配置する主なファイルとディレクトリは次です。

```text
.specify/
├── glossary.md
├── conventions/README.md
├── project/
│   ├── tech-stack.md
│   ├── domain-map.md
│   ├── coding-rules.md
│   └── architecture-principles.md
├── templates/
│   ├── commands/
│   │   ├── brief.md
│   │   ├── analyze.md
│   │   ├── clarify.md
│   │   ├── common-design.md
│   │   ├── design.md
│   │   ├── tasks.md
│   │   └── implement.md
│   └── artifacts/
│       ├── brief.md
│       ├── common_design/
│       └── design/
briefs/
designs/
├── common_design/
│   ├── api/
│   ├── data/
│   ├── module/
│   └── ui/
└── specific_design/
```

補足:

- 現行 `init` が自動生成する project 文書は `tech-stack.md`、`domain-map.md`、`coding-rules.md`、`architecture-principles.md` です
- `src/speckit_for_projects/templates/project/design-system.md.j2` と `src/speckit_for_projects/templates/project/ui-storybook/` はテンプレートとしては存在します
- ただし、現行 `sdd init` の管理対象には含まれていないため、自動生成はされません
- これは `shadcn/ui` のような外部デザインシステム採用案件では、project 独自の UI 定義書や project 共通 Storybook が不要になりうるためです
- そのため `design-system.md` や `project/ui-storybook/` は現行の管理対象 scaffold ではありません

### 2.6 既存ファイルがある場合

`--force` なし:

- 管理対象ファイルが既に存在すれば保持されます
- agent 向け command / skill も既存なら保持されます

`--force` あり:

- 管理対象ファイルをテンプレートから再配置します
- agent 向け command / skill も上書きします

### 2.7 Git 初期化

対象ディレクトリに `.git` がない場合だけ `git init` を試みます。

- 既に `.git` があれば何もしません
- `--no-git` を付けると試行しません
- `git` コマンド自体がなくても、scaffold 導入自体は継続します

## 3. `sdd check`

### 3.1 役割

`sdd check` は次を確認します。

- 共有 scaffold の欠落
- 指定 agent 向け command ファイルの欠落
- 一部 agent で必要な CLI ランタイムの不足

### 3.2 基本例

```bash
sdd check --ai codex
```

`generic` の場合:

```bash
sdd check --ai generic --ai-commands-dir .myagent/commands
```

### 3.3 終了コード

- `0`: failure / warning なし
- `1`: warning あり、failure なし
- `2`: failure あり

### 3.4 `warning` と `failure` の違い

`warning` の例:

- `codex`、`claude`、`gemini` など CLI 前提 agent の実行バイナリがローカルにない

`failure` の例:

- `.specify/project/tech-stack.md` がない
- `.specify/templates/commands/design.md` がない
- `designs/common_design/module/` がない
- `--ai generic` なのに `--ai-commands-dir` を省略した
- 指定 agent 向け `sdd.design.md` などの command ファイルが出力先にない

### 3.5 `sdd check` が確認する共有 scaffold

主に次を検査します。

- `.specify/glossary.md`
- `.specify/project/tech-stack.md`
- `.specify/project/coding-rules.md`
- `.specify/project/architecture-principles.md`
- `.specify/project/domain-map.md`
- `.specify/templates/commands/*.md`
- `.specify/templates/artifacts/brief.md`
- `.specify/templates/artifacts/common_design/*.md`
- `.specify/templates/artifacts/design/` 配下の必須テンプレート
- `briefs/`
- `designs/common_design/` と各種サブディレクトリ
- `designs/specific_design/`

## 4. `sdd analyze`

### 4.1 役割

`sdd analyze` は `designs/specific_design/` 配下の生成済み bundle 整合を検査します。

責務分離:

- `sdd check`: scaffold と環境の確認
- `sdd analyze`: feature ごとの成果物 bundle の確認

### 4.2 基本例

```bash
sdd analyze 001-screened-application-portal
sdd analyze designs/specific_design/001-screened-application-portal
sdd analyze --all
```

### 4.3 引数とオプション

- `target`: `design-id` または bundle path
- `--all`: `designs/specific_design/` 配下を全件検査する
- `--debug`: brief path など追加情報も表示する

### 4.4 終了コード

- `0`: 対象 bundle がすべて整合
- `2`: issue あり、または入力不正

### 4.5 検査内容

- bundle 必須ファイルの有無
- `traceability.yaml` の構造と common design 参照整合
- `common-design-refs.yaml` の構造と shared design 解決可否
- brief がある場合の `REQ-*` coverage
- `tasks.md` が specific artifact または common design ref を参照しているか

### 4.6 入力制約

- `target` と `--all` は同時指定不可
- `target` 未指定かつ `--all` なしはエラー
- `--all` では `designs/specific_design/` が必要

## 5. `sdd.clarify`

### 5.1 位置づけ

`sdd.clarify` は CLI サブコマンドではありません。`init` で配置される agent 向け command / prompt / skill として使います。

### 5.2 役割

`brief` 作成直後や `design` 着手前に、次の曖昧さを整理します。

- `Domain Alignment`
- `Common Design References`
- 利用者、外部連携、境界条件、運用制約
- `REQ-*` の testable 性

### 5.3 初版の制約

- read-only で使う
- `briefs/*.md` や `designs/common_design/` を直接更新しない
- blocking 質問と non-blocking 提案を分けて返す

### 5.4 `sdd analyze` との違い

- `sdd.clarify`: 設計前の曖昧さを詰める
- `sdd.analyze`: 生成後の成果物 bundle を検査する

## 6. 対応 agent と出力先

主な agent 出力先は次のとおりです。

| agent | command / prompt 出力先 | 備考 |
| --- | --- | --- |
| `codex` | `.codex/prompts/` | slash command ではなく保存済み prompt 扱い |
| `claude` | `.claude/commands/` | frontmatter wrapper |
| `gemini` | `.gemini/commands/` | frontmatter wrapper |
| `copilot` | `.github/agents/` | frontmatter wrapper |
| `cursor-agent` | `.cursor/commands/` | frontmatter wrapper |
| `opencode` | `.opencode/command/` | frontmatter wrapper |
| `windsurf` | `.windsurf/workflows/` | frontmatter wrapper |
| `kiro-cli` | `.kiro/prompts/` | `kiro` は alias |
| `generic` | `--ai-commands-dir` 指定先 | plain wrapper |

`--ai-skills` を使うと、基本は `.agents/skills/` 配下へ `speckit-for-projects-*` skill が入ります。`codex` も skill 出力先は `.agents/skills/` です。

## 7. Codex での扱い

Codex だけ少し挙動が違います。

- `.codex/prompts/sdd.brief.md` などは custom slash command ではありません
- 保存済み prompt として開くか、本文を参照して実行します
- `--ai-skills` を付ければ `speckit-for-projects-analyze`、`speckit-for-projects-brief`、`speckit-for-projects-clarify` などの skill も導入できます

Codex で導入後に認識が悪い場合は、セッションを開き直す方が確実です。

## 8. 運用上のコマンド例

初期導入:

```bash
sdd init --here --ai codex --ai-skills
sdd check --ai codex
```

設計 bundle を検査したい:

```bash
sdd analyze 001-screened-application-portal
```

テンプレートだけ再配置したい:

```bash
sdd init --here --force
```

Codex 用 prompt / skill も含めて再配置したい:

```bash
sdd init --here --ai codex --ai-skills --force
sdd check --ai codex
```

`generic` agent の出力先を明示して確認したい:

```bash
sdd init --here --ai generic --ai-commands-dir .myagent/commands
sdd check --ai generic --ai-commands-dir .myagent/commands
sdd analyze --all
```

`clarify` は CLI から直接実行せず、生成された `sdd.clarify.md` または `speckit-for-projects-clarify` skill を agent 側で使います。

## 9. 関連ドキュメント

- [guides/manual.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/manual.ja.md)
- [guides/workflow-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/workflow-reference.ja.md)
- [guides/troubleshooting.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/troubleshooting.ja.md)
