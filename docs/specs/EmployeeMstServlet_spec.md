# EmployeeMstServlet 仕様書

## ファイル概要
- **ファイル名**: EmployeeMstServlet.java
- **パッケージ**: servlet
- **場所**: src/servlet/EmployeeMstServlet.java
- **作成日**: 不明

## 目的と役割
EmployeeMstServletは、社員マスタ管理機能を提供するサーブレットです。社員情報の登録、更新、削除、検索といったCRUD操作をWebインターフェースを通じて実現します。ビジネスロジック層（EmployeeMstBL）と連携し、社員データの管理を行います。

## クラス構成

### クラス定義
```java
@WebServlet("/employee")
public class EmployeeMstServlet extends HttpServlet
```

### 継承関係
- **親クラス**: `javax.servlet.http.HttpServlet`
- **実装インターフェース**: なし

### アノテーション
- `@WebServlet("/employee")`: URLパターン "/employee" にマッピング

### クラス変数
- `serialVersionUID`: シリアライゼーション用の固有ID（値: 1L）

## 主要メソッド

### コンストラクタ
```java
public EmployeeMstServlet()
```
- **引数**: なし
- **処理内容**: 親クラスのコンストラクタを呼び出す

### doGet メソッド
```java
protected void doGet(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException
```
- **引数**:
  - `request`: HttpServletRequest - クライアントからのリクエスト情報
  - `response`: HttpServletResponse - クライアントへのレスポンス情報
- **戻り値**: void
- **例外**: ServletException, IOException
- **処理内容**:
  1. 文字エンコーディングをUTF-8に設定
  2. EmployeeMstBLとEmployeeFormのインスタンス生成
  3. コンボボックス用データの取得
  4. フォームの初期化
  5. employeeMst.jspへフォワード

### doPost メソッド
```java
protected void doPost(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException
```
- **引数**:
  - `request`: HttpServletRequest - クライアントからのリクエスト情報
  - `response`: HttpServletResponse - クライアントへのレスポンス情報
- **戻り値**: void
- **例外**: ServletException, IOException
- **処理内容**:
  1. 文字エンコーディングをUTF-8に設定
  2. EmployeeMstBLとEmployeeFormのインスタンス生成
  3. executeパラメータに応じた処理分岐
     - `list`: 社員一覧表示
     - `select`: 特定社員の選択・表示
     - `register`: 社員情報の新規登録
     - `update`: 社員情報の更新
     - `delete`: 社員情報の削除
  4. エラーメッセージ・情報メッセージの設定
  5. コンボボックスの再初期化
  6. employeeMst.jspへフォワード

### setAttributeFromEmployeeForm メソッド
```java
protected void setAttributeFromEmployeeForm(HttpServletRequest request, EmployeeForm employeeForm)
```
- **処理内容**: EmployeeFormオブジェクトからRequestオブジェクトへ値を渡す

### setEmployeeForm メソッド
```java
protected void setEmployeeForm(HttpServletRequest request, EmployeeForm employeeForm)
```
- **処理内容**: Requestパラメータから EmployeeForm オブジェクトへ値を設定

### setInfoMsg メソッド
```java
protected void setInfoMsg(HttpServletRequest request, EmployeeForm employeeForm)
```
- **処理内容**: 情報メッセージをRequestに設定

### setErrorMsg メソッド
```java
protected void setErrorMsg(HttpServletRequest request, EmployeeForm employeeForm)
```
- **処理内容**: エラーメッセージをRequestに設定

### initEmployeeForm メソッド
```java
protected void initEmployeeForm(HttpServletRequest request)
```
- **処理内容**: フォームの全項目を空文字列で初期化

### initComboBox メソッド
```java
protected void initComboBox(HttpServletRequest request, EmployeeMstBL bl, EmployeeForm employeeForm)
```
- **処理内容**: コンボボックス用のデータをRequestに設定
  - 社員情報リスト
  - 部署リスト
  - グループリスト

## 処理フロー

### GETリクエスト時（初期表示）
```
1. /employee へのGETリクエスト受信
   ↓
2. doGet()メソッド実行
   ↓
3. 文字エンコーディング設定（UTF-8）
   ↓
4. BLとFormのインスタンス生成
   ↓
5. コンボボックスデータ取得
   - 社員一覧
   - 部署一覧
   - グループ一覧
   ↓
6. フォームを空で初期化
   ↓
7. employeeMst.jspへフォワード
```

### POSTリクエスト時（一覧表示）
```
execute=list のとき：
1. /employee へのPOSTリクエスト受信
   ↓
2. doPost()メソッド実行
   ↓
3. BLを通じて全社員情報を検索
   ↓
4. employeeListをRequestに設定
   ↓
5. employeeMstList.jspへフォワード
```

