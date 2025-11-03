# ER図（Entity Relationship Diagram）

## システム名
物品管理システム

## データベース名
refresh

## 作成日
2025-11-03

---

## 現在実装されているテーブルのER図

```mermaid
erDiagram
    pers {
        VARCHAR(4) pers_employee PK "社員番号"
        VARCHAR(7) pers_oano "OA番号"
        VARCHAR(10) pers_sei "姓"
        VARCHAR(10) pers_mei "名"
        VARCHAR(22) pers_name "氏名(漢字)"
        VARCHAR(21) pers_namek "氏名(カナ)"
        VARCHAR(20) pers_bu "所属部署"
        VARCHAR(30) pers_gr "所属グループ"
        VARCHAR(8) pers_indate "登録日"
        VARCHAR(6) pers_intime "登録時刻"
        VARCHAR(8) pers_update "更新日"
        VARCHAR(6) pers_uptime "更新時刻"
    }

    item {
        INT(3) item_code PK "物品コード"
        VARCHAR(100) item_hin "品番"
        VARCHAR(40) item_name "品名"
        VARCHAR(10) item_askul "ASKUL申込番号"
        INT(4) item_page "カタログページ"
        INT(6) item_tank "単価"
        VARCHAR(6) item_indate "登録日"
        VARCHAR(6) item_intime "登録時刻"
        VARCHAR(8) item_update "更新日"
        VARCHAR(6) item_uptime "更新時刻"
        VARCHAR(8) item_cuts_from "カット開始日"
        VARCHAR(8) itemcuts_to "カット終了日"
        VARCHAR(6) item_cutstank "カット単価"
    }
```

**注**: 現在、persテーブルとitemテーブルの間にリレーションシップは存在しません。

---

## 完全なシステムER図（想定）

```mermaid
erDiagram
    pers ||--o{ application_header : "申請する"
    pers ||--o{ application_header : "承認する"
    application_header ||--|{ application_detail : "含む"
    item ||--o{ application_detail : "選択される"

    pers {
        VARCHAR(4) pers_employee PK "社員番号"
        VARCHAR(7) pers_oano "OA番号"
        VARCHAR(10) pers_sei "姓"
        VARCHAR(10) pers_mei "名"
        VARCHAR(22) pers_name "氏名(漢字)"
        VARCHAR(21) pers_namek "氏名(カナ)"
        VARCHAR(20) pers_bu "所属部署"
        VARCHAR(30) pers_gr "所属グループ"
        VARCHAR(8) pers_indate "登録日"
        VARCHAR(6) pers_intime "登録時刻"
        VARCHAR(8) pers_update "更新日"
        VARCHAR(6) pers_uptime "更新時刻"
    }

    item {
        INT(3) item_code PK "物品コード"
        VARCHAR(100) item_hin "品番"
        VARCHAR(40) item_name "品名"
        VARCHAR(10) item_askul "ASKUL申込番号"
        INT(4) item_page "カタログページ"
        INT(6) item_tank "単価"
        VARCHAR(6) item_indate "登録日"
        VARCHAR(6) item_intime "登録時刻"
        VARCHAR(8) item_update "更新日"
        VARCHAR(6) item_uptime "更新時刻"
        VARCHAR(8) item_cuts_from "カット開始日"
        VARCHAR(8) itemcuts_to "カット終了日"
        VARCHAR(6) item_cutstank "カット単価"
    }

    application_header {
        INT(10) app_id PK "申請番号"
        VARCHAR(4) app_employee FK "申請者社員番号"
        DATE app_date "申請日"
        TEXT app_purpose "使用目的"
        INT(10) app_total "合計金額"
        VARCHAR(20) app_status "ステータス"
        VARCHAR(4) app_approver FK "承認者社員番号"
        DATE app_approve_date "承認日"
        TEXT app_remarks "備考"
        DATETIME created_at "登録日時"
        DATETIME updated_at "更新日時"
    }

    application_detail {
        INT(10) appd_app_id PK,FK "申請番号"
        INT(3) appd_line_no PK "明細番号"
        INT(3) appd_item_code FK "物品コード"
        INT(5) appd_quantity "数量"
        INT(6) appd_unit_price "単価"
        INT(10) appd_amount "金額"
        VARCHAR(200) appd_remarks "備考"
        DATETIME created_at "登録日時"
        DATETIME updated_at "更新日時"
    }
```

---

## リレーションシップ詳細

### 1. pers（社員情報） - application_header（購入申請ヘッダ）

#### リレーション1: 申請者
- **種類**: 1対多（One to Many）
- **説明**: 1人の社員は複数の購入申請を作成できる
- **カーディナリティ**: 1 : 0..*
- **外部キー**: application_header.app_employee → pers.pers_employee
- **参照整合性**: CASCADE（社員削除時は論理削除推奨）

