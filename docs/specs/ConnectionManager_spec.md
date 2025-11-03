# ConnectionManager 仕様書

## ファイル概要
- **ファイル名**: ConnectionManager.java
- **パッケージ**: connection
- **場所**: src/connection/ConnectionManager.java
- **作成日**: 不明

## 目的と役割
ConnectionManagerは、データベース接続を管理するシングルトンクラスです。MySQLデータベースへのJDBC接続を一元管理し、アプリケーション全体で統一されたデータベースアクセスを提供します。

## クラス構成

### クラス定義
```java
public class ConnectionManager
```

### 継承関係
- **親クラス**: なし（java.lang.Object）
- **実装インターフェース**: なし

### クラス変数
- `instance`: ConnectionManager型（static） - 自身のシングルトンインスタンス

## デザインパターン
**Singletonパターン**を実装しています。
- privateコンストラクタでインスタンス化を制限
- staticメソッドでインスタンスを取得
- アプリケーション全体で1つのインスタンスのみ存在

## 主要メソッド

### getConnectionManager メソッド（静的）
```java
public static ConnectionManager getConnectionManager()
```
- **引数**: なし
- **戻り値**: `ConnectionManager` - シングルトンインスタンス
- **処理内容**:
  1. instanceがnullの場合、新しいインスタンスを生成
  2. 既存のinstanceを返す
- **スレッドセーフティ**: 非同期（同期化されていない）

### コンストラクタ（private）
```java
private ConnectionManager()
```
- **アクセス修飾子**: private（外部からのインスタンス化を防止）
- **処理内容**:
  1. MySQLのJDBCドライバをロード
  2. Class.forName("com.mysql.cj.jdbc.Driver")
- **例外処理**:
  - ClassNotFoundException: ドライバが見つからない場合
  - スタックトレース出力

### getConnection メソッド
```java
public synchronized Connection getConnection() throws SQLException
```
- **引数**: なし
- **戻り値**: `Connection` - データベースコネクション
- **修飾子**: synchronized（スレッドセーフ）
- **例外**: SQLException
- **処理内容**:
  1. DriverManager.getConnection()を呼び出し
  2. 接続URLの構成:
     - プロトコル: jdbc:mysql
     - ホスト: localhost
     - データベース名: refresh
     - オプション: serverTimezone=UTC
  3. 認証情報:
     - ユーザー名: root
     - パスワード: password
  4. Connectionオブジェクトを返す
- **例外処理**:
  - SQLException: 接続失敗時
  - スタックトレース出力
  - 例外を再スロー

## データベース接続設定

### 接続情報
```
URL: jdbc:mysql://localhost/refresh?serverTimezone=UTC
ユーザー名: root
パスワード: password
データベース名: refresh
```

### JDBCドライバ
- **ドライバクラス**: com.mysql.cj.jdbc.Driver
- **MySQL Connector/J**: 8.0以降のドライバ（cj パッケージ）

### 接続オプション
- **serverTimezone=UTC**: サーバータイムゾーンをUTCに設定

## 処理フロー

### インスタンス取得フロー
```
1. getConnectionManager() 呼び出し
   ↓
2. instance が null かチェック
   ↓
3-a. null の場合:
   new ConnectionManager() でインスタンス生成
   → コンストラクタでJDBCドライバをロード
   ↓
3-b. null でない場合:
   既存インスタンスをそのまま使用
   ↓
4. instance を返す
```

### 接続取得フロー
```
1. getConnection() 呼び出し
   ↓
2. synchronized ブロックで排他制御
   ↓
3. DriverManager.getConnection() 実行
   - 接続URL: jdbc:mysql://localhost/refresh
   - ユーザー: root
   - パスワード: password
   ↓
4. Connection オブジェクトを返す
   ↓
5. エラー時: SQLException をスローし、呼び出し元で処理
```

## 依存関係

### 依存クラス
- `java.sql.Connection`
- `java.sql.DriverManager`
- `java.sql.SQLException`

