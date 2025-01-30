# employeeMstList.jsp

## 概要
このJSPファイルは社員マスタ情報の一覧表示を担当するページを実装します。社員の基本情報をテーブル形式で表示し、Bootstrapを使用したレスポンシブなデザインを提供します。

## 主な機能

### ページ構成
1. ヘッダー部分
   - 共通ヘッダーコンポーネントの読み込み
   - ページタイトル「社員マスタ」の表示

2. 社員一覧テーブル
   - 表示項目：
     - 社員番号
     - OA番号
     - 氏名（漢字）
     - 氏名（カナ）
     - 部署
     - 所属グループ
   - JSTL forEach文による動的データ表示

### JavaScript機能
- `getList()`関数
  - フォーム送信処理
  - 実行パラメータ（execute=select）の動的追加
  - 一覧取得のトリガー

## 使用技術
- JSP/JSTL
  - Employee DTOのインポート
  - JSTLコアタグライブラリ
- Bootstrap 3.x
  - レスポンシブグリッドシステム
  - テーブルスタイリング（striped, hover, bordered）
- jQuery 1.12.4

## 特記事項
- UTF-8文字エンコーディングを使用
- IE8対応のためのポリフィル（html5shiv, respond.js）を含む
- カスタムCSSファイル（base.css）でスタイルをカスタマイズ
- ヘッダー固定のためのパディング調整（padding-top: 65px）
- employeeListという属性名で社員リストデータを受け取り表示
