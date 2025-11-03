# EmployeeDAO 仕様書

## ファイル概要
- **ファイル名**: EmployeeDAO.java
- **パッケージ**: dao
- **場所**: src/dao/EmployeeDAO.java
- **作成日**: 不明

## 目的と役割
EmployeeDAOは、社員マスタのデータアクセスオブジェクト（DAO）として、データベースの「pers」テーブルに対するCRUD操作を提供します。PreparedStatementを使用してSQLインジェクション対策を実施し、安全なデータベースアクセスを実現します。

## クラス構成

### クラス定義
```java
public class EmployeeDAO
```

### 継承関係
- **親クラス**: なし（java.lang.Object）
- **実装インターフェース**: なし

### クラス変数
- `con`: Connection型 - データベースコネクション（privateフィールド）

## 主要メソッド

### コンストラクタ
```java
public EmployeeDAO(Connection con)
```
- **引数**:
  - `con`: Connection - データベース接続
- **処理内容**: コネクションをフィールドに設定

### searchEmpolyees メソッド
```java
public ArrayList<String> searchEmpolyees()
```
- **引数**: なし
- **戻り値**: `ArrayList<String>` - 社員情報のリスト（"社員番号 氏名"形式）
- **SQL**:
  ```sql
  SELECT pers_employee, pers_name FROM pers
  ```
- **処理内容**:
  1. PreparedStatementを生成
  2. SQLクエリを実行
  3. ResultSetから社員番号と氏名を取得
  4. "社員番号 氏名"形式でリストに追加
  5. リストを返す
- **例外処理**: SQLExceptionをcatchしてスタックトレース出力

### searchAllEmpolyees メソッド
```java
public ArrayList<Employee> searchAllEmpolyees()
```
- **引数**: なし
- **戻り値**: `ArrayList<Employee>` - 全社員情報のリスト
- **SQL**:
  ```sql
  SELECT * FROM pers
  ```
- **処理内容**:
  1. PreparedStatementを生成
  2. SQLクエリを実行
  3. ResultSetから全カラムを取得
  4. Employeeオブジェクトに格納
  5. リストに追加
  6. リストを返す
- **例外処理**: SQLExceptionをcatchしてスタックトレース出力

### searchEmpolyeeById メソッド
```java
public Employee searchEmpolyeeById(String id, EmployeeForm employeeForm)
```
- **引数**:
  - `id`: String - 社員番号
  - `employeeForm`: EmployeeForm - エラーメッセージ格納用
- **戻り値**: `Employee` - 該当する社員情報（見つからない場合は空のEmployeeオブジェクト）
- **SQL**:
  ```sql
  SELECT * FROM pers WHERE pers_employee = ?
  ```
- **処理内容**:
  1. PreparedStatementを生成
  2. 社員番号をバインド
  3. SQLクエリを実行
  4. 該当データがあればEmployeeオブジェクトに格納
  5. Employeeオブジェクトを返す
- **例外処理**:
  - SQLExceptionをcatch
  - スタックトレース出力
  - エラーメッセージ "社員情報の取得時に予期せぬエラーが発生しました。" を設定

### registerEmployee メソッド
```java
public boolean registerEmployee(EmployeeForm employeeForm)
```
- **引数**:
  - `employeeForm`: EmployeeForm - 登録する社員情報
- **戻り値**: `boolean` - 登録成功時true、失敗時false
- **SQL**:
  ```sql
  INSERT INTO pers (pers_employee, pers_oano, pers_sei, pers_mei, pers_name,
                    pers_namek, pers_bu, pers_gr, pers_indate, pers_intime)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  ```
- **処理内容**:
  1. PreparedStatementを生成
  2. setRegisterParameters()で値をバインド
  3. executeUpdate()でINSERT実行
  4. 成功メッセージ "社員情報の登録に成功しました。" を設定
  5. trueを返す
- **例外処理**:
  - SQLIntegrityConstraintViolationException: 主キー重複時
    - エラーメッセージ "入力した社員番号はすでに登録されています。"
    - falseを返す
  - SQLException: その他のエラー
    - エラーメッセージ "社員情報の登録時に予期せぬエラーが発生しました。"
    - falseを返す

### updateEmployee メソッド
```java
public boolean updateEmployee(EmployeeForm employeeForm)
```
- **引数**:
  - `employeeForm`: EmployeeForm - 更新する社員情報
