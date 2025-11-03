# EmployeeMstBL 仕様書

## ファイル概要
- **ファイル名**: EmployeeMstBL.java
- **パッケージ**: bl
- **場所**: src/bl/EmployeeMstBL.java
- **作成日**: 不明

## 目的と役割
EmployeeMstBLは、社員マスタのビジネスロジックを担当するクラスです。プレゼンテーション層（Servlet）とデータアクセス層（DAO）の間に位置し、社員情報のCRUD操作に関するビジネスルールを実装します。データベース接続の管理とトランザクション処理も担当します。

## クラス構成

### クラス定義
```java
public class EmployeeMstBL
```

### 継承関係
- **親クラス**: なし（java.lang.Object）
- **実装インターフェース**: なし

### クラス定数
- `DEFAULT_ITEM`: String型、値は "--- 社員を選択 ---"
  - 社員選択コンボボックスのデフォルト項目

## 主要メソッド

### searchEmpolyees メソッド
```java
public ArrayList<String> searchEmpolyees()
```
- **引数**: なし
- **戻り値**: `ArrayList<String>` - 社員情報のリスト（"社員番号 氏名"形式）
- **処理内容**:
  1. DBコネクションの取得
  2. EmployeeDAO経由で社員一覧を取得
  3. リストの先頭にDEFAULT_ITEMを追加
  4. コネクションのクローズ
  5. 社員情報リストを返す
- **例外処理**:
  - 例外発生時はスタックトレース出力
  - finally句で確実にコネクションをクローズ

### searchAllEmpolyees メソッド
```java
public ArrayList<Employee> searchAllEmpolyees()
```
- **引数**: なし
- **戻り値**: `ArrayList<Employee>` - 全社員情報のリスト（Employeeオブジェクト）
- **処理内容**:
  1. DBコネクションの取得
  2. EmployeeDAO経由で全社員データを取得
  3. コネクションのクローズ
  4. 社員リストを返す
- **用途**: 一覧表示用の詳細情報取得
- **例外処理**:
  - 例外発生時はスタックトレース出力
  - finally句で確実にコネクションをクローズ

### searchEmpolyeeById メソッド
```java
public EmployeeForm searchEmpolyeeById(String employeeInfo)
```
- **引数**:
  - `employeeInfo`: String - 社員情報文字列（"社員番号 氏名"形式）
- **戻り値**: `EmployeeForm` - 検索結果が格納されたフォームオブジェクト
- **処理内容**:
  1. 空のEmployeeFormオブジェクトを生成
  2. DBコネクションの取得
  3. employeeInfoから社員番号を抽出（スペース区切りの最初の要素）
  4. EmployeeDAO経由で該当社員データを取得
  5. 取得したEmployeeオブジェクトをEmployeeFormにマッピング
  6. コネクションのクローズ
  7. EmployeeFormを返す
- **例外処理**:
  - DB接続エラー時: エラーメッセージ "DB接続時に予期せぬエラーが発生しました。" を設定
  - DB切断エラー時: エラーメッセージ "DB切断時に予期せぬエラーが発生しました。" を設定
  - スタックトレース出力

### registerEmpolyee メソッド
```java
public boolean registerEmpolyee(EmployeeForm employeeForm)
```
- **引数**:
  - `employeeForm`: EmployeeForm - 登録する社員情報
- **戻り値**: `boolean` - 登録成功時true、失敗時false
- **処理内容**:
  1. DBコネクションの取得
  2. EmployeeDAO経由で社員情報を登録
  3. コネクションのクローズ
  4. 登録結果を返す
- **例外処理**:
  - DB接続エラー時: エラーメッセージ設定、falseを返す
  - DB切断エラー時: エラーメッセージ設定、falseを返す
  - スタックトレース出力

### updateEmpolyee メソッド
```java
public boolean updateEmpolyee(EmployeeForm employeeForm)
```
- **引数**:
  - `employeeForm`: EmployeeForm - 更新する社員情報
- **戻り値**: `boolean` - 更新成功時true、失敗時false
- **処理内容**:
  1. DBコネクションの取得
  2. EmployeeDAO経由で社員情報を更新
  3. コネクションのクローズ
  4. 更新結果を返す
- **例外処理**:
  - DB接続エラー時: エラーメッセージ設定、falseを返す
  - DB切断エラー時: エラーメッセージ設定、falseを返す
  - スタックトレース出力

### deleteEmpolyee メソッド
```java
public boolean deleteEmpolyee(EmployeeForm employeeForm)
```
- **引数**:
  - `employeeForm`: EmployeeForm - 削除する社員情報
- **戻り値**: `boolean` - 削除成功時true、失敗時false
- **処理内容**:
  1. DBコネクションの取得
  2. EmployeeDAO経由で社員情報を削除
  3. コネクションのクローズ
  4. 削除結果を返す