### POSTリクエスト時（社員選択）
```
execute=select のとき：
1. employeeNameパラメータ取得
   ↓
2. BLを通じて該当社員情報を検索
   ↓
3. エラーチェック
   ↓
4. 社員情報をRequestに設定
   ↓
5. デフォルト値でなければeditFlg=trueを設定（更新・削除ボタン表示）
   ↓
6. employeeMst.jspへフォワード
```

### POSTリクエスト時（登録）
```
execute=register のとき：
1. フォームデータを EmployeeForm に設定
   ↓
2. バリデーション実行
   ↓
3. バリデーションOKの場合、BL経由で登録
   ↓
4. 結果に応じてメッセージ設定
   ↓
5. コンボボックス再初期化
   ↓
6. employeeMst.jspへフォワード
```

### POSTリクエスト時（更新）
```
execute=update のとき：
1. フォームデータを EmployeeForm に設定
   ↓
2. バリデーション実行
   ↓
3. バリデーションOKの場合、BL経由で更新
   ↓
4. 結果に応じてメッセージ設定
   ↓
5. editFlg=trueを設定（エラー時）
   ↓
6. コンボボックス再初期化
   ↓
7. employeeMst.jspへフォワード
```

### POSTリクエスト時（削除）
```
execute=delete のとき：
1. フォームデータを EmployeeForm に設定
   ↓
2. BL経由で削除実行
   ↓
3. 結果に応じてメッセージ設定
   ↓
4. editFlg=trueを設定（エラー時）
   ↓
5. コンボボックス再初期化
   ↓
6. employeeMst.jspへフォワード
```

## 依存関係

### 依存クラス
- `javax.servlet.*`
- `javax.servlet.http.*`
- `java.io.IOException`
- `java.util.ArrayList`
- `bl.EmployeeMstBL` - ビジネスロジック層
- `form.EmployeeForm` - フォームクラス

### 連携するファイル
- **JSPファイル**:
  - employeeMst.jsp（社員マスタ入力画面）
  - employeeMstList.jsp（社員一覧画面）
- **ビジネスロジック**: EmployeeMstBL
- **フォームクラス**: EmployeeForm

### 呼び出し元
- Webブラウザ
- employeeMst.jsp、employeeMstList.jsp からのフォーム送信

### 呼び出し先
- EmployeeMstBL（各種CRUD操作）
- EmployeeForm（バリデーション、データ保持）
- JSPファイル（フォワード）

## データベース関連
直接的なDB操作は行わず、EmployeeMstBL経由でデータベースアクセスを実施します。

### 対象テーブル
- **pers** テーブル（社員情報）
  - pers_employee（社員番号）- 主キー
  - pers_oano（OA番号）
  - pers_name（氏名・漢字）
  - pers_namek（氏名・カナ）
  - pers_bu（部署）
  - pers_gr（グループ）

## 使用技術・ライブラリ

### フレームワーク
- Java Servlet API

### アノテーション
- `@WebServlet`: サーブレット3.0以降のアノテーションベースマッピング

### デザインパターン
- MVC（Model-View-Controller）パターン
- 3層アーキテクチャ（プレゼンテーション層としての役割）

## セキュリティ考慮事項
- 文字エンコーディング設定（UTF-8）
- 認証・認可の実装なし（要検討）
- SQLインジェクション対策はDAO層で実施（PreparedStatement使用）
- XSS対策は要確認

## パフォーマンス考慮事項
- リクエスト毎にBLとFormのインスタンスを生成（軽量なため問題なし）
- コンボボックスデータは毎回DB取得（キャッシュ化の検討余地あり）

## エラーハンドリング
- try-catch による例外捕捉
- エラーメッセージはEmployeeFormに格納
- エラー発生時もJSPへフォワード（エラーメッセージを表示）
- 例外の詳細はスタックトレース出力

## リクエストパラメータ

### executeパラメータの値
- `list`: 一覧表示
- `select`: 社員選択
- `register`: 登録
- `update`: 更新
- `delete`: 削除

### その他のパラメータ
- `employeeName`: 社員名（選択時）
- `employeeId`: 社員番号
- `oano`: OA番号
- `employeeNameKanji`: 氏名（漢字）
- `employeeNameKana`: 氏名（カナ）
- `department`: 部署
- `group`: グループ

## 改善提案
1. 認証・認可機能の追加
2. ログ出力の実装
3. コンボボックスデータのキャッシュ化
4. トランザクション管理の明示化
5. 入力値のサニタイズ強化
6. RESTful APIへのリファクタリング検討