- **戻り値**: `boolean` - 更新成功時true、失敗時false
- **SQL**:
  ```sql
  UPDATE pers SET pers_oano = ?, pers_sei = ?, pers_mei = ?,
                  pers_name = ?, pers_namek = ?, pers_bu = ?, pers_gr = ?,
                  pers_update = ?, pers_uptime = ?
  WHERE pers_employee = ?
  ```
- **処理内容**:
  1. PreparedStatementを生成
  2. setUpdateParameters()で値をバインド
  3. executeUpdate()でUPDATE実行
  4. 成功メッセージ "社員情報の更新に成功しました。" を設定
  5. trueを返す
- **例外処理**:
  - SQLException:
    - エラーメッセージ "社員情報の更新時に予期せぬエラーが発生しました。"
    - falseを返す

### deleteEmployee メソッド
```java
public boolean deleteEmployee(EmployeeForm employeeForm)
```
- **引数**:
  - `employeeForm`: EmployeeForm - 削除する社員情報
- **戻り値**: `boolean` - 削除成功時true、失敗時false
- **SQL**:
  ```sql
  DELETE FROM pers WHERE pers_employee = ?
  ```
- **処理内容**:
  1. PreparedStatementを生成
  2. setDeleteParameters()で値をバインド
  3. executeUpdate()でDELETE実行
  4. 成功メッセージ "社員情報の削除に成功しました。" を設定
  5. trueを返す
- **例外処理**:
  - SQLException:
    - エラーメッセージ "社員情報の削除時に予期せぬエラーが発生しました。"
    - falseを返す

### setRegisterParameters メソッド
```java
public void setRegisterParameters(PreparedStatement pStmt, EmployeeForm employeeForm)
    throws SQLException
```
- **引数**:
  - `pStmt`: PreparedStatement
  - `employeeForm`: EmployeeForm
- **処理内容**: INSERT用のパラメータを設定
  1. 社員番号
  2. OA番号
  3. 姓（空文字列）
  4. 名（空文字列）
  5. 氏名（漢字）
  6. 氏名（カナ）
  7. 部署
  8. グループ
  9. 登録日（yyyyMMdd形式）
  10. 登録時刻（HHmmss形式）

### setUpdateParameters メソッド
```java
public void setUpdateParameters(PreparedStatement pStmt, EmployeeForm employeeForm)
    throws SQLException
```
- **引数**:
  - `pStmt`: PreparedStatement
  - `employeeForm`: EmployeeForm
- **処理内容**: UPDATE用のパラメータを設定
  1. OA番号
  2. 姓（空文字列）
  3. 名（空文字列）
  4. 氏名（漢字）
  5. 氏名（カナ）
  6. 部署
  7. グループ
  8. 更新日（yyyyMMdd形式）
  9. 更新時刻（HHmmss形式）
  10. 社員番号（WHERE条件）

### setDeleteParameters メソッド
```java
public void setDeleteParameters(PreparedStatement pStmt, EmployeeForm employeeForm)
    throws SQLException
```
- **引数**:
  - `pStmt`: PreparedStatement
  - `employeeForm`: EmployeeForm
- **処理内容**: DELETE用のパラメータを設定
  1. 社員番号（WHERE条件）

## データベーステーブル構造

### pers テーブル（社員情報マスタ）
| カラム名 | データ型 | 説明 | 備考 |
|---------|---------|------|------|
| pers_employee | VARCHAR | 社員番号 | 主キー |
| pers_oano | VARCHAR | OA番号 | |
| pers_sei | VARCHAR | 姓 | 現在未使用（空文字列） |
| pers_mei | VARCHAR | 名 | 現在未使用（空文字列） |
| pers_name | VARCHAR | 氏名（漢字） | |
| pers_namek | VARCHAR | 氏名（カナ） | |
| pers_bu | VARCHAR | 所属部署 | |
| pers_gr | VARCHAR | 所属グループ | |
| pers_indate | VARCHAR | 登録日 | yyyyMMdd形式 |
| pers_intime | VARCHAR | 登録時刻 | HHmmss形式 |
| pers_update | VARCHAR | 更新日 | yyyyMMdd形式 |
| pers_uptime | VARCHAR | 更新時刻 | HHmmss形式 |

