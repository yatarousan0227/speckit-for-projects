# SpecKit for Projects 成果物リファレンス

この文書は、`SpecKit for Projects` が扱うディレクトリと成果物の役割をまとめたリファレンスです。どこが正本で、誰が主に編集し、再生成時にどう扱うかを明確にします。

## 1. ルート構成

```text
.specify/
briefs/
designs/
```

役割は次のとおりです。

- `.specify/`: プロジェクト共通標準と生成テンプレート
- `briefs/`: 要求定義の起点
- `designs/common_design/`: 共有設計の正本
- `designs/specific_design/`: feature 固有設計束

## 2. `.specify/`

### 2.1 `.specify/project/`

プロジェクト共通標準の置き場です。

- `tech-stack.md`
- `coding-rules.md`
- `architecture-principles.md`
- `domain-map.md`

現行実装で `init` が自動配置するのは上の 4 文書です。

一方で、テンプレート資産としては次もリポジトリに存在します。

- `src/speckit_for_projects/templates/project/design-system.md.j2`
- `src/speckit_for_projects/templates/project/ui-storybook/`

ただし、これらは現行 `sdd init` / `sdd check` の managed scaffold には入っていません。`shadcn/ui` のような外部デザインシステム採用案件では project 独自の UI 定義書が不要になりうるため、任意扱いにしている project UI 定義です。

ここに書くべき内容:

- 採用技術、依存技術、実行基盤
- 命名、テスト、レビューの規則
- レイヤと責務の原則
- 業務ドメイン境界

ここに書かない方がよい内容:

- 1 feature 固有の画面項目
- 1 feature 固有のバッチ詳細
- 個別 task の実装ログ

UI に関する補足:

- project 全体の UI 原則を置く候補は `design-system.md`
- 共有 UI レビュー基盤を置く候補は `project/ui-storybook/`
- ただし外部デザインシステムをそのまま採用する案件では、これらを作らずに済むことがあります
- ただし現行運用で確実に存在する正本は `designs/common_design/ui/` と `designs/specific_design/<design-id>/ui-storybook/` です

### 2.2 `.specify/glossary.md`

用語の正本です。brief や design で用語が揺れるなら、まずここを直します。

### 2.3 `.specify/templates/commands/`

AI agent に渡す command 本文の共通ソースです。

- `brief.md`
- `common-design.md`
- `design.md`
- `tasks.md`
- `implement.md`

agent 別の `.codex/prompts/` や `.claude/commands/` は、ここを元に生成される配布先です。

### 2.4 `.specify/templates/artifacts/`

生成成果物の雛形です。

- `brief.md`
- `common_design/*.md`
- `design/overview.md`
- `design/ui-fields.yaml`
- `design/common-design-refs.yaml`
- `design/sequence-flows/core-flow.md`
- `design/batch-design.md`
- `design/test-design.md`
- `design/test-plan.md`
- `design/traceability.yaml`
- `design/tasks.md`
- `design/ui-storybook/`

## 3. `briefs/`

### 3.1 命名

- `001-kebab-slug.md`
- 例: `001-screened-application-portal.md`

### 3.2 役割

feature / initiative の要求定義です。

### 3.3 典型セクション

- `Background`
- `Goal`
- `Scope In`
- `Scope Out`
- `Users And External Actors`
- `Constraints`
- `Domain Alignment`
- `Common Design References`
- `Requirements`
- `Source References`

### 3.4 主な編集者

- 人間がレビューして正本管理する
- AI で初稿生成しても、そのまま最終正本にしない

## 4. `designs/common_design/`

### 4.1 `api/`

共有 API 契約の正本です。

代表的な内容:

- API の責務
- consumer / provider
- 入出力と制約
- versioning note

### 4.2 `data/`

共有データモデルの正本です。

代表的な内容:

- エンティティ
- 属性
- 関係
- 不変条件

### 4.3 `module/`

共有 module 境界の正本です。

代表的な内容:

- module の責務
- public interface
- collaboration rule
- non-responsibility

### 4.4 `ui/`

共有 UI ルールの正本です。

現行テンプレートが想定するのは主に次です。

- `CD-UI-001-screen-catalog.md`
- `CD-UI-002-navigation-rules.md`

これは feature ごとの画面詳細ではなく、複数 feature が再利用する画面一覧や標準遷移です。

## 5. `designs/specific_design/<design-id>/`

### 5.1 役割

1 つの brief を実装可能な設計束に落とした成果物群です。

### 5.2 必須成果物

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
- `tasks.md`

### 5.3 `overview.md`

feature 全体を俯瞰する中心文書です。

見るべき点:

- brief の目的と scope が反映されているか
- domain context が書かれているか
- shared design context が書かれているか
- primary flow が説明できるか

### 5.4 `ui-storybook/`

設計レビュー用の UI bundle です。`@storybook/html` を前提にしたテンプレートが入ります。

主な役割:

- 画面状態の視覚レビュー
- `SCR-*` 単位の story 管理
- HTML テンプレートの雛形共有

確認コマンド:

```bash
cd designs/specific_design/<design-id>/ui-storybook
npm install
npm run storybook
```

build 確認:

```bash
npm run build-storybook
```

### 5.5 `ui-fields.yaml`

画面ごとの項目定義です。

見るべき点:

- 入力 / 表示項目が story と整合しているか
- validation note が不足していないか
- 外部 API や data model とのマッピングが曖昧でないか

### 5.6 `common-design-refs.yaml`

この feature が依存する `CD-*` 一覧と使い方のメモです。共有設計そのものの正本ではありません。

### 5.7 `sequence-flows/core-flow.md`

主要な正常系または中核フローです。

見るべき点:

- actor
- system
- external dependency
- 分岐と失敗時の扱い

### 5.8 `batch-design.md`

非同期処理や batch がない場合でも、`not applicable` を含めて整理する想定です。

### 5.9 `test-design.md`

要件ごとのテスト観点をまとめます。`REQ-*` 単位の見落とし検出に使います。

### 5.10 `test-plan.md`

テストレベル、実行順、環境、責務分担をまとめます。`test-design.md` より運用寄りです。

### 5.11 `traceability.yaml`

要件と成果物の対応表です。要件漏れ確認の基準になります。

### 5.12 `tasks.md`

実装タスクと実行台帳です。設計レビューだけでなく、実装フェーズの証跡にもなります。

## 6. 誰がどこを触るか

人が正本としてレビューしやすい場所:

- `.specify/project/*.md`
- `.specify/glossary.md`
- `briefs/*.md`
- `designs/common_design/*.md`

AI に再生成させやすい場所:

- `designs/specific_design/<design-id>/overview.md`
- `designs/specific_design/<design-id>/ui-fields.yaml`
- `designs/specific_design/<design-id>/traceability.yaml`
- `designs/specific_design/<design-id>/tasks.md`

実装で更新される場所:

- アプリケーションコード
- テストコード
- `tasks.md` の execution ledger

## 7. 正本の戻し先

設計束で見つかった知見をどこへ戻すか迷ったら、次の基準で判断します。

- 複数 feature で共有するルールなら `.specify/project/`
- 複数 feature で共有する契約なら `designs/common_design/`
- その feature の要求そのものなら `briefs/`
- その feature の具体設計だけなら `designs/specific_design/`

## 8. 関連ドキュメント

- [guides/workflow-reference.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/workflow-reference.ja.md)
- [guides/troubleshooting.ja.md](/Users/iwasakishinya/Documents/hook/general_sdd/guides/troubleshooting.ja.md)
