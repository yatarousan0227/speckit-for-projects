# SpecKit for Projects マニュアル

この文書は、`SpecKit for Projects` の日本語マニュアルの入口です。従来の 1 枚マニュアルを、目的別に読みやすく分割しています。

## まず押さえること

`SpecKit for Projects` は、CLI が全部を自動生成するツールではありません。役割は大きく 3 つです。

- `sdd init`: リポジトリへ共通 scaffold とエージェント向け prompt / command / skill を配置する
- `sdd check`: scaffold とエージェント実行前提が揃っているかを確認する
- `sdd analyze`: `specific_design` bundle の整合崩れを機械的に検査する

実際の `brief`、`clarify`、`common_design`、`specific_design`、`debug`、`tasks`、`implement`、`reflect` は、配置された command / prompt / skill を使って AI エージェント側で進めます。CLI はその前提整備と、生成済み bundle の整合確認を担当します。

## 情報モデル

`SpecKit for Projects` の情報は次の 3 層で分離します。

- `project`: リポジトリ全体で共有する標準
- `common_design`: 複数 brief / feature から参照される共有設計
- `specific_design`: 1 つの brief を具体化した feature 固有設計

この分離を崩すと、再生成時に設計の正本が曖昧になります。

## 読み方

目的別に次を参照してください。

- 初回導入から 1 周したい: [guides/tutorial.ja.md](tutorial.ja.md)
- CLI のオプションと挙動を確認したい: [guides/cli-reference.ja.md](cli-reference.ja.md)
- `brief -> clarify -> common-design -> design -> tasks -> analyze -> implement -> debug -> reflect` の流れを詳しく見たい: [guides/workflow-reference.ja.md](workflow-reference.ja.md)
- 生成されるファイルの意味と正本を確認したい: [guides/artifact-reference.ja.md](artifact-reference.ja.md)
- warning / failure や再生成事故の対処を知りたい: [guides/troubleshooting.ja.md](troubleshooting.ja.md)

## 最短フロー

```bash
sdd init --here --ai codex --ai-skills
sdd check --ai codex
```

その後の標準フローは次の順です。

1. `.specify/project/` と `.specify/glossary.md` を埋める
2. AI で `sdd.brief`
3. 必要なら AI で `sdd.clarify`
4. 必要なら AI で `sdd.common-design`
5. AI で `sdd.design`
6. AI で `sdd.tasks`
7. `sdd analyze <design-id>` または `sdd analyze --all`
8. 予定された task 実装は AI で `sdd.implement`
9. 不具合起因の修正は AI で `sdd.debug`
10. 手動コード修正後の文書追随は AI で `sdd.reflect`
11. `git diff` で差分確認

## どこを人が管理するか

主に人が正本として管理するのは次です。

- `.specify/project/tech-stack.md`
- `.specify/project/coding-rules.md`
- `.specify/project/architecture-principles.md`
- `.specify/project/domain-map.md`
- `.specify/glossary.md`
- `briefs/*.md`
- `designs/common_design/` 配下の共有設計

補足:

- project 層の UI 系文書として `src/speckit_for_projects/templates/project/design-system.md.j2` と `src/speckit_for_projects/templates/project/ui-storybook/` は存在します
- 既定では配備しませんが、`sdd init --project-design-system` を付けると管理対象 scaffold として配備します
- 理由は、`shadcn/ui` のような外部デザインシステムを採用する案件では project 独自の UI 定義書が不要になりうるためです
- そのため、現状の公式 scaffold として必須扱いしているのは上の project 文書群です

再生成前提で扱うのは主に次です。

- `designs/specific_design/<design-id>/`
- `designs/specific_design/<design-id>/tasks.md` の task 定義部

`sdd.clarify` は `brief` と shared design 前提の曖昧さを設計前に詰めるための step で、`sdd analyze` が主に検査するのは `designs/specific_design/<design-id>/common-design-refs.yaml`、`traceability.yaml`、`tasks.md` を含む bundle 全体です。`sdd.debug` は不具合修正と設計同期、`sdd.reflect` は手動コード差分を正として設計書と `tasks.md` を追随させる用途で使い分けます。

`tasks.md` のうち、実装実行後に更新されるのは execution ledger 部分だけです。詳細は [guides/workflow-reference.ja.md](workflow-reference.ja.md) を参照してください。

## 関連ドキュメント

- [README.ja.md](../README.ja.md)
- [examples/README.md](../examples/README.md)
- [examples/project-standards/todo-app-ja/README.md](../examples/project-standards/todo-app-ja/README.md)
