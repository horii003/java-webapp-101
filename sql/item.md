# item.sql

## 概要
このSQLファイルは物品管理システムで使用される物品（item）テーブルの作成スクリプトを定義します。物品の基本情報、ASKULカタログ情報、および各種タイムスタンプを管理するためのテーブル構造を提供します。

## テーブル定義

### テーブル名
- スキーマ名: refresh
- テーブル名: item

### カラム構成
1. `item_code` (INT(3))
   - 主キー
   - 物品コード（3桁の整数）

2. 基本情報
   - `item_hin` (VARCHAR(100))
     - 品番情報
   - `item_name` (VARCHAR(40))
     - 物品名称
   - `item_askul` (VARCHAR(10))
     - ASKULカタログ番号
   - `item_page` (INT(4))
     - カタログページ番号
   - `item_tank` (INT(6))
     - 単価情報

3. タイムスタンプ情報
   - `item_indate` (VARCHAR(6))
     - 登録日
   - `item_intime` (VARCHAR(6))
     - 登録時刻
   - `item_update` (VARCHAR(8))
     - 更新日
   - `item_uptime` (VARCHAR(6))
     - 更新時刻

4. 期間管理
   - `item_cuts_from` (VARCHAR(8))
     - 有効期間開始日
   - `itemcuts_to` (VARCHAR(8))
     - 有効期間終了日
   - `item_cutstank` (VARCHAR(6))
     - 期間管理用タンク情報

## 特記事項
- 日付・時刻はVARCHAR型で管理
- コード値は3桁の整数で管理
- ASKULカタログ情報との連携を前提とした設計
- 物品の有効期間管理機能を実装