#### リレーション2: 承認者
- **種類**: 1対多（One to Many）
- **説明**: 1人の社員は複数の購入申請を承認できる
- **カーディナリティ**: 1 : 0..*
- **外部キー**: application_header.app_approver → pers.pers_employee
- **参照整合性**: CASCADE（社員削除時は論理削除推奨）

---

### 2. application_header（購入申請ヘッダ） - application_detail（購入申請明細）

#### リレーション
- **種類**: 1対多（One to Many）
- **説明**: 1つの購入申請は複数の物品明細を持つ
- **カーディナリティ**: 1 : 1..*（最低1明細は必要）
- **外部キー**: application_detail.appd_app_id → application_header.app_id
- **参照整合性**: CASCADE（ヘッダ削除時に明細も削除）

---

### 3. item（物品マスタ） - application_detail（購入申請明細）

#### リレーション
- **種類**: 1対多（One to Many）
- **説明**: 1つの物品は複数の申請明細で選択される
- **カーディナリティ**: 1 : 0..*
- **外部キー**: application_detail.appd_item_code → item.item_code
- **参照整合性**: RESTRICT（使用中の物品は削除不可）

---

## 拡張ER図（マスタテーブル追加版）

```mermaid
erDiagram
    pers }o--|| department : "所属"
    pers }o--|| group_mst : "所属"
    pers ||--o{ application_header : "申請"
    pers ||--o{ application_header : "承認"
    application_header }o--|| status_mst : "状態"
    application_header ||--|{ application_detail : "含む"
    item ||--o{ application_detail : "選択"
    item }o--|| category : "分類"

    pers {
        VARCHAR(4) pers_employee PK
        VARCHAR(7) pers_oano
        VARCHAR(22) pers_name
        VARCHAR(21) pers_namek
        VARCHAR(20) pers_bu FK
        VARCHAR(30) pers_gr FK
        DATETIME created_at
        DATETIME updated_at
        BOOLEAN is_deleted
    }

    department {
        VARCHAR(20) dept_code PK
        VARCHAR(50) dept_name
        INT sort_order
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    group_mst {
        VARCHAR(30) group_code PK
        VARCHAR(50) group_name
        VARCHAR(20) dept_code FK
        INT sort_order
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    item {
        INT(3) item_code PK
        VARCHAR(100) item_hin
        VARCHAR(40) item_name
        VARCHAR(10) category_code FK
        VARCHAR(10) item_askul
        INT(4) item_page
        INT(6) item_tank
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    category {
        VARCHAR(10) category_code PK
        VARCHAR(50) category_name
        INT sort_order
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }

    application_header {
        INT(10) app_id PK
        VARCHAR(4) app_employee FK
        DATE app_date
        TEXT app_purpose
        INT(10) app_total
        VARCHAR(20) app_status FK
        VARCHAR(4) app_approver FK
        DATE app_approve_date
        TEXT app_remarks
        DATETIME created_at
        DATETIME updated_at
        BOOLEAN is_deleted
    }

    application_detail {
        INT(10) appd_app_id PK,FK
        INT(3) appd_line_no PK
        INT(3) appd_item_code FK
        INT(5) appd_quantity
        INT(6) appd_unit_price
        INT(10) appd_amount
        VARCHAR(200) appd_remarks
        DATETIME created_at
        DATETIME updated_at
    }

    status_mst {
        VARCHAR(20) status_code PK
        VARCHAR(50) status_name
        INT sort_order
        BOOLEAN is_active
        DATETIME created_at
        DATETIME updated_at
    }
```

---

## エンティティ詳細

### マスタエンティティ

#### 1. pers（社員情報マスタ）
- **種類**: マスタエンティティ
- **ライフサイクル**: 長期（論理削除）
- **更新頻度**: 低
- **主な用途**: 社員情報管理、申請者・承認者の識別

#### 2. item（物品マスタ）
- **種類**: マスタエンティティ
- **ライフサイクル**: 長期（論理削除）
- **更新頻度**: 中
- **主な用途**: 購入可能物品の管理

#### 3. department（部署マスタ）
- **種類**: マスタエンティティ
- **ライフサイクル**: 長期
- **更新頻度**: 低
- **主な用途**: 組織構造の管理

#### 4. group_mst（グループマスタ）
- **種類**: マスタエンティティ
- **ライフサイクル**: 長期
- **更新頻度**: 低
- **主な用途**: 部署内グループの管理

#### 5. category（カテゴリマスタ）
- **種類**: マスタエンティティ
- **ライフサイクル**: 長期
- **更新頻度**: 低
- **主な用途**: 物品の分類管理

#### 6. status_mst（ステータスマスタ）
- **種類**: マスタエンティティ
- **ライフサイクル**: 長期
- **更新頻度**: 極低
- **主な用途**: 申請ステータスの管理

### トランザクションエンティティ

#### 7. application_header（購入申請ヘッダ）
- **種類**: トランザクションエンティティ
- **ライフサイクル**: 中期（5年保持）
- **更新頻度**: 高
- **主な用途**: 購入申請の基本情報管理

