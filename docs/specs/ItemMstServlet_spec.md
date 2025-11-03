# ItemMstServlet 仕様書

## ファイル概要
- **ファイル名**: ItemMstServlet.java
- **パッケージ**: servlet
- **場所**: src/servlet/ItemMstServlet.java
- **実装状況**: 基本機能のみ実装、詳細機能は未実装

## 目的と役割
ItemMstServletは、物品マスタ管理ページへの遷移を担当するサーブレットです。物品情報のCRUD操作を管理するための画面へユーザーをフォワードします。

## クラス構成

### クラス定義
```java
@WebServlet("/item")
public class ItemMstServlet extends HttpServlet
```

### 継承関係
- **親クラス**: `javax.servlet.http.HttpServlet`
- **実装インターフェース**: なし

### アノテーション
- `@WebServlet("/item")`: URLパターン "/item" にマッピング

### クラス変数
- `serialVersionUID`: シリアライゼーション用の固有ID（値: 1L）

## 主要メソッド

### コンストラクタ
```java
public ItemMstServlet()
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
  - 物品マスタページ（itemMst.jsp）へリクエストをフォワード

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
  1. コンソールに "POST: ITEM page..." を出力
  2. doGet()メソッドを呼び出す
- **備考**: TODO コメントあり、デバッグ用のコンソール出力あり

## 処理フロー

### GETリクエスト時
```
1. /item へのGETリクエスト受信
   ↓
2. doGet()メソッド呼び出し
   ↓
3. itemMst.jspへフォワード
   ↓
4. JSPがレンダリングされてクライアントに返される
```

### POSTリクエスト時
```
1. /item へのPOSTリクエスト受信
   ↓
2. doPost()メソッド呼び出し
   ↓
3. コンソールに "POST: ITEM page..." 出力
   ↓
4. doGet()メソッドを呼び出し
   ↓
5. GETリクエストと同じ処理
```

## 依存関係

### 依存クラス
- `javax.servlet.*`
- `javax.servlet.http.*`
- `java.io.IOException`

### 関連ファイル
- **JSPファイル**: itemMst.jsp（物品マスタページ）
- **バリデータ**: `validator.ItemValidator`（関連はあるが未使用）
- **DTO**: `dto.Test`（関連はあるが未使用）

### 呼び出し元
- Webブラウザからの直接アクセス
- 他のページからのリンク

### 呼び出し先
- itemMst.jsp（フォワード）

## データベース関連
- 現在はデータベース連携なし
- 実際の物品マスタ管理には、CRUD操作の実装が必要（未実装）

## デバッグ機能
- doPost()内でコンソール出力を実装
- "POST: ITEM page..." メッセージでPOSTリクエストを確認可能
- 本番環境では削除推奨

## 使用技術・ライブラリ
- Java Servlet API
- アノテーションベースマッピング（@WebServlet）

## 実装状況

### 実装済み
- JSPへの基本的なフォワード機能
- デバッグ用のコンソール出力

### 未実装
- 物品情報の取得
- 物品情報の登録
- 物品情報の更新
- 物品情報の削除
- バリデーション機能
- ItemValidatorの活用

## 改善提案

### 1. 物品マスタのCRUD操作実装
```java
protected void doPost(HttpServletRequest request, HttpServletResponse response)
    throws ServletException, IOException {
    request.setCharacterEncoding("UTF-8");

    // ビジネスロジック層のインスタンス化
    ItemMstBL bl = new ItemMstBL();
    ItemForm itemForm = new ItemForm();

    String execution = request.getParameter("execute");

    switch(execution) {
        case "list":
            // 一覧表示
            request.setAttribute("itemList", bl.searchAllItems());
            request.getRequestDispatcher("itemMstList.jsp").forward(request, response);
            return;

        case "register":
            // 登録処理
            setItemForm(request, itemForm);
            if (itemForm.validateInputData()) {
                bl.registerItem(itemForm);
            }
            break;

        case "update":
            // 更新処理
            setItemForm(request, itemForm);
            if (itemForm.validateInputData()) {
                bl.updateItem(itemForm);
            }
            break;

        case "delete":
            // 削除処理
            setItemForm(request, itemForm);
            bl.deleteItem(itemForm);
            break;
    }

    request.getRequestDispatcher("itemMst.jsp").forward(request, response);
}
```

### 2. ItemValidatorの活用
```java
// バリデーション実行
ItemValidator validator = new ItemValidator();
Test test = new Test();
test.setTest(request.getParameter("itemCode"));

List<String> errors = validator.validate(test);
if (errors != null && !errors.isEmpty()) {
    request.setAttribute("errors", errors);
    request.getRequestDispatcher("itemMst.jsp").forward(request, response);
    return;
}
```

### 3. 初期表示データの取得
```java
protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    // 物品カテゴリーの取得
    ItemMstBL bl = new ItemMstBL();
    List<String> categories = bl.getCategories();
    request.setAttribute("categories", categories);

    // 物品マスタページへ遷移
    request.getRequestDispatcher("itemMst.jsp").forward(request, response);
}
```

### 4. ログ出力への置き換え
```java
private static final Logger log = LoggerFactory.getLogger(ItemMstServlet.class);

protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    log.info("Accessing item master page (POST)");
    // ...
}
```

### 5. エラーハンドリング
```java
try {
    // 処理
} catch (Exception e) {
    log.error("Error in ItemMstServlet", e);
    request.setAttribute("error", "物品マスタの処理中にエラーが発生しました");
    request.getRequestDispatcher("error.jsp").forward(request, response);
}
```

### 6. DTO/フォームクラスの整備
```java
// Testクラスを適切な名前に変更
public class Item {
    private String itemCode;
    private String itemName;
    private String category;
    private int unitPrice;
    // ...
}

public class ItemForm extends BaseValidator {
    private String itemCode;
    private String itemName;
    // ... バリデーション機能
}
```

### 7. 検索機能の追加
```java
// 物品検索
String keyword = request.getParameter("keyword");
String category = request.getParameter("category");

List<Item> searchResults = bl.searchItems(keyword, category);
request.setAttribute("itemList", searchResults);
```

### 8. REST APIへのリファクタリング
```java
@WebServlet("/api/items/*")
public class ItemMstServlet extends HttpServlet {
    // RESTful API実装
    protected void doGet() { /* 取得 */ }
    protected void doPost() { /* 作成 */ }
    protected void doPut() { /* 更新 */ }
    protected void doDelete() { /* 削除 */ }
}
```

## セキュリティ考慮事項
- 認証・認可の実装が必要
- マスタデータの変更権限チェック
- 入力値のサニタイズ
- CSRF対策

## パフォーマンス考慮事項
- 物品データが大量の場合、ページネーションが必須
- カテゴリーデータのキャッシュ
- インデックスの適切な設定

## コメントの解釈
- "TODO Auto-generated" コメント: 実装が未完成
- コンソール出力: デバッグ用の一時的なコード

## まとめ
ItemMstServletは物品マスタ管理機能の基本的な枠組みのみを提供する未完成のサーブレットです。実際の物品CRUD操作、ItemValidator の活用、Test DTO の適切な命名など、今後の開発で多くの機能実装が必要です。
