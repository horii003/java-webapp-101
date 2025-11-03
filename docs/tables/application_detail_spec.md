# 購入申請明細（application_detail）

## テーブル概要

### テーブル論理名
購入申請明細

### テーブル物理名
application_detail

### 用途
購入申請の物品明細を管理するトランザクションテーブル。申請番号と明細番号の複合キーで管理する。

### 実装状況
❌ 未実装（今後実装予定）

---

## テーブル定義

| No. | カラム論理名 | カラム物理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|-----|------------|-------------|---------|------|------|----|----|------------|------|
| 1 | 申請番号 | appd_app_id | INT | 10 | × | ○ | ○ | - | 購入申請ヘッダの申請番号 |
| 2 | 明細番号 | appd_line_no | INT | 3 | × | ○ | - | - | 明細の連番（1から採番） |
| 3 | 物品コード | appd_item_code | INT | 3 | × | - | ○ | - | 物品マスタの物品コード |
| 4 | 数量 | appd_quantity | INT | 5 | × | - | - | 1 | 購入数量 |
| 5 | 単価 | appd_unit_price | INT | 6 | × | - | - | - | 購入時の単価（税抜） |
| 6 | 金額 | appd_amount | INT | 10 | × | - | - | - | 明細金額（数量×単価） |
| 7 | 備考 | appd_remarks | VARCHAR | 200 | ○ | - | - | - | 明細の備考 |
| 8 | 登録日時 | created_at | DATETIME | - | × | - | - | CURRENT_TIMESTAMP | レコード登録日時 |
| 9 | 更新日時 | updated_at | DATETIME | - | × | - | - | CURRENT_TIMESTAMP | レコード更新日時 |

---

## インデックス

### 主キーインデックス
- **PRIMARY KEY**: (appd_app_id, appd_line_no)

### 外部キーインデックス
- appd_app_id（申請番号検索用）
- appd_item_code（物品コード検索用）

### 複合インデックス
- (appd_app_id, appd_line_no)（主キー）
- (appd_item_code, appd_app_id)（物品別の申請検索用）

---

## 制約

### 主キー制約
- **複合主キー**: (appd_app_id, appd_line_no)

### 外部キー制約
- **appd_app_id** → application_header.app_id（購入申請ヘッダ）
  - 参照整合性: CASCADE（ヘッダ削除時に明細も削除）
- **appd_item_code** → item.item_code（物品マスタ）
  - 参照整合性: RESTRICT（使用中の物品は削除不可）

### NOT NULL制約
- appd_app_id（申請番号）
- appd_line_no（明細番号）
- appd_item_code（物品コード）
- appd_quantity（数量）
- appd_unit_price（単価）
- appd_amount（金額）
- created_at（登録日時）
- updated_at（更新日時）

### CHECK制約
- appd_quantity > 0（数量は1以上）
- appd_unit_price >= 0（単価は0以上）
- appd_amount >= 0（金額は0以上）
- appd_line_no > 0（明細番号は1以上）

---

## 補足事項

### 設計上の注意点
- 複合主キー（appd_app_id, appd_line_no）を使用
- appd_line_no は各申請内で1から採番
- appd_amount は appd_quantity × appd_unit_price で自動計算
- 単価は申請時の物品マスタの単価をコピーして保持（履歴管理）

### 金額計算ロジック
```
appd_amount = appd_quantity × appd_unit_price
```
- トリガーまたはアプリケーションロジックで自動計算
- 手動入力は不可

---

## 使用箇所（想定）

### DAO
- ApplicationDetailDAO（今後実装）

### BL（ビジネスロジック）
- ApplicationBL（今後実装）

### DTO
- ApplicationDetail（今後実装）

### Form
- ApplicationDetailForm（今後実装）

### 画面
- SC-004（購入申請書作成）
- SC-005（申請履歴表示）

---

## DDL

```sql
CREATE TABLE refresh.application_detail (
    appd_app_id INT(10) NOT NULL,
    appd_line_no INT(3) NOT NULL,
    appd_item_code INT(3) NOT NULL,
    appd_quantity INT(5) NOT NULL DEFAULT 1,
    appd_unit_price INT(6) NOT NULL,
    appd_amount INT(10) NOT NULL,
    appd_remarks VARCHAR(200),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (appd_app_id, appd_line_no),
    CONSTRAINT fk_appd_app_id FOREIGN KEY (appd_app_id) REFERENCES application_header(app_id) ON DELETE CASCADE,
    CONSTRAINT fk_appd_item_code FOREIGN KEY (appd_item_code) REFERENCES item(item_code) ON DELETE RESTRICT,
    CONSTRAINT chk_appd_quantity CHECK (appd_quantity > 0),
    CONSTRAINT chk_appd_unit_price CHECK (appd_unit_price >= 0),
    CONSTRAINT chk_appd_amount CHECK (appd_amount >= 0),
    CONSTRAINT chk_appd_line_no CHECK (appd_line_no > 0)
);

-- インデックス作成
CREATE INDEX idx_appd_app_id ON application_detail(appd_app_id);
CREATE INDEX idx_appd_item_code ON application_detail(appd_item_code);
CREATE INDEX idx_appd_item_app ON application_detail(appd_item_code, appd_app_id);
```

---

## サンプルデータ

```sql
-- 申請番号1の明細
INSERT INTO application_detail (appd_app_id, appd_line_no, appd_item_code, appd_quantity, appd_unit_price, appd_amount, appd_remarks)
VALUES
(1, 1, 1, 2, 1200, 2400, 'オフィス用'),
(1, 2, 2, 3, 800, 2400, '会議室用');

-- 申請番号2の明細
INSERT INTO application_detail (appd_app_id, appd_line_no, appd_item_code, appd_quantity, appd_unit_price, appd_amount, appd_remarks)
VALUES
(2, 1, 1, 10, 1200, 12000, '開発チーム用'),
(2, 2, 2, 5, 800, 4000, 'テストチーム用');
```

