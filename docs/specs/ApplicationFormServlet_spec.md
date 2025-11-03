# ApplicationFormServlet 仕様書

## ファイル概要
- **ファイル名**: ApplicationFormServlet.java
- **パッケージ**: servlet
- **場所**: src/servlet/ApplicationFormServlet.java
- **作成日**: 不明

## 目的と役割
ApplicationFormServletは、購入申請書作成ページへの遷移を担当するサーブレットです。ユーザーからのリクエストを受け取り、購入申請書の入力画面（applicationForm.jsp）へフォワードします。

## クラス構成

### クラス定義
```java
@WebServlet("/applicationForm")
public class ApplicationFormServlet extends HttpServlet
```

### 継承関係
- **親クラス**: `javax.servlet.http.HttpServlet`
- **実装インターフェース**: なし

### アノテーション
- `@WebServlet("/applicationForm")`: URLパターン "/applicationForm" にマッピング

### クラス変数
- `serialVersionUID`: シリアライゼーション用の固有ID（値: 1L）

## 主要メソッド

### コンストラクタ
```java
public ApplicationFormServlet()
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
  - 購入申請書作成ページ（applicationForm.jsp）へリクエストをフォワード

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
  - doGet()メソッドを呼び出す（POSTリクエストもGETと同じ処理）

## 処理フロー

### GETリクエスト時の処理フロー
```
1. クライアントから /applicationForm へのGETリクエスト受信
   ↓
2. doGet()メソッドが呼び出される
   ↓
3. request.getRequestDispatcher("applicationForm.jsp")でディスパッチャを取得
   ↓
4. forward()でapplicationForm.jspへフォワード
   ↓
5. applicationForm.jspがレンダリングされクライアントに返される
```

### POSTリクエスト時の処理フロー
```
1. クライアントから /applicationForm へのPOSTリクエスト受信
   ↓
2. doPost()メソッドが呼び出される
   ↓
3. doGet(request, response)を呼び出し
   ↓
4. GETリクエストと同じ処理を実行
   ↓
5. applicationForm.jspへフォワード
```

## 依存関係

### 依存クラス
- `javax.servlet.ServletException`
- `javax.servlet.annotation.WebServlet`
- `javax.servlet.http.HttpServlet`
- `javax.servlet.http.HttpServletRequest`
- `javax.servlet.http.HttpServletResponse`
- `java.io.IOException`

### 連携するファイル
- **JSPファイル**: applicationForm.jsp（購入申請書作成ページ）

### 呼び出し元
- Webブラウザから直接アクセス
- 他のページからのリンク
- 他のサーブレットからのリダイレクト/フォワード（可能性あり）

### 呼び出し先
- applicationForm.jsp（フォワード）

## データベース関連
このサーブレットはデータベースとの連携は行いません。

## 使用技術・ライブラリ

### フレームワーク
- Java Servlet API

### アノテーション
- `@WebServlet`: サーブレット3.0以降のアノテーションベースマッピング

## セキュリティ考慮事項
- 認証・認可の実装なし
- 誰でもアクセス可能なページ
- フォーム送信時のCSRF対策が必要

## パフォーマンス考慮事項
- 単純なフォワード処理のため、パフォーマンス上の問題はなし
- ビジネスロジックなし

## エラーハンドリング
- ServletException、IOExceptionはサーブレットコンテナが処理
- 独自のエラーハンドリングは実装されていない

## doGetとdoPostの関係
- doPost()がdoGet()を呼び出す実装
- GET/POSTで同じ画面を表示
- RESTfulな設計とは異なる

## 特徴と制約

### 特徴
1. **シンプルな実装**
   - フォワードのみを行う
   - ビジネスロジックなし

2. **GET/POST両対応**
   - どちらのメソッドでも同じ画面を表示

3. **ステートレス**
   - セッション管理なし
   - リクエスト間で状態を保持しない

### 制約
1. **機能が未実装**
   - 実際の申請書作成処理は未実装
   - JSPへの単純なフォワードのみ

2. **エラーハンドリングなし**
   - 例外は全てコンテナに委譲

3. **バリデーションなし**
   - 入力チェックなし

## 改善提案

### 1. POST処理の実装
```java
protected void doPost(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
    // 文字エンコーディング設定
    request.setCharacterEncoding("UTF-8");

    // フォームデータの取得
    String itemName = request.getParameter("itemName");
    String quantity = request.getParameter("quantity");
    // ...

    // バリデーション
    if (isValid(itemName, quantity)) {
        // データベースへの保存
        // ...
        // 成功メッセージ
        request.setAttribute("message", "申請書を登録しました");
    } else {
        // エラーメッセージ
        request.setAttribute("error", "入力内容に誤りがあります");
    }

    // 結果ページへフォワード
    request.getRequestDispatcher("applicationFormResult.jsp").forward(request, response);
}
```

### 2. GET/POSTの明確な分離
```java
// GET: 初期表示
protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    // フォーム表示
}

