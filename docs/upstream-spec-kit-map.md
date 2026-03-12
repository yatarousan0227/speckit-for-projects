# spec-kit 流用マップ v1

- 文書状態: Draft
- 作成日: 2026-03-11
- 対象 upstream: `github/spec-kit`
- 参照コミット: `56095f06d2b4b6f29b92dc3f4421da59f66a840b`
- ライセンス: MIT

## 1. 目的

この文書は、`SpecKit for Projects` v1 で `spec-kit` から何を流用し、何を差し替えるかを固定するための upstream マップである。Phase 0 の完了条件として、この文書と実際のローカル配置が一致していることを要求する。

## 2. 取り込み方針

- 取り込み方式は選択的ベンダーとする。
- `spec-kit` の UX と配布モデルは継承するが、成果物モデルと command semantics は `SpecKit for Projects` 用に再設計する。
- upstream へのランタイム依存は持たない。
- `SpecKit for Projects` 側へ取り込んだコードは `foundations/` を中心に隔離し、ドメインロジックは `domain/` と `services/` へ置く。
- v1.1 では `agent parity`、runtime 検査、`--ai-skills` のみを追加で取り込む。
- `extension/catalog`、GitHub release fetch、`.vscode/settings.json` merge は deliberate divergence として維持する。

## 3. 流用対象一覧

| upstream パス | 用途 | local 配置先 | 取り込み区分 | 補足 |
| --- | --- | --- | --- | --- |
| `pyproject.toml` | CLI パッケージ構成、依存定義の参考 | `pyproject.toml` | 軽微修正 | パッケージ名、entrypoint、依存は `SpecKit for Projects` 用に変更 |
| `src/specify_cli/__init__.py` | CLI 骨格、`init/check` 実装、GitHub 取得処理の参考 | `src/speckit_for_projects/foundations/app.py` と `src/speckit_for_projects/cli.py` | 全面置換 | コマンド名、表示文言、AI 対応一覧は `SpecKit for Projects` 用に差し替える |
| `src/specify_cli/__init__.py` の `AI_ASSISTANT_ALIASES` / `check_tool` / `install_ai_skills` | agent alias、runtime 検査、skill 配布の参考 | `src/speckit_for_projects/foundations/app.py`, `src/speckit_for_projects/services/agent_runtime.py`, `src/speckit_for_projects/services/agent_skill_installer.py` | 軽微修正 | offline package 前提で移植し、network fetch は導入しない |
| `src/specify_cli/extensions.py` | extension 配布の参考 | `src/speckit_for_projects/foundations/scaffolding.py` | 軽微修正 | `SpecKit for Projects` の agent template 配布に合わせる |
| `templates/commands/*.md` | AI 向け command template 配布モデル | `src/speckit_for_projects/templates/commands/` | 全面置換 | `specify/plan/tasks` を `/sdd.brief` `/sdd.design` `/sdd.tasks` `/sdd.implement` に置換 |
| `templates/agent-file-template.md` | agent-specific command file のラッパ生成 | `src/speckit_for_projects/templates/agent-files/` | 軽微修正 | コマンド名と説明を `SpecKit for Projects` 用に変更 |
| `templates/checklist-template.md` | チェックリスト整形の参考 | `src/speckit_for_projects/templates/project/` または `src/speckit_for_projects/templates/commands/` | 参考実装 | 直接流用は必須ではない |
| `templates/vscode-settings.json` | エディタ連携設定の参考 | 必要に応じて `.specify/` 配下へ | 参考実装 | v1 では任意 |
| `tests/` 配下の fixture / golden test パターン | テスト構成の参考 | `tests/unit/`, `tests/integration/`, `tests/golden/` | 軽微修正 | 対象生成物を `SpecKit for Projects` 用に差し替える |
| `README.md` の `Supported AI Agents` と `init` オプション | `--ai` 対応一覧と CLI 引数の基準 | `docs/implementation-plan.md`, 実装コード | 無改変参照 | 現行サポート一覧を合わせる |

## 4. 再設計対象

以下は upstream から流用せず、`SpecKit for Projects` 固有実装とする。

- `/sdd.brief`, `/sdd.design`, `/sdd.tasks`, `/sdd.implement` の command semantics
- 設計書束、UI 成果物束、シーケンス成果物束、テスト成果物束のテンプレート
- `traceability.yaml` の構造
- `.specify/project/` 配下の共通統制文書
- `brief-id` / `design-id` の命名規約
- `brief` / `design` の full-file overwrite + `git diff` 前提の再生成運用
- `tasks.md` の execution ledger 保持再生成
- extension catalog / marketplace 連携
- GitHub release asset の取得と展開
- `.vscode/settings.json` の merge 処理
- `tabnine` agent の追加対応

## 5. ローカル構成対応

| `SpecKit for Projects` 側パス | 役割 | upstream との関係 |
| --- | --- | --- |
| `src/speckit_for_projects/foundations/` | `spec-kit` 由来の共通基盤受け皿 | 取り込み・軽微改変中心 |
| `src/speckit_for_projects/commands/` | `sdd init` と `sdd check` の CLI 実装 | upstream 骨格を参考に独自公開コマンド化 |
| `src/speckit_for_projects/templates/commands/` | `/sdd.brief`, `/sdd.design`, `/sdd.tasks`, `/sdd.implement` の command template | upstream `templates/commands` を全面置換 |
| `src/speckit_for_projects/templates/agent-files/` | agent-specific command file ラッパ | upstream `agent-file-template.md` を基に調整 |
| `src/speckit_for_projects/domain/` | `SpecKit for Projects` 固有の内部モデル | upstream 非依存 |
| `src/speckit_for_projects/services/` | 初期化、検査、コンテキスト組み立て、整合チェック | upstream 非依存または軽微流用 |

## 6. notice / attribution ルール

- `spec-kit` 由来コードを取り込む場合は、MIT License の著作権表示と許諾文を保持する。
- `SpecKit for Projects` リポジトリには upstream 由来であることを README または CONTRIBUTING 相当文書に明記する。
- 取り込みファイルに大きな改変を加えた場合でも、元ファイル由来である旨をコメントまたは関連文書で追跡できるようにする。
- upstream コミット SHA をこの文書で固定し、更新時は SHA を差し替える。

## 7. Phase 0 完了チェック

- `spec-kit` 取り込み元 SHA がこの文書に記録されている。
- 流用対象の local 配置先が作業実体と一致している。
- `foundations/` 配下へ隔離すべきコードが `domain/` や `services/` に混入していない。
- `templates/commands/` は `spec-kit` の command 配布モデルを継承しつつ、内容が `SpecKit for Projects` 用に置換されている。
- MIT attribution ルールが README または関連文書へ反映されている。
