# 社員情報マスタ（pers）

## テーブル概要

### テーブル論理名
社員情報マスタ

### テーブル物理名
pers

### 用途
社員の基本情報を管理するマスタテーブル。社員番号をキーとして、氏名、所属部署、グループなどの情報を保持する。

### 実装状況
✅ 実装済み

---

## テーブル定義

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

---

## インデックス

### 主キーインデックス
- **PRIMARY KEY**: pers_employee

### 推奨される追加インデックス
- pers_bu（部署検索用）
- pers_gr（グループ検索用）
- pers_name（氏名検索用）

---

## 制約

### 主キー制約
- **pers_employee**（社員番号）

### その他の制約
- 現在、外部キー制約はなし

---

## 補足事項

### 設計上の注意点
- 姓（pers_sei）と名（pers_mei）は定義されているが、現在のアプリケーションでは使用されていない
- 日付・時刻カラムは文字列型（VARCHAR）で保存
- 登録日時と更新日時を別々のカラムで管理（監査用）

### データ型の課題
- 日付・時刻カラムがVARCHAR型で定義されている
- 将来的にはDATE型、DATETIME型への変換が望ましい

---

## 使用箇所

### DAO
- EmployeeDAO

### BL（ビジネスロジック）
- EmployeeMstBL

### DTO
- Employee

### Form
- EmployeeForm

### 画面
- SC-002（社員マスタ）
- SC-003（社員マスタ一覧）

---

## DDL

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

---

## サンプルデータ

```sql
INSERT INTO pers (pers_employee, pers_oano, pers_sei, pers_mei, pers_name, pers_namek, pers_bu, pers_gr, pers_indate, pers_intime)
VALUES
('0001', '0250001', '', '', '山田太郎', 'ヤマダタロウ', 'システム開発部', 'SIG', '20240101', '090000'),
('0002', '0250002', '', '', '佐藤花子', 'サトウハナコ', 'ラボシステム部', '運用G', '20240101', '090000');
```

---

## データメンテナンス方針

### バックアップ
- マスタデータとして日次バックアップ対象

### データ保持期間
- 削除しない（論理削除の実装を推奨）

### 更新頻度
- 低頻度（社員情報の変更時のみ）

---

## 改善提案

### 1. データ型の改善
- 日付・時刻カラムをDATE型、DATETIME型に変更
- 登録日時と更新日時を統合し、TIMESTAMP型の使用を検討

### 2. 監査情報の追加
- created_by（登録者）カラムの追加
- updated_by（更新者）カラムの追加
- deleted_at（削除日時）カラムの追加（論理削除用）

### 3. 正規化の改善
- 部署マスタ、グループマスタの作成
- 外部キー制約の追加

### 4. 命名規則の統一
- 未使用のpers_sei、pers_meiカラムの削除または活用方針の決定

---

## リレーションシップ

### 将来のリレーションシップ（想定）
- application_header.app_employee → pers.pers_employee（申請者）
- application_header.app_approver → pers.pers_employee（承認者）

---

## 作成日
2025-11-03

## 最終更新日
2025-11-03