// POST: データ処理
protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    // 申請書の登録処理
}
```

### 3. ビジネスロジックの追加
```java
// ビジネスロジック層の呼び出し
ApplicationFormBL bl = new ApplicationFormBL();
boolean result = bl.registerApplication(form);
```

### 4. エラーハンドリング
```java
try {
    // 処理
} catch (Exception e) {
    log.error("Error in ApplicationFormServlet", e);
    request.setAttribute("error", "システムエラーが発生しました");
    request.getRequestDispatcher("error.jsp").forward(request, response);
}
```

### 5. ログ出力
```java
private static final Logger log = LoggerFactory.getLogger(ApplicationFormServlet.class);

protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    log.info("Accessing application form page");
    // ...
}
```

### 6. 認証チェック
```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    // セッションチェック
    HttpSession session = request.getSession(false);
    if (session == null || session.getAttribute("user") == null) {
        response.sendRedirect("login.jsp");
        return;
    }
    // ...
}
```

### 7. CSRF対策
```java
// トークン生成
String csrfToken = generateCSRFToken();
session.setAttribute("csrfToken", csrfToken);
request.setAttribute("csrfToken", csrfToken);

// JSPでトークンを含める
<input type="hidden" name="csrfToken" value="${csrfToken}">

// POSTでトークン検証
String sessionToken = (String) session.getAttribute("csrfToken");
String requestToken = request.getParameter("csrfToken");
if (!sessionToken.equals(requestToken)) {
    // CSRF攻撃の可能性
    response.sendError(HttpServletResponse.SC_FORBIDDEN);
    return;
}
```

### 8. RESTful APIへのリファクタリング
```java
// REST API化
@WebServlet("/api/applications")
public class ApplicationFormServlet extends HttpServlet {
    // GET: 申請書一覧取得
    // POST: 申請書作成
    // PUT: 申請書更新
    // DELETE: 申請書削除
}
```

### 9. 入力値のバリデーション
```java
// フォームクラスの作成
ApplicationForm form = new ApplicationForm();
form.setItemName(request.getParameter("itemName"));
// ...

// バリデーション
if (!form.validateInputData()) {
    request.setAttribute("errors", form.getErrorMessage());
    request.getRequestDispatcher("applicationForm.jsp").forward(request, response);
    return;
}
```

### 10. ファイルアップロード対応
```java
@MultipartConfig
public class ApplicationFormServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response) {
        Part filePart = request.getPart("file");
        // ファイル処理
    }
}
```

## 使用例

### アクセス例
```
# ブラウザから直接アクセス
http://localhost:8080/applicationForm

# GETリクエスト
GET /applicationForm HTTP/1.1
Host: localhost:8080

# POSTリクエスト（現在の実装ではGETと同じ動作）
POST /applicationForm HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded
```

### JSPでのリンク
```jsp
<a href="applicationForm">購入申請書を作成</a>

<form action="applicationForm" method="post">
    <!-- フォーム内容 -->
    <button type="submit">送信</button>
</form>
```

## コメントの解釈
- コード内に「TODO Auto-generated」コメントが残っている
- Eclipse等のIDEで自動生成されたテンプレート
- 実装が完了していないことを示唆

## まとめ
ApplicationFormServletは、購入申請書作成ページへの単純なフォワード機能のみを提供する未完成のサーブレットです。実際の申請書処理機能は未実装であり、今後の開発で機能拡張が必要です。
