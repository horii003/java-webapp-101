# HistoryViewServlet.java

## 概要
このサーブレットは購入履歴参照機能を提供するサーブレットクラスです。HttpServletを継承し、WebServletアノテーションを使用してURLマッピングを行っています。

## 基本情報
- URLマッピング: `/historyView`
- 継承クラス: `javax.servlet.http.HttpServlet`
- シリアルバージョンUID: 1L

## 主な機能

### GETリクエスト処理
- `doGet()`メソッド
  - 購入履歴参照ページ（historyView.jsp）への遷移を処理
  - リクエストディスパッチャーを使用してフォワード処理を実行

### POSTリクエスト処理
- `doPost()`メソッド
  - GETリクエストと同じ処理を実行
  - doGet()メソッドに処理を委譲

## 特記事項
- シンプルなページ遷移処理のみを実装
- 履歴データの取得や表示ロジックはJSPファイルに委譲
- GET/POSTどちらのリクエストでも同じ処理を実行
