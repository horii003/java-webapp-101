# BaseValidator.java

## 概要
このクラスは入力値検証の基底クラスです。文字列の桁数チェックや数値チェックなどの共通的な検証機能を提供し、Lombokアノテーションを使用してゲッター/セッターを自動生成します。

## 基本情報
- パッケージ: `validator`
- Lombokアノテーション:
  - `@Getter`: ゲッターメソッドの自動生成
  - `@Setter`: セッターメソッドの自動生成

## フィールド
1. `hasError`: エラー有無を示すフラグ
2. `errorMessage`: エラーメッセージのリスト（ArrayList<String>）
3. `infoMessage`: 情報メッセージのリスト（ArrayList<String>）

## 主な機能

### 初期化
- コンストラクタ
  - エラーメッセージリストの初期化
  - 情報メッセージリストの初期化

### 検証機能
1. `checkByte(String str, int maxBytes, String errorMsg)`
   - 文字列のバイト長チェック
   - Shift-JISエンコーディングでのバイト数を確認
   - null/空文字列チェック
   - エラー時はメッセージを追加しfalseを返却

2. `isNumber(String str, String errorMsg)`
   - 数値形式チェック
   - Integer.parseIntを使用した検証
   - エラー時はメッセージを追加しfalseを返却

## 特記事項
- 文字エンコーディングはShift-JISを使用
- エラー発生時は自動的にhasErrorフラグがtrueに設定
- 各検証メソッドは独自のエラーメッセージを受け取り可能
- 継承先のバリデータクラスで共通利用される基盤機能を提供
