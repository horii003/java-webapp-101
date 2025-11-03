# 購入申請ヘッダ（application_header）

## テーブル概要

### テーブル論理名
購入申請ヘッダ

### テーブル物理名
application_header

### 用途
購入申請の基本情報を管理するトランザクションテーブル。申請番号をキーとして、申請者、申請日、合計金額などの情報を保持する。

### 実装状況
❌ 未実装（今後実装予定）

---

## テーブル定義

| No. | カラム論理名 | カラム物理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|-----|------------|-------------|---------|------|------|----|----|------------|------|
| 1 | 申請番号 | app_id | INT | 10 | × | ○ | - | AUTO_INCREMENT | 申請を一意に識別する番号 |
| 2 | 申請者社員番号 | app_employee | VARCHAR | 4 | × | - | ○ | - | 申請者の社員番号（pers.pers_employee） |
| 3 | 申請日 | app_date | DATE | - | × | - | - | CURRENT_DATE | 申請日 |
| 4 | 使用目的 | app_purpose | TEXT | - | × | - | - | - | 購入の使用目的 |
| 5 | 合計金額 | app_total | INT | 10 | × | - | - | 0 | 申請の合計金額（税抜） |
| 6 | ステータス | app_status | VARCHAR | 20 | × | - | - | '申請中' | 申請状態（申請中/承認済/却下/削除） |
| 7 | 承認者社員番号 | app_approver | VARCHAR | 4 | ○ | - | ○ | - | 承認者の社員番号 |
| 8 | 承認日 | app_approve_date | DATE | - | ○ | - | - | - | 承認日 |
| 9 | 備考 | app_remarks | TEXT | - | ○ | - | - | - | 備考 |
| 10 | 登録日時 | created_at | DATETIME | - | × | - | - | CURRENT_TIMESTAMP | レコード登録日時 |
| 11 | 更新日時 | updated_at | DATETIME | - | × | - | - | CURRENT_TIMESTAMP | レコード更新日時 |

---

## インデックス

### 主キーインデックス
- **PRIMARY KEY**: app_id

### 外部キーインデックス
- app_employee（申請者検索用）
- app_approver（承認者検索用）

### 検索用インデックス
- app_date（申請日検索用）
- app_status（ステータス検索用）
- (app_employee, app_date)（申請者と日付の複合検索用）

---

## 制約

### 主キー制約
- **app_id**（申請番号） - AUTO_INCREMENT

### 外部キー制約
- **app_employee** → pers.pers_employee（申請者）
  - 参照整合性: CASCADE（社員削除時は論理削除推奨）
- **app_approver** → pers.pers_employee（承認者）
  - 参照整合性: CASCADE（社員削除時は論理削除推奨）

### NOT NULL制約
- app_id（申請番号）
- app_employee（申請者社員番号）
- app_date（申請日）
- app_purpose（使用目的）
- app_total（合計金額）
- app_status（ステータス）
- created_at（登録日時）
- updated_at（更新日時）

### CHECK制約
- app_total >= 0（合計金額は0以上）
- app_status IN ('申請中', '承認済', '却下', '削除')

---

## 補足事項

### 設計上の注意点
- app_id は AUTO_INCREMENT で自動採番
- app_total は明細テーブル（application_detail）の合計から自動計算
- created_at, updated_at は TIMESTAMP 型でタイムゾーンを考慮
- 論理削除の実装を推奨（is_deleted フラグまたは app_status='削除'）

### ステータス管理
申請のライフサイクルに応じたステータス遷移：
1. **申請中**: 初期状態
2. **承認済**: 承認者による承認完了
3. **却下**: 承認者による却下
4. **削除**: 申請者または管理者による削除（論理削除）

---

## 使用箇所（想定）

### DAO
- ApplicationHeaderDAO（今後実装）

### BL（ビジネスロジック）
- ApplicationBL（今後実装）

### DTO
- ApplicationHeader（今後実装）

### Form
- ApplicationForm（今後実装）

### 画面
- SC-004（購入申請書作成）
- SC-005（申請履歴表示）

---

## DDL

