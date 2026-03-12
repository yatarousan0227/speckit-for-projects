# Glossary

この用語集は、ToDo アプリで共有するドメイン用語と命名規約を定義する。

- Task:
  - ユーザーが所有する作業項目。タイトル、任意の説明、状態、任意の期限日を持つ。
- Open Task:
  - まだ完了しておらず、対応対象として残っている task。
- Completed Task:
  - 作業完了済みであり、状態が完了として永続化された task。
- Archived Task:
  - 通常の作業一覧からは除外されるが、履歴や復元のため保持される task。
- Due Date:
  - task を完了すべき目標日付。
- Reminder:
  - task の期限前または期限日に発行される通知。
- Task List:
  - フィルタ、ソート、件数集計付きで task を一覧表示する画面または集合。
- Filter:
  - 状態、期限範囲、キーワードなどにより表示対象を絞り込む条件。
- Authenticated User:
  - サインイン済みで、自身の task を管理する利用者。
- Ownership Check:
  - 実行中ユーザーが対象 task の参照・更新権限を持つかを server 側で確認する処理。
- Soft Delete:
  - レコードを即時物理削除せず、通常利用から隠す論理削除方式。

## Naming Conventions

- 単一ドメインオブジェクトには `task` を使う
- コレクション単位の route、module、directory には `tasks` を使う
- task 完了日時のフィールド名は `completedAt` を使う
- 期限日フィールド名は `dueDate` を使う
- アーカイブ機能を実装する場合の日時フィールド名は `archivedAt` を使う