#### 8. application_detail（購入申請明細）
- **種類**: トランザクションエンティティ
- **ライフサイクル**: 中期（5年保持）
- **更新頻度**: 高
- **主な用途**: 購入申請の物品明細管理

---

## 正規化レベル

### 現在の正規化状態

#### persテーブル
- **第1正規形**: ✅ 達成（繰り返し項目なし）
- **第2正規形**: ✅ 達成（部分関数従属性なし）
- **第3正規形**: ❌ 未達成（部署、グループが推移的関数従属）

#### itemテーブル
- **第1正規形**: ✅ 達成
- **第2正規形**: ✅ 達成
- **第3正規形**: ❌ 未達成（カテゴリ情報が含まれる可能性）

### 正規化の改善提案

#### 第3正規形への改善
1. 部署マスタ、グループマスタの分離
2. カテゴリマスタの分離
3. ステータスマスタの分離

これにより：
- データの一貫性向上
- 更新異常の防止
- メンテナンス性の向上

---

## インデックス設計

### 主キーインデックス
- pers.pers_employee
- item.item_code
- application_header.app_id
- application_detail.(appd_app_id, appd_line_no)

### 外部キーインデックス
- application_header.app_employee
- application_header.app_approver
- application_detail.appd_app_id
- application_detail.appd_item_code

### 検索用インデックス
- pers.pers_bu（部署検索）
- pers.pers_gr（グループ検索）
- pers.pers_name（氏名検索）
- item.item_name（物品名検索）
- application_header.app_date（申請日検索）
- application_header.app_status（ステータス検索）

---

## データ整合性制約

### 主キー制約
すべてのテーブルに主キー制約を設定

### 外部キー制約
関連するテーブル間に外部キー制約を設定

### NOT NULL制約
必須項目にNOT NULL制約を設定

### CHECK制約
- app_total >= 0（合計金額は0以上）
- appd_quantity > 0（数量は1以上）
- appd_unit_price >= 0（単価は0以上）

### UNIQUE制約
- pers.pers_oano（OA番号の一意性）
- item.item_askul（ASKUL番号の一意性、NULL許可）

---

## トリガー設計

### 更新日時の自動更新
```sql
CREATE TRIGGER update_timestamp_pers
BEFORE UPDATE ON pers
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
```

### 合計金額の自動計算
```sql
CREATE TRIGGER calculate_total
AFTER INSERT OR UPDATE OR DELETE ON application_detail
FOR EACH ROW
UPDATE application_header
SET app_total = (
    SELECT SUM(appd_amount)
    FROM application_detail
    WHERE appd_app_id = NEW.appd_app_id
)
WHERE app_id = NEW.appd_app_id;
```

---

## ビュー設計

### 社員情報ビュー
```sql
CREATE VIEW v_employee_info AS
SELECT
    p.pers_employee,
    p.pers_name,
    p.pers_namek,
    d.dept_name,
    g.group_name
FROM pers p
LEFT JOIN department d ON p.pers_bu = d.dept_code
LEFT JOIN group_mst g ON p.pers_gr = g.group_code
WHERE p.is_deleted = FALSE;
```

### 申請一覧ビュー
```sql
CREATE VIEW v_application_list AS
SELECT
    ah.app_id,
    ah.app_date,
    p1.pers_name AS applicant_name,
    ah.app_purpose,
    ah.app_total,
    s.status_name,
    p2.pers_name AS approver_name,
    ah.app_approve_date
FROM application_header ah
INNER JOIN pers p1 ON ah.app_employee = p1.pers_employee
LEFT JOIN pers p2 ON ah.app_approver = p2.pers_employee
INNER JOIN status_mst s ON ah.app_status = s.status_code
WHERE ah.is_deleted = FALSE;
```

---

## パフォーマンスチューニング

### パーティショニング
大量データが蓄積されるテーブルのパーティショニング検討
- application_header: 申請日でパーティション
- application_detail: 申請番号でパーティション

### クエリ最適化
- EXPLAINを使用したクエリプラン確認
- 適切なインデックスの作成
- 結合順序の最適化

### キャッシュ戦略
- マスタデータのアプリケーションキャッシュ
- クエリ結果のキャッシュ

---

## データマイグレーション

### 既存データの移行
現在のVARCHAR型の日付データをDATE/DATETIME型に変換

```sql
-- 例: pers_indate (VARCHAR) から created_at (DATETIME) への変換
UPDATE pers
SET created_at = STR_TO_DATE(
    CONCAT(pers_indate, pers_intime),
    '%Y%m%d%H%i%s'
);
```

---

## まとめ

このER図は、物品管理システムの現在の状態と将来の拡張を示しています。

### 現状
- 2つの独立したマスタテーブル（pers、item）
- リレーションシップなし
- データ型や正規化に課題あり

### 将来の姿
- 適切な正規化（第3正規形）
- 明確なリレーションシップ
- マスタテーブルの分離
- トランザクションテーブルの追加
- データ整合性の確保

これにより、保守性、拡張性、パフォーマンスが向上します。
