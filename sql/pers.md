# pers.sql

## 概要
このSQLファイルは物品管理システムで使用される社員（pers）テーブルの作成スクリプトを定義します。社員の基本情報、所属情報、および各種タイムスタンプを管理するためのテーブル構造を提供します。

## テーブル定義

### テーブル名
- スキーマ名: refresh
- テーブル名: pers

### カラム構成
1. `pers_employee` (VARCHAR(4))
   - 主キー
   - 社員番号（4桁）

2. 社員基本情報
   - `pers_oano` (VARCHAR(7))
     - OA番号
   - `pers_sei` (VARCHAR(10))
     - 姓
   - `pers_mei` (VARCHAR(10))
     - 名
   - `pers_name` (VARCHAR(22))
     - 氏名（フルネーム）
   - `pers_namek` (VARCHAR(21))
     - 氏名カナ

3. 所属情報
   - `pers_bu` (VARCHAR(20))
     - 部署名
   - `pers_gr` (VARCHAR(30))
     - グループ名

4. タイムスタンプ情報
   - `pers_indate` (VARCHAR(8))
     - 登録日
   - `pers_intime` (VARCHAR(6))
     - 登録時刻
   - `pers_update` (VARCHAR(8))
     - 更新日
   - `pers_uptime` (VARCHAR(6))
     - 更新時刻

## 特記事項
- 日付・時刻はVARCHAR型で管理
- 社員番号は4桁の文字列として管理
- 氏名は姓・名を別フィールドで保持し、結合したフルネームも保持
- 所属情報は部署とグループの2階層で管理