```sql
CREATE TABLE refresh.application_header (
    app_id INT(10) PRIMARY KEY AUTO_INCREMENT,
    app_employee VARCHAR(4) NOT NULL,
    app_date DATE NOT NULL DEFAULT CURRENT_DATE,
    app_purpose TEXT NOT NULL,
    app_total INT(10) NOT NULL DEFAULT 0,
    app_status VARCHAR(20) NOT NULL DEFAULT '申請中',
    app_approver VARCHAR(4),
    app_approve_date DATE,
    app_remarks TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_app_employee FOREIGN KEY (app_employee) REFERENCES pers(pers_employee) ON DELETE CASCADE,
    CONSTRAINT fk_app_approver FOREIGN KEY (app_approver) REFERENCES pers(pers_employee) ON DELETE CASCADE,
    CONSTRAINT chk_app_total CHECK (app_total >= 0),
    CONSTRAINT chk_app_status CHECK (app_status IN ('申請中', '承認済', '却下', '削除'))
);

-- インデックス作成
CREATE INDEX idx_app_employee ON application_header(app_employee);
CREATE INDEX idx_app_approver ON application_header(app_approver);
CREATE INDEX idx_app_date ON application_header(app_date);
CREATE INDEX idx_app_status ON application_header(app_status);
CREATE INDEX idx_app_employee_date ON application_header(app_employee, app_date);
```

---

## サンプルデータ

```sql
INSERT INTO application_header (app_employee, app_date, app_purpose, app_total, app_status, app_approver, app_approve_date, app_remarks)
VALUES
('0001', '2025-01-15', 'オフィス備品の購入', 5000, '承認済', '0002', '2025-01-16', ''),
('0002', '2025-01-20', '開発用機材の購入', 15000, '申請中', NULL, NULL, '急ぎで必要です');
```

---

## データメンテナンス方針

### バックアップ
- トランザクションデータとして日次バックアップ対象

### データ保持期間
- 5年間保持
- 5年経過後はアーカイブテーブルへ移動

### 更新頻度
- 高頻度（申請・承認時）

---

## トリガー設計

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

### 更新日時の自動更新
```sql
CREATE TRIGGER update_timestamp
BEFORE UPDATE ON application_header
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
```

---

## ビジネスルール

### 申請作成ルール
1. 申請者（app_employee）は必須
2. 使用目的（app_purpose）は必須
3. 申請日（app_date）はデフォルトで当日
4. 初期ステータスは「申請中」

### 承認ルール
1. 承認時に app_approver と app_approve_date を設定
2. ステータスを「承認済」に更新
3. 承認者は申請者と異なる必要がある

### 却下ルール
1. 却下時にステータスを「却下」に更新
2. 却下理由は app_remarks に記録

### 削除ルール
1. 論理削除を推奨（ステータスを「削除」に設定）
2. 物理削除の場合、関連する明細も CASCADE で削除

---

## リレーションシップ

### 親テーブル
- **pers（社員情報マスタ）**
  - リレーション1: app_employee → pers.pers_employee（申請者）
  - カーディナリティ: 多対1
  - リレーション2: app_approver → pers.pers_employee（承認者）
  - カーディナリティ: 多対1

### 子テーブル
- **application_detail（購入申請明細）**
  - リレーション: app_id → application_detail.appd_app_id
  - カーディナリティ: 1対多
  - 削除時の動作: CASCADE（ヘッダ削除時に明細も削除）

---

## パフォーマンスチューニング

### パーティショニング
大量データが蓄積される場合、申請日（app_date）でパーティショニングを検討

```sql
PARTITION BY RANGE (YEAR(app_date)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027)
);
```

---

## ビュー設計

### 申請一覧ビュー
```sql
CREATE VIEW v_application_list AS
SELECT
    ah.app_id,
    ah.app_date,
    p1.pers_name AS applicant_name,
    ah.app_purpose,
    ah.app_total,
    ah.app_status,
    p2.pers_name AS approver_name,
    ah.app_approve_date
FROM application_header ah
INNER JOIN pers p1 ON ah.app_employee = p1.pers_employee
LEFT JOIN pers p2 ON ah.app_approver = p2.pers_employee
WHERE ah.app_status != '削除';
```

---

## 作成日
2025-11-03

## 最終更新日
2025-11-03
