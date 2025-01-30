# Employee.java

## 概要
このクラスは社員情報を保持するDTOクラスです。Lombokアノテーションを使用して、ボイラープレートコードを削減し、データベースから取得した社員情報をオブジェクトとして扱うための機能を提供します。

## クラス構成
- パッケージ: `dto`
- Lombokアノテーション:
  - `@Getter`: ゲッターメソッドの自動生成
  - `@Setter`: セッターメソッドの自動生成
  - `@NoArgsConstructor`: 引数なしコンストラクタの生成
  - `@AllArgsConstructor`: 全フィールドを引数に持つコンストラクタの生成

## フィールド
1. 基本情報
   - `employee`: 社員番号
   - `oano`: OA番号
   - `sei`: 姓
   - `mei`: 名字
   - `nameKanji`: 氏名（漢字）
   - `namekana`: 氏名（カナ）

2. 所属情報
   - `department`: 所属部署
   - `group`: 所属グループ

3. 管理情報
   - `indate`: 作成日
   - `intime`: 作成時間
   - `update`: 更新日
   - `uptime`: 更新時間

## 主な機能

### SQLデータマッピング
- `getSQLResult(ResultSet rs)`メソッド
  - SQLクエリ結果をオブジェクトのフィールドにマッピング
  - データベースのカラム名と一致するフィールドに値を設定
  - SQLExceptionのハンドリングは呼び出し元で実施

## 特記事項
- すべてのフィールドはString型で管理
- データベースのカラム名は「pers_」プレフィックスを使用
- Lombokによるコード生成で冗長性を排除