## 処理フロー

### 社員情報登録
```
1. registerEmployee(employeeForm) 呼び出し
   ↓
2. INSERT文のPreparedStatementを生成
   ↓
3. setRegisterParameters()でパラメータ設定
   - 社員情報
   - 現在日時（登録日時）
   ↓
4. executeUpdate()実行
   ↓
5. 成功: 成功メッセージ設定、trueを返す
   失敗: エラーメッセージ設定、falseを返す
```

### 社員情報更新
```
1. updateEmployee(employeeForm) 呼び出し
   ↓
2. UPDATE文のPreparedStatementを生成
   ↓
3. setUpdateParameters()でパラメータ設定
   - 更新する社員情報
   - 現在日時（更新日時）
   - WHERE条件（社員番号）
   ↓
4. executeUpdate()実行
   ↓
5. 成功: 成功メッセージ設定、trueを返す
   失敗: エラーメッセージ設定、falseを返す
```

### 社員情報削除
```
1. deleteEmployee(employeeForm) 呼び出し
   ↓
2. DELETE文のPreparedStatementを生成
   ↓
3. setDeleteParameters()でパラメータ設定
   - WHERE条件（社員番号）
   ↓
4. executeUpdate()実行
   ↓
5. 成功: 成功メッセージ設定、trueを返す
   失敗: エラーメッセージ設定、falseを返す
```

## 依存関係

### 依存クラス
- `java.sql.Connection`
- `java.sql.PreparedStatement`
- `java.sql.ResultSet`
- `java.sql.SQLException`
- `java.sql.SQLIntegrityConstraintViolationException`
- `java.time.LocalDateTime`
- `java.time.format.DateTimeFormatter`
- `java.util.ArrayList`
- `dto.Employee`
- `form.EmployeeForm`

### 呼び出し元
- `bl.EmployeeMstBL` - ビジネスロジック層

### 呼び出し先
- なし（データベースへの直接アクセス）

## 使用技術・ライブラリ

### JDBC
- PreparedStatement（SQLインジェクション対策）
- ResultSet
- SQLException

### Java Time API
- LocalDateTime - 現在日時の取得
- DateTimeFormatter - 日時フォーマット

### デザインパターン
- DAO（Data Access Object）パターン
- 3層アーキテクチャのデータアクセス層

## セキュリティ考慮事項

### SQLインジェクション対策
- 全てのSQL文でPreparedStatementを使用
- パラメータバインドによる安全なSQL実行

### 制約違反の検出
- 主キー重複時の適切なエラーハンドリング
- SQLIntegrityConstraintViolationExceptionの個別キャッチ

## パフォーマンス考慮事項
- PreparedStatementのクローズ処理が未実装（メモリリーク注意）
- バッチ処理の未実装（大量データ登録時は要検討）

## エラーハンドリング

### 例外の種類
1. **SQLIntegrityConstraintViolationException**
   - 主キー重複時
   - 適切なエラーメッセージをユーザーに提示

2. **SQLException**
   - その他のデータベースエラー
   - スタックトレース出力
   - 汎用的なエラーメッセージを設定

### エラーメッセージ
- "社員情報の取得時に予期せぬエラーが発生しました。"
- "入力した社員番号はすでに登録されています。"
- "社員情報の登録時に予期せぬエラーが発生しました。"
- "社員情報の更新時に予期せぬエラーが発生しました。"
- "社員情報の削除時に予期せぬエラーが発生しました。"

## リソース管理
- **PreparedStatementのクローズ**: 未実装（要改善）
- **ResultSetのクローズ**: 未実装（要改善）
- **Connectionのクローズ**: 呼び出し元（BL層）で実施

## 改善提案
1. **リソース管理**: try-with-resources構文の使用
2. **日付型の改善**: 文字列型から DATE/TIMESTAMP型への変更
3. **姓・名の活用**: pers_sei、pers_meiカラムの活用（現在未使用）
4. **バッチ処理**: 大量データ登録・更新時の対応
5. **トランザクション**: 明示的なcommit/rollback
6. **メソッド名**: スペルミス修正（Empolyee → Employee）
7. **ページネーション**: 大量データ取得時の対応
8. **インデックス最適化**: 検索パフォーマンスの向上
9. **監査ログ**: 誰がいつ更新したかの記録
