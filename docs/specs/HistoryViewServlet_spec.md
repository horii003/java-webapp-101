# HistoryViewServlet 仕様書

## ファイル概要
- **ファイル名**: HistoryViewServlet.java
- **パッケージ**: servlet
- **場所**: src/servlet/HistoryViewServlet.java
- **実装状況**: 基本機能のみ実装、詳細機能は未実装

## 目的と役割
HistoryViewServletは、購入履歴参照ページへの遷移を担当するサーブレットです。ユーザーからのリクエストを受け取り、購入履歴の表示画面（historyView.jsp）へフォワードします。

## クラス構成

### クラス定義
```java
@WebServlet("/historyView")
public class HistoryViewServlet extends HttpServlet
```

### 継承関係
- **親クラス**: `javax.servlet.http.HttpServlet`
- **実装インターフェース**: なし

### アノテーション
- `@WebServlet("/historyView")`: URLパターン "/historyView" にマッピング

### クラス変数
- `serialVersionUID`: シリアライゼーション用の固有ID（値: 1L）

## 主要メソッド

### コンストラクタ
```java
public HistoryViewServlet()
```
- **引数**: なし
- **処理内容**: 親クラスのコンストラクタを呼び出す
- **備考**: TODO コメントあり（自動生成コード）

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
  - 購入履歴参照ページ（historyView.jsp）へリクエストをフォワード

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
- **備考**: TODO コメントあり（未実装）

## 処理フロー

### GETリクエスト時
```
1. /historyView へのGETリクエスト受信
   ↓
2. doGet()メソッド呼び出し
   ↓
3. historyView.jspへフォワード
   ↓
4. JSPがレンダリングされてクライアントに返される
```

### POSTリクエスト時
```
1. /historyView へのPOSTリクエスト受信
   ↓
2. doPost()メソッド呼び出し
   ↓
3. doGet()メソッドを呼び出し
   ↓
4. GETリクエストと同じ処理
```

## 依存関係

### 依存クラス
- `javax.servlet.*`
- `javax.servlet.http.*`
- `java.io.IOException`

### 連携するファイル
- **JSPファイル**: historyView.jsp（購入履歴参照ページ）

### 呼び出し元
- Webブラウザからの直接アクセス
- 他のページからのリンク

### 呼び出し先
- historyView.jsp（フォワード）

## データベース関連
- 現在はデータベース連携なし
- 実際の履歴表示には、履歴データの取得処理が必要（未実装）

## 使用技術・ライブラリ
- Java Servlet API
- アノテーションベースマッピング（@WebServlet）

## 実装状況
- **実装済み**: JSPへの基本的なフォワード機能
- **未実装**:
  - 購入履歴データの取得
  - データベースアクセス
  - 検索・フィルタリング機能
  - ページネーション

## 改善提案

### 1. 購入履歴データの取得
```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    // ビジネスロジック層の呼び出し
    PurchaseHistoryBL bl = new PurchaseHistoryBL();
    List<PurchaseHistory> historyList = bl.getHistoryList();

    request.setAttribute("historyList", historyList);
    request.getRequestDispatcher("historyView.jsp").forward(request, response);
}
```

### 2. ユーザー別履歴の取得
```java
// セッションからユーザー情報取得
HttpSession session = request.getSession();
User user = (User) session.getAttribute("user");

// ユーザー別の履歴取得
List<PurchaseHistory> historyList = bl.getHistoryByUser(user.getId());
```

### 3. 検索・フィルタリング機能
```java
// 検索条件の取得
String startDate = request.getParameter("startDate");
String endDate = request.getParameter("endDate");
String itemName = request.getParameter("itemName");

// 条件に基づいた履歴取得
List<PurchaseHistory> historyList = bl.searchHistory(startDate, endDate, itemName);
```

### 4. ページネーション
```java
// ページング情報の取得
int page = Integer.parseInt(request.getParameter("page") != null ?
    request.getParameter("page") : "1");
int pageSize = 20;

// ページングされた履歴取得
PagedResult<PurchaseHistory> pagedResult = bl.getHistoryPaged(page, pageSize);
request.setAttribute("historyList", pagedResult.getData());
request.setAttribute("totalPages", pagedResult.getTotalPages());
request.setAttribute("currentPage", page);
```

### 5. CSV/Excel エクスポート機能
```java
// エクスポート処理
String format = request.getParameter("export");
if ("csv".equals(format)) {
    exportCSV(response, historyList);
    return;
} else if ("excel".equals(format)) {
    exportExcel(response, historyList);
    return;
}
```

### 6. エラーハンドリング
```java
try {
    // 履歴取得処理
} catch (Exception e) {
    log.error("Error retrieving purchase history", e);
    request.setAttribute("error", "履歴の取得に失敗しました");
    request.getRequestDispatcher("error.jsp").forward(request, response);
}
```

### 7. 認証チェック
```java
// ログインチェック
if (!isAuthenticated(request)) {
    response.sendRedirect("login.jsp");
    return;
}
```

## セキュリティ考慮事項
- 認証・認可の実装が必要
- 他のユーザーの履歴が閲覧できないようにする
- SQLインジェクション対策（DAO層で実施）

## パフォーマンス考慮事項
- 履歴データが大量の場合、ページネーションが必須
- インデックスの適切な設定
- キャッシュの活用

## まとめ
HistoryViewServletは購入履歴参照機能の基本的な枠組みのみを提供する未完成のサーブレットです。実際の履歴データ取得や表示機能は今後の開発で実装が必要です。