---

## データメンテナンス方針

### バックアップ
- トランザクションデータとして日次バックアップ対象
- ヘッダテーブルと一緒にバックアップ

### データ保持期間
- 5年間保持（ヘッダテーブルと同じ）
- 5年経過後はアーカイブテーブルへ移動

### 更新頻度
- 高頻度（申請作成・修正時）

---

## トリガー設計

### 金額の自動計算
```sql
CREATE TRIGGER calculate_amount_insert
BEFORE INSERT ON application_detail
FOR EACH ROW
SET NEW.appd_amount = NEW.appd_quantity * NEW.appd_unit_price;

CREATE TRIGGER calculate_amount_update
BEFORE UPDATE ON application_detail
FOR EACH ROW
SET NEW.appd_amount = NEW.appd_quantity * NEW.appd_unit_price;
```

### ヘッダの合計金額更新
```sql
CREATE TRIGGER update_header_total_insert
AFTER INSERT ON application_detail
FOR EACH ROW
UPDATE application_header
SET app_total = (
    SELECT SUM(appd_amount)
    FROM application_detail
    WHERE appd_app_id = NEW.appd_app_id
)
WHERE app_id = NEW.appd_app_id;

CREATE TRIGGER update_header_total_update
AFTER UPDATE ON application_detail
FOR EACH ROW
UPDATE application_header
SET app_total = (
    SELECT SUM(appd_amount)
    FROM application_detail
    WHERE appd_app_id = NEW.appd_app_id
)
WHERE app_id = NEW.appd_app_id;

CREATE TRIGGER update_header_total_delete
AFTER DELETE ON application_detail
FOR EACH ROW
UPDATE application_header
SET app_total = (
    SELECT IFNULL(SUM(appd_amount), 0)
    FROM application_detail
    WHERE appd_app_id = OLD.appd_app_id
)
WHERE app_id = OLD.appd_app_id;
```

---

## ビジネスルール

### 明細作成ルール
1. 申請番号（appd_app_id）は必須
2. 明細番号（appd_line_no）は各申請内で1から連番
3. 物品コード（appd_item_code）は物品マスタに存在する必要がある
4. 数量（appd_quantity）は1以上
5. 単価（appd_unit_price）は物品マスタから自動取得

### 明細更新ルール
1. 数量または単価が変更された場合、金額を再計算
2. 金額が変更された場合、ヘッダの合計金額を更新

### 明細削除ルール
1. 明細削除時、ヘッダの合計金額を再計算
2. 最後の明細を削除する場合、ヘッダも削除することを推奨

### 単価の履歴管理
- 物品マスタの単価が変更されても、過去の申請明細の単価は変更しない
- 申請時の単価をスナップショットとして保持

---

## リレーションシップ

### 親テーブル
- **application_header（購入申請ヘッダ）**
  - リレーション: appd_app_id → application_header.app_id
  - カーディナリティ: 多対1
  - 削除時の動作: CASCADE（ヘッダ削除時に明細も削除）

- **item（物品マスタ）**
  - リレーション: appd_item_code → item.item_code
  - カーディナリティ: 多対1
  - 削除時の動作: RESTRICT（使用中の物品は削除不可）

---

## パフォーマンスチューニング

### パーティショニング
申請番号（appd_app_id）でパーティショニングを検討（ヘッダテーブルと同じパーティション戦略）

### クエリ最適化
- 申請番号での検索を最適化（主キーの一部）
- 物品コードでの集計クエリを最適化（インデックス使用）

---

## ビュー設計

### 申請明細一覧ビュー
```sql
CREATE VIEW v_application_detail_list AS
SELECT
    ad.appd_app_id,
    ad.appd_line_no,
    i.item_name,
    ad.appd_quantity,
    ad.appd_unit_price,
    ad.appd_amount,
    ad.appd_remarks
FROM application_detail ad
INNER JOIN item i ON ad.appd_item_code = i.item_code
ORDER BY ad.appd_app_id, ad.appd_line_no;
```

### 物品別購入履歴ビュー
```sql
CREATE VIEW v_item_purchase_history AS
SELECT
    i.item_code,
    i.item_name,
    COUNT(DISTINCT ad.appd_app_id) AS purchase_count,
    SUM(ad.appd_quantity) AS total_quantity,
    SUM(ad.appd_amount) AS total_amount
FROM application_detail ad
INNER JOIN item i ON ad.appd_item_code = i.item_code
INNER JOIN application_header ah ON ad.appd_app_id = ah.app_id
WHERE ah.app_status = '承認済'
GROUP BY i.item_code, i.item_name;
```

---

## データ整合性チェック

### 金額の整合性チェック
```sql
-- 明細の金額が正しく計算されているかチェック
SELECT *
FROM application_detail
WHERE appd_amount != appd_quantity * appd_unit_price;

-- ヘッダの合計金額が明細の合計と一致するかチェック
SELECT
    ah.app_id,
    ah.app_total AS header_total,
    IFNULL(SUM(ad.appd_amount), 0) AS detail_total
FROM application_header ah
LEFT JOIN application_detail ad ON ah.app_id = ad.appd_app_id
GROUP BY ah.app_id, ah.app_total
HAVING ah.app_total != IFNULL(SUM(ad.appd_amount), 0);
```

---

## 統計情報

### 推奨される統計情報の収集
```sql
-- テーブル統計の更新
ANALYZE TABLE application_detail;

-- インデックス統計の確認
SHOW INDEX FROM application_detail;
```

---

## 作成日
2025-11-03

## 最終更新日
2025-11-03
