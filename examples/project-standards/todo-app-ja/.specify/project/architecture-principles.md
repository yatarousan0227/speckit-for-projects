# Architecture Principles

このファイルは、ToDo アプリのすべての設計束で参照するアーキテクチャ上の共通正本である。

## Required Principles

- 責務分離:
  - 表示責務は React コンポーネントに置く
  - アプリケーションの制御は Server Action または Route Handler に置く
  - 業務ルールは feature service に置く
  - 永続化責務は repository に置く
- 依存方向:
  - UI は feature のアプリケーションインターフェースに依存してよいが、repository 実装へ直接依存しない
  - feature service は repository と共通基盤へ依存してよい
  - repository は UI やリクエスト固有の描画コードへ依存しない
- Server First 原則:
  - task 一覧や詳細取得は、一貫性と状態管理簡素化に寄与するなら server rendering を優先する
  - client component は、操作性の高い UI 挙動が必要な箇所に限定する
- API 所有境界:
  - task ライフサイクルの振る舞いは `tasks` feature が責任を持つ
  - 認証の振る舞いは auth layer が責任を持つ
  - 期限通知を導入する場合、notification module を別責務とし、task repository に混在させない
- データ整合性:
  - task 状態の正本はデータベースとする
  - 完了状態は `status` や `completedAt` のような永続化済みフィールドから導出する
  - フィルタとソートの規則は決定的であり、feature design に明記する
- セキュリティと分離:
  - task の参照・更新は必ず認証済みユーザーにスコープする
  - 認可チェックは server で実施し、client だけに依存しない
- 変更戦略:
  - 早すぎる共通化より、明確な feature 境界を優先する
  - 共通モジュール化は、少なくとも 2 つ以上の具体的ユースケースが出てから行う
- 運用簡素性:
  - まずは 1 つのデプロイ単位と 1 つの主データベースを前提とする
  - queue、worker、イベント駆動は、測定可能な運用上の必要性が出た時点で導入する

## Integration Principles

- 外部メール配信は内部の notification interface 越しに利用する
- 監視・ログ基盤は infrastructure adapter に閉じ込め、差し替え可能に保つ
- サードパーティ SDK を core domain logic に直接混在させない

## Design Review Heuristics

- client 側だけで所有者チェックを済ませられる設計は不正とみなす
- 業務ルールが route handler、component、repository に分散し、正本が不明な設計は不正とみなす
- 同じ task 状態を表す永続化モデルが複数存在し、整合戦略がない設計は不正とみなす
