# Design System

この文書は、ToDo アプリにおけるローカル UI システムのルールを定義する。外部コンポーネントライブラリを前提にしないため、画面設計、実装、Storybook カバレッジの基準としてこの文書を使う。

## Component Taxonomy

- Foundations:
  - `surface`、`text`、`border`、`accent`、`success`、`warning`、`danger` の意味トークンを定義する
  - スペーシングは 4px スケールを基準にする
  - タイポグラフィはページタイトル、セクションタイトル、本文、補助テキスト、メタ情報で使い分ける
- Primitives:
  - `Button`、`TextField`、`TextArea`、`Checkbox`、`Select`、`Badge`、`Dialog`、`Toast`、`Card`、`EmptyState`
- Feature components:
  - `TaskComposer`、`TaskFilterBar`、`TaskList`、`TaskRow`、`TaskSummary`、`TaskEmptyState`
- Screens:
  - 画面は feature component と layout primitive を組み合わせて構成する
  - 画面固有スタイルを安易に増やさず、再利用価値があるものは primitive または feature component に昇格させる

## Atomic Design Structure

- コンポーネント階層は Atomic Design に従い、`atoms -> molecules -> organisms -> templates -> pages` とする。
- `atoms` は `Button`、`Checkbox`、`Badge` のような安全に再利用できる最小プリミティブを置く。
- `molecules` は少数の atom を組み合わせた再利用単位とし、`FieldWithHint` や `TaskStatusBadge` などを置く。
- `organisms` は `TaskComposer`、`TaskFilterBar`、`TaskList` のような機能単位のセクションを置く。
- `templates` は画面固有文言を埋め込まずにレイアウト骨格を定義する。
- `pages` は Storybook 上でレビューする具体画面状態を組み立てる。

ディレクトリ構成例:

```text
src/components/
  atoms/
    Button/
    Checkbox/
    Badge/
  molecules/
    FieldWithHint/
    TaskStatusBadge/
  organisms/
    TaskComposer/
    TaskFilterBar/
    TaskList/
  templates/
    TaskInboxTemplate/
  pages/
    TaskInboxPage/
```

## Composition Rules

- タスク状態は文言、アイコン、色の組み合わせで表現し、色だけで完了・期限超過・入力エラーを示さない。
- フォームは「ラベル、入力コントロール、補助テキスト、エラーテキスト」の順序を統一する。
- タスク行は操作密度を上げすぎず、完了トグル、主情報、期限日、補助アクションを視覚的にもキーボード操作上も一まとまりに保つ。
- Empty、Loading、Error 状態は場当たり的な inline markup ではなく、再利用可能な専用コンポーネントで表現する。

## Variant Rules

- `Button` は `primary`、`secondary`、`ghost`、`danger` を持つ。
- `Badge` は `neutral`、`success`、`warning` を持つ。
- 入力系コンポーネントは `default`、`error`、`disabled`、`readOnly` を持つ。
- 破壊的操作は `danger` variant か確認ダイアログのいずれかを必須とする。

## Accessibility Rules

- すべての操作可能コントロールは accessible name を持つ。
- すべての interactive primitive でキーボードフォーカスを視認できるようにする。
- Checkbox、Filter、Dialog の操作フローはポインティングデバイスなしでも完結できるようにする。
- モバイルレイアウトで使うコントロールの最小タッチターゲットは 44x44 CSS px とする。

## Storybook Expectations

- すべての primitive と再利用可能な feature component に最低 1 つの story を用意する。
- タスク向けコンポーネントの story では、該当する範囲で default、empty、validation-error、overdue-task 状態を含める。
- マージ前の目視確認は desktop 幅と狭い mobile 幅の両方で実施する。
- story の配置も Atomic Design のレイヤーに合わせ、reviewer が primitive から screen state まで追えるようにする。

Storybook 構成例:

```text
ui-storybook/
  stories/
    atoms/
      Button.stories.js
    molecules/
      FieldWithHint.stories.js
    organisms/
      TaskList.stories.js
    templates/
      TaskInboxTemplate.stories.js
    pages/
      TaskInboxPage.stories.js
```

story title 例:

- `Atoms/Button`
- `Molecules/FieldWithHint`
- `Organisms/TaskList`
- `Templates/TaskInboxTemplate`
- `Pages/TaskInboxPage`