### JDBCドライバ依存
- MySQL Connector/J（com.mysql.cj.jdbc.Driver）

### 呼び出し元
- `bl.EmployeeMstBL` - ビジネスロジック層

## 使用技術・ライブラリ

### JDBC（Java Database Connectivity）
- DriverManager: 接続管理
- Connection: データベース接続

### MySQL
- データベース管理システム
- バージョン: 5.7以降（cjドライバ対応版）

## セキュリティ考慮事項

### 認証情報のハードコーディング
**重大なセキュリティリスク**
- ユーザー名とパスワードがソースコードに直接記述
- バージョン管理システムに認証情報が保存される
- コードレビュー時に露出

### 推奨される改善策
1. **環境変数の使用**
   ```java
   String user = System.getenv("DB_USER");
   String password = System.getenv("DB_PASSWORD");
   ```

2. **プロパティファイルの使用**
   - db.propertiesに設定を記述
   - .gitignoreに追加

3. **JNDIの使用**
   - アプリケーションサーバーのデータソース設定

## スレッドセーフティ

### インスタンス生成
- **問題点**: getConnectionManager()が非同期
- **リスク**: 複数スレッドから同時呼び出しで複数インスタンス生成の可能性
- **改善策**:
  ```java
  public static synchronized ConnectionManager getConnectionManager()
  ```
  または、静的初期化
  ```java
  private static final ConnectionManager instance = new ConnectionManager();
  ```

### 接続取得
- **現状**: synchronizedキーワードで同期化済み
- **動作**: スレッドセーフ

## パフォーマンス考慮事項

### コネクションプールの欠如
- **現状**: 毎回新しい接続を生成
- **問題点**:
  - 接続生成のオーバーヘッド
  - 同時接続数の制限なし
  - リソースの無駄
- **推奨される改善策**:
  - Apache Commons DBCP
  - HikariCP
  - Tomcat JDBC Connection Pool

### synchronized による性能影響
- getConnection()が同期化されているため、並行処理がボトルネックになる可能性
- コネクションプール導入で緩和可能

## エラーハンドリング

### ドライバロード時
- ClassNotFoundException をcatch
- スタックトレースのみ出力
- アプリケーションは続行（後続の接続時に失敗）

### 接続取得時
- SQLException をスロー
- 呼び出し元で処理が必要

## リソース管理
- 接続のクローズは呼び出し元の責任
- ConnectionManagerはクローズを管理しない

## 改善提案

### 1. セキュリティ
- 認証情報の外部化（環境変数、プロパティファイル）
- パスワードの暗号化

### 2. コネクションプール
- HikariCPなどのコネクションプールライブラリの導入
- 接続数の制限
- アイドルタイムアウトの設定

### 3. スレッドセーフティ
- Singletonパターンの改善（Double-Checked Locking または Enum）

### 4. 設定の柔軟性
- データベースURL、ユーザー名、パスワードの外部設定化
- 複数環境（開発、ステージング、本番）対応

### 5. ログ出力
- 接続成功/失敗のログ
- SLF4J、Log4jなどのロギングフレームワーク使用

### 6. フェイルオーバー
- マスター/スレーブ構成への対応
- 接続失敗時のリトライロジック

### 7. JNDIへの移行
- アプリケーションサーバーのデータソース機能活用
- コンテナ管理のコネクションプール使用

### 8. 接続パラメータの最適化
- useSSL、allowPublicKeyRetrievalなどの設定
- タイムアウト設定
- 自動再接続の設定

## 設定例（改善版）

### プロパティファイル（db.properties）
```properties
db.url=jdbc:mysql://localhost:3306/refresh?serverTimezone=UTC&useSSL=false
db.username=root
db.password=password
db.driver=com.mysql.cj.jdbc.Driver
pool.maxActive=10
pool.maxIdle=5
pool.minIdle=2
```

### 環境変数
```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=refresh
export DB_USER=root
export DB_PASSWORD=password
```
