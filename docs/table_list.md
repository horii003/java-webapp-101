# テーブル一覧

## システム名
物品管理システム

## データベース名
refresh

## DBMS
MySQL

## 作成日
2025-11-03

---

## テーブル一覧表

| No. | テーブル論理名 | テーブル物理名 | 用途 | 実装状況 | 備考 |
|-----|---------------|---------------|------|---------|------|
| 1 | 社員情報マスタ | pers | 社員の基本情報を管理 | ✅ 実装済み | |
| 2 | 物品マスタ | item | 物品の基本情報を管理 | ✅ テーブルのみ | 業務ロジック未実装 |
| 3 | 購入申請ヘッダ | - | 購入申請の基本情報 | ❌ 未実装 | 今後実装予定 |
| 4 | 購入申請明細 | - | 購入申請の物品明細 | ❌ 未実装 | 今後実装予定 |

---

## テーブル詳細

### 1. 社員情報マスタ（pers）

#### 概要
社員の基本情報を管理するマスタテーブル。社員番号をキーとして、氏名、所属部署、グループなどの情報を保持する。

#### テーブル定義

| No. | カラム論理名 | カラム物理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|-----|------------|-------------|---------|------|------|----|----|------------|------|
| 1 | 社員番号 | pers_employee | VARCHAR | 4 | × | ○ | - | - | 社員を一意に識別する番号 |
| 2 | OA番号 | pers_oano | VARCHAR | 7 | ○ | - | - | - | OAシステムの社員番号 |
| 3 | 姓 | pers_sei | VARCHAR | 10 | ○ | - | - | - | 姓（現在未使用） |
| 4 | 名 | pers_mei | VARCHAR | 10 | ○ | - | - | - | 名（現在未使用） |
| 5 | 氏名（漢字） | pers_name | VARCHAR | 22 | ○ | - | - | - | フルネーム（漢字） |
| 6 | 氏名（カナ） | pers_namek | VARCHAR | 21 | ○ | - | - | - | フルネーム（カナ） |
| 7 | 所属部署 | pers_bu | VARCHAR | 20 | ○ | - | - | - | 所属する部署名 |
| 8 | 所属グループ | pers_gr | VARCHAR | 30 | ○ | - | - | - | 所属するグループ名 |
| 9 | 登録日 | pers_indate | VARCHAR | 8 | ○ | - | - | - | レコード登録日（yyyyMMdd形式） |
| 10 | 登録時刻 | pers_intime | VARCHAR | 6 | ○ | - | - | - | レコード登録時刻（HHmmss形式） |
| 11 | 更新日 | pers_update | VARCHAR | 8 | ○ | - | - | - | レコード更新日（yyyyMMdd形式） |
| 12 | 更新時刻 | pers_uptime | VARCHAR | 6 | ○ | - | - | - | レコード更新時刻（HHmmss形式） |

#### インデックス
- **PRIMARY KEY**: pers_employee

#### 制約
- **主キー制約**: pers_employee（社員番号）

#### 補足
- 姓（pers_sei）と名（pers_mei）は定義されているが、現在のアプリケーションでは使用されていない
- 日付・時刻カラムは文字列型（VARCHAR）で保存
- 登録日時と更新日時を別々のカラムで管理（監査用）

#### 使用箇所
- **DAO**: EmployeeDAO
- **BL**: EmployeeMstBL
- **DTO**: Employee
- **Form**: EmployeeForm
- **画面**: SC-002（社員マスタ）、SC-003（社員マスタ一覧）

#### DDL
```sql
CREATE TABLE refresh.pers (
    pers_employee VARCHAR(4) PRIMARY KEY,
    pers_oano VARCHAR(7),
    pers_sei VARCHAR(10),
    pers_mei VARCHAR(10),
    pers_name VARCHAR(22),
    pers_namek VARCHAR(21),
    pers_bu VARCHAR(20),
    pers_gr VARCHAR(30),
    pers_indate VARCHAR(8),
    pers_intime VARCHAR(6),
    pers_update VARCHAR(8),
    pers_uptime VARCHAR(6)
);
```

#### サンプルデータ
```sql
INSERT INTO pers (pers_employee, pers_oano, pers_sei, pers_mei, pers_name, pers_namek, pers_bu, pers_gr, pers_indate, pers_intime)
VALUES
('0001', '0250001', '', '', '山田太郎', 'ヤマダタロウ', 'システム開発部', 'SIG', '20240101', '090000'),
('0002', '0250002', '', '', '佐藤花子', 'サトウハナコ', 'ラボシステム部', '運用G', '20240101', '090000');
```

---

### 2. 物品マスタ（item）

#### 概要
購入可能な物品の基本情報を管理するマスタテーブル。物品コードをキーとして、品名、品番、単価などの情報を保持する。

#### テーブル定義

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

#### インデックス
- **PRIMARY KEY**: item_code

#### 制約
- **主キー制約**: item_code（物品コード）

