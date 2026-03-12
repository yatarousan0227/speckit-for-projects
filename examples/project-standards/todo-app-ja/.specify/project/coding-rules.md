# Coding Rules

この文書は、ToDo アプリにおいて生成されるタスクと設計成果物が従うべき実装ルールを定義する。

## Required Rules

- 命名規約:
  - React コンポーネント名と型名は `PascalCase` を使う
  - 変数名、関数名、オブジェクトプロパティ名は `camelCase` を使う
  - ルートセグメントやコード外ファイル名は必要に応じて `kebab-case` を使う
  - ドメイン名は `task`, `taskList`, `dueDate`, `completedAt` を一貫して使う
- モジュール境界:
  - UI コンポーネントから Prisma を直接呼ばない
  - Route Handler と Server Action は feature 単位の server module へ業務ルールを委譲する
  - repository に表示ロジックを含めない
- バリデーション:
  - 外部入力は業務ロジック実行前に必ず Zod で検証する
  - フォームバリデーションルールは、可能な限り client と server で共通化する
- エラーハンドリング:
  - 想定された業務エラーは、ユーザー向け安全メッセージと安定したエラーコードを返す
  - 想定外エラーはリクエスト文脈付きで記録し、ユーザーには汎用メッセージを返す
  - 構造化ログなしに例外を握りつぶさない
- データ更新:
  - 作成、更新、完了、再オープン、削除の各操作では、認証済みユーザーが対象 task の所有者か必ず検証する
  - リトライが起こり得る書き込みは、可能な限り冪等にする
- ログと監視:
  - サーバー処理のログは構造化 JSON とする
  - エラーログには feature 名、action 名、取得可能なら user ID と task ID を含める
  - アクセストークン、パスワード、セッションクッキー生値などの秘匿情報はログに出さない
- レビュー方針:
  - Pull Request にはテストを付けるか、未実施理由を明記する
  - 生成物はマージ前に `git diff` で確認する
- テスト方針:
  - ドメインルールには unit test を付ける
  - Route Handler と Server Action には正常系 / 異常系の integration test を付ける
  - E2E では task 作成、完了切替、編集、フィルタ、削除を含める

## Preferred File Organization

- `src/app/` はルート入口とレイアウト連携を置く
- `src/features/tasks/` は task 固有の UI と server logic を置く
- `src/server/` は共通の server-only 基盤を置く
- `src/lib/` は feature 横断だがドメイン結合の低いユーティリティを置く

## Prohibited Shortcuts

- UI コンポーネントへ SQL を埋め込まない
- 明確な理由なしに client と server でバリデーションスキーマを重複定義しない
- task 永続化状態の正本を client component に持たせない
- リクエスト同期処理で十分な機能に対して、安易にバックグラウンドジョブを導入しない
