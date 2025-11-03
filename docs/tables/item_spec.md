# 物品マスタ（item）

## テーブル概要

### テーブル論理名
物品マスタ

### テーブル物理名
item

### 用途
購入可能な物品の基本情報を管理するマスタテーブル。物品コードをキーとして、品名、品番、単価などの情報を保持する。

### 実装状況
✅ テーブルのみ実装済み（業務ロジックは未実装）

---

## テーブル定義

| No. | カラム論理名 | カラム物理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|-----|------------|-------------|---------|------|------|----|----|------------|------|
| 1 | 物品コード | item_code | INT | 3 | × | ○ | - | - | 物品を一意に識別するコード |
| 2 | 品番 | item_hin | VARCHAR | 100 | ○ | - | - | - | メーカー品番、色など |
| 3 | 品名 | item_name | VARCHAR | 40 | ○ | - | - | - | 物品の名称 |
| 4 | ASKUL申込番号 | item_askul | VARCHAR | 10 | ○ | - | - | - | ASKULカタログの申込番号 |
| 5 | カタログページ | item_page | INT | 4 | ○ | - | - | - | カタログのページ番号 |
| 6 | 単価 | item_tank | INT | 6 | ○ | - | - | - | 物品の単価（税抜） |
| 7 | 登録日 | item_indate | VARCHAR | 6 | ○ | - | - | - | レコード登録日 |
| 8 | 登録時刻 | item_intime | VARCHAR | 6 | ○ | - | - | - | レコード登録時刻 |
| 9 | 更新日 | item_update | VARCHAR | 8 | ○ | - | - | - | レコード更新日 |
| 10 | 更新時刻 | item_uptime | VARCHAR | 6 | ○ | - | - | - | レコード更新時刻 |
| 11 | カット開始日 | item_cuts_from | VARCHAR | 8 | ○ | - | - | - | 販売中止開始日 |
| 12 | カット終了日 | itemcuts_to | VARCHAR | 8 | ○ | - | - | - | 販売中止終了日 |
| 13 | カット単価 | item_cutstank | VARCHAR | 6 | ○ | - | - | - | カット時の単価 |

---

## インデックス

### 主キーインデックス
- **PRIMARY KEY**: item_code

### 推奨される追加インデックス
- item_name（物品名検索用）
- item_askul（ASKUL番号検索用）

---

## 制約

### 主キー制約
- **item_code**（物品コード）

### その他の制約
- 現在、外部キー制約はなし
- item_askul（ASKUL番号）にUNIQUE制約の追加を推奨（NULL許可）

---

## 補足事項

### 設計上の注意点
- カラム名に命名の不統一あり（itemcuts_to のみ item_ プレフィックスが抜けている）
- 日付型ではなく文字列型を使用
- item_indate の桁数が6桁（pers テーブルは8桁）で不統一
- カット関連のカラムは販売中止期間を管理するための項目と思われる

### データ型の課題
- 日付・時刻カラムがVARCHAR型で定義されている
- 単価カラムがINT型だが、将来的にはDECIMAL型への変更を検討（小数点対応）

---

## 使用箇所

### DAO
- 未実装

### BL（ビジネスロジック）
- 未実装

### DTO
- Test（本来は Item という名前にすべき）

### Form
- 未実装

### 画面
- SC-006（物品マスタ）
- SC-004（購入申請書作成）

---

## DDL

```sql
CREATE TABLE refresh.item (
    item_code INT(3) PRIMARY KEY,
    item_hin VARCHAR(100),
    item_name VARCHAR(40),
    item_askul VARCHAR(10),
    item_page INT(4),
    item_tank INT(6),
    item_indate VARCHAR(6),
    item_intime VARCHAR(6),
    item_update VARCHAR(8),
    item_uptime VARCHAR(6),
    item_cuts_from VARCHAR(8),
    itemcuts_to VARCHAR(8),
    item_cutstank VARCHAR(6)
);
```

---

## サンプルデータ

```sql
INSERT INTO item (item_code, item_hin, item_name, item_askul, item_page, item_tank, item_indate, item_intime)
VALUES
(1, 'ベージュ', 'コーヒー', '123456789', 343, 1200, '240101', '090000'),
(2, 'ネイビー', 'お茶', '987654321', 344, 800, '240101', '090000');
```

---

## データメンテナンス方針

### バックアップ
- マスタデータとして日次バックアップ対象

### データ保持期間
- 削除しない（論理削除の実装を推奨）

### 更新頻度
- 中頻度（商品の追加・変更時）

---

## 改善提案

### 1. 命名規則の統一
- itemcuts_to を item_cuts_to に修正
- item_indate の桁数を8桁に統一（yyyyMMdd形式）

### 2. データ型の改善
- 日付・時刻カラムをDATE型、DATETIME型に変更
- 単価カラムをDECIMAL(10,2)型に変更（小数点対応）
- カット単価（item_cutstank）もINT型に統一または削除

### 3. 監査情報の追加
- created_by（登録者）カラムの追加
- updated_by（更新者）カラムの追加
- is_active（有効フラグ）カラムの追加

### 4. 正規化の改善
- カテゴリマスタの作成
- category_code（カテゴリコード）外部キーカラムの追加

### 5. DTOの命名改善
- Test クラスを Item クラスにリネーム

---

## リレーションシップ

### 将来のリレーションシップ（想定）
- application_detail.appd_item_code → item.item_code（購入申請明細）
- item.category_code → category.category_code（カテゴリマスタ）

---

## ビジネスルール

### カット（販売中止）機能
- item_cuts_from から itemcuts_to までの期間、該当物品は選択不可
- カット期間中は item_cutstank の単価を適用

### 単価管理
- item_tank: 通常時の単価
- item_cutstank: カット時の特別単価（セール価格等）

---

## 参照整合性

### 削除時のルール
- 使用中（購入申請明細で参照されている）の物品は削除不可（RESTRICT）
- 論理削除の実装を推奨

---

## 作成日
2025-11-03

## 最終更新日
2025-11-03