#### 補足
- カラム名に命名の不統一あり（itemcuts_to のみ item_ が抜けている）
- 日付型ではなく文字列型を使用
- item_indate の桁数が6桁（pers テーブルは8桁）で不統一
- カット関連のカラムは販売中止期間を管理するための項目と思われる

#### 使用箇所
- **DAO**: 未実装
- **BL**: 未実装
- **DTO**: Test（本来は Item という名前にすべき）
- **Form**: 未実装
- **画面**: SC-006（物品マスタ）、SC-004（購入申請書作成）

#### DDL
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

#### サンプルデータ
```sql
INSERT INTO item (item_code, item_hin, item_name, item_askul, item_page, item_tank, item_indate, item_intime)
VALUES
(1, 'ベージュ', 'コーヒー', '123456789', 343, 1200, '240101', '090000'),
(2, 'ネイビー', 'お茶', '987654321', 344, 800, '240101', '090000');
```

---

### 3. 購入申請ヘッダ（未実装）

#### 概要（想定）
購入申請の基本情報を管理するトランザクションテーブル。申請番号をキーとして、申請者、申請日、合計金額などの情報を保持する。

#### テーブル定義（想定）

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

#### 外部キー
- app_employee → pers.pers_employee（申請者）
- app_approver → pers.pers_employee（承認者）

---

### 4. 購入申請明細（未実装）

#### 概要（想定）
購入申請の物品明細を管理するトランザクションテーブル。申請番号と明細番号の複合キーで管理する。

#### テーブル定義（想定）

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

#### インデックス
- **PRIMARY KEY**: (appd_app_id, appd_line_no)

#### 外部キー
- appd_app_id → application_header.app_id（購入申請ヘッダ）
- appd_item_code → item.item_code（物品マスタ）

---

## テーブル関連図

```
┌─────────────────┐
│   pers          │
│ （社員情報）     │
│ PK: pers_employee│
└─────────────────┘
        │ 1
        │
        │ *
┌───────┴─────────────────┐
│   application_header    │
│  （購入申請ヘッダ）      │
│  PK: app_id             │
│  FK: app_employee       │
│  FK: app_approver       │
└─────────────────────────┘
        │ 1
        │
        │ *
┌───────┴─────────────────┐
│   application_detail    │
│  （購入申請明細）        │
│  PK: (appd_app_id,      │
│       appd_line_no)     │
│  FK: appd_app_id        │
│  FK: appd_item_code     │
└─────────────────────────┘
        │ *
        │
        │ 1
┌───────┴─────────┐
│   item          │
│ （物品マスタ）   │
│ PK: item_code   │
└─────────────────┘
```

---

## データベース設計上の課題

### 1. データ型の問題
**現状**:
- 日付・時刻カラムが VARCHAR 型で定義
- 数値カラムが VARCHAR 型の場合がある

**改善提案**:
- DATE型、DATETIME型、TIMESTAMP型の使用
- 適切な数値型（INT、DECIMAL）の使用

### 2. 命名規則の不統一
**現状**:
- itemcuts_to のみ item_ プレフィックスが抜けている
- 登録日時のカラム名が不統一（indate/indateなど桁数も異なる）

**改善提案**:
- 統一された命名規則の適用
- テーブルプレフィックスの一貫性

### 3. 監査情報の不足
**現状**:
- 登録者、更新者の情報がない
- 論理削除の仕組みがない

**改善提案**:
- created_by、updated_by カラムの追加
- deleted_at カラムの追加（論理削除用）

### 4. 正規化の課題
**現状**:
- 部署、グループがマスタ化されていない
- ステータスがマスタ化されていない

**改善提案**:
- 部署マスタ、グループマスタの作成
- ステータスマスタの作成

---

## 推奨される追加テーブル

### 1. 部署マスタ
部署情報を管理するマスタテーブル

### 2. グループマスタ
グループ情報を管理するマスタテーブル

### 3. ステータスマスタ
申請ステータスを管理するマスタテーブル

### 4. ユーザーマスタ
ログインユーザー情報を管理するマスタテーブル

### 5. 権限マスタ
システム権限を管理するマスタテーブル

### 6. ログテーブル
システム操作ログを記録するテーブル

---

## データメンテナンス方針

### バックアップ
- 日次フルバックアップ
- トランザクションログのバックアップ

### データ保持期間
- マスタデータ：削除しない（論理削除）
- トランザクションデータ：5年間保持

### アーカイブ
- 5年以上経過したデータはアーカイブテーブルへ移動

---

## パフォーマンスチューニング

### インデックス設計
**現在の状況**:
- 主キーインデックスのみ

**推奨される追加インデックス**:
- pers.pers_bu（部署検索用）
- pers.pers_gr（グループ検索用）
- item.item_name（物品名検索用）
- application_header.app_employee（申請者検索用）
- application_header.app_date（申請日検索用）

### クエリ最適化
- WHERE句で使用するカラムにインデックス作成
- 結合キーにインデックス作成
- EXPLAIN を使用したクエリプラン確認