- **例外処理**:
  - DB接続エラー時: エラーメッセージ設定、falseを返す
  - DB切断エラー時: エラーメッセージ設定、falseを返す
  - スタックトレース出力

## 処理フロー

### 社員情報検索（コンボボックス用）
```
1. searchEmpolyees() 呼び出し
   ↓
2. ConnectionManager からコネクション取得
   ↓
3. EmployeeDAO をインスタンス化
   ↓
4. dao.searchEmpolyees() 実行
   ↓
5. 結果リストの先頭に DEFAULT_ITEM を追加
   ↓
6. finally句でコネクションをクローズ
   ↓
7. 社員情報リストを返す
```

### 社員情報登録
```
1. registerEmpolyee(employeeForm) 呼び出し
   ↓
2. ConnectionManager からコネクション取得
   ↓
3. EmployeeDAO をインスタンス化
   ↓
4. dao.registerEmployee(employeeForm) 実行
   ↓
5. 成功時: result = true
   失敗時: result = false、エラーメッセージ設定
   ↓
6. finally句でコネクションをクローズ
   ↓
7. result を返す
```

### 社員情報更新
```
1. updateEmpolyee(employeeForm) 呼び出し
   ↓
2. ConnectionManager からコネクション取得
   ↓
3. EmployeeDAO をインスタンス化
   ↓
4. dao.updateEmployee(employeeForm) 実行
   ↓
5. 成功時: result = true
   失敗時: result = false、エラーメッセージ設定
   ↓
6. finally句でコネクションをクローズ
   ↓
7. result を返す
```

### 社員情報削除
```
1. deleteEmpolyee(employeeForm) 呼び出し
   ↓
2. ConnectionManager からコネクション取得
   ↓
3. EmployeeDAO をインスタンス化
   ↓
4. dao.deleteEmployee(employeeForm) 実行
   ↓
5. 成功時: result = true
   失敗時: result = false、エラーメッセージ設定
   ↓
6. finally句でコネクションをクローズ
   ↓
7. result を返す
```

## 依存関係

### 依存クラス
- `java.sql.Connection`
- `java.sql.SQLException`
- `java.util.ArrayList`
- `connection.ConnectionManager` - DB接続管理
- `dao.EmployeeDAO` - データアクセス層
- `dto.Employee` - 社員データ転送オブジェクト
- `form.EmployeeForm` - 社員フォームクラス

### 呼び出し元
- `servlet.EmployeeMstServlet` - プレゼンテーション層

### 呼び出し先
- `ConnectionManager.getConnectionManager()` - シングルトンインスタンス取得
- `ConnectionManager.getConnection()` - DB接続取得
- `EmployeeDAO` - 各種データベース操作

## データベース関連
直接的なSQL実行は行わず、EmployeeDAO層に委譲します。

### 対象テーブル
- **pers** テーブル（社員情報マスタ）

### トランザクション管理
- 各メソッド内でコネクションの取得とクローズを実施
- 自動コミットモード（明示的なトランザクション管理なし）
- エラー時の自動ロールバックに依存

## 使用技術・ライブラリ

### JDBC
- java.sql.Connection
- java.sql.SQLException

### デザインパターン
- 3層アーキテクチャのビジネスロジック層
- Facade パターン（DAO層への統一インターフェース提供）

## エラーハンドリング

### 例外の種類
1. **一般的な Exception**
   - catch して printStackTrace()
   - 処理続行（検索系の場合）
   - エラーメッセージ設定（CUD操作の場合）

2. **SQLException**
   - finally句でのクローズ時に発生
   - catch して printStackTrace()
   - エラーメッセージをEmployeeFormに設定

### エラーメッセージ
- "DB接続時に予期せぬエラーが発生しました。"
- "DB切断時に予期せぬエラーが発生しました。"

## リソース管理
- **コネクション管理**:
  - 各メソッド内でコネクションを取得
  - finally句で確実にクローズ
  - リークを防ぐための適切な実装

## パフォーマンス考慮事項
- メソッド呼び出し毎にDB接続を取得・解放（コネクションプールが推奨）
- トランザクションスコープが小さい（メソッド単位）

## セキュリティ考慮事項
- SQLインジェクション対策はDAO層で実施（PreparedStatement使用）
- ビジネスロジック層では入力値の検証は行わない（Form層で実施）

## 改善提案
1. トランザクション管理の明示化（commit/rollback）
2. コネクションプールの活用
3. ログ出力の実装（SLF4J、Log4jなど）
4. try-with-resources構文の使用（Java 7以降）
5. メソッド名のスペルミス修正（Empolyee → Employee）
6. 汎用例外ではなく、独自例外クラスの定義
7. NULL安全性の向上
