# Tech Stack

この文書は、ToDo アプリで採用する正式なランタイム、フレームワーク、インフラ、外部サービスを定義する。

## Runtime

- 言語: アプリケーションコードは TypeScript 5.x
- ランタイム: Node.js 22 LTS
- パッケージマネージャー: pnpm 10
- ホスティング方式: Next.js ベースの単一 Web アプリを Vercel へデプロイ
- データベース: PostgreSQL 16
- ORM / スキーマ管理: Prisma
- 認証: NextAuth.js を利用し、メールアドレス認証または OAuth 連携をサポート

## Frontend

- フレームワーク: Next.js 15 App Router
- UI ライブラリ: React 19
- スタイリング: Tailwind CSS 4
- フォーム処理: React Hook Form
- 入力バリデーション: Zod
- 状態管理方針:
  - サーバー状態は Server Component または Route Handler 経由で取得する
  - ローカル UI 状態は Client Component 内に閉じる
  - 画面横断のクライアント状態は最小限にする

## Backend

- API 方式: Next.js Route Handlers と Server Actions
- 業務ロジック配置: `src/features/<feature>/server/`
- DB アクセス配置: `src/server/repositories/` 配下の Prisma リポジトリ
- バックグラウンド処理: 期限通知やクリーンアップの cron 実行は任意とし、リクエスト処理から分離する

## Quality And Operations

- ユニットテスト: Vitest
- UI / 結合テスト: React Testing Library
- E2E テスト: Playwright
- Lint: ESLint
- Format: Prettier
- エラー監視: Sentry
- 構造化ログ: Pino 互換の JSON ログ
- CI:
  - typecheck
  - lint
  - unit / integration test
  - Prisma migration 検証
  - 主要導線の Playwright smoke test

## External Services

- パスワード再設定や期限通知メール送信用のメール配信サービス
- 例外およびパフォーマンス監視用の Sentry
- デプロイ基盤としての Vercel

## Constraints

- スケールやドメイン複雑性が増すまでは、単一サービス構成を維持する
- ブラウザ対応は最新安定版の Chrome、Safari、Edge、Firefox を対象とする
- タスクの主要操作は、リアルタイム基盤なしで成立させる
