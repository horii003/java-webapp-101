# Java Webアプリケーション 仕様書一覧

## 概要
このディレクトリには、java-webapp-101プロジェクトの各ソースコードファイルの詳細な仕様書が格納されています。

## プロジェクト概要
- **プロジェクト名**: java-webapp-101
- **種類**: Java Webアプリケーション
- **アーキテクチャ**: 3層アーキテクチャ（プレゼンテーション層、ビジネスロジック層、データアクセス層）
- **主要機能**: 社員マスタ管理、物品マスタ管理、購入申請、購入履歴参照

## アーキテクチャ構成

### レイヤー構造
```
┌─────────────────────────────────────┐
│   プレゼンテーション層（Servlet）    │
│  - IndexServlet                     │
│  - EmployeeMstServlet               │
│  - ApplicationFormServlet           │
│  - HistoryViewServlet               │
│  - ItemMstServlet                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   ビジネスロジック層（BL）          │
│  - EmployeeMstBL                    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   データアクセス層（DAO）           │
│  - EmployeeDAO                      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   データベース（MySQL）             │
│  - persテーブル（社員情報）         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   補助クラス                        │
│  - DTO（Employee, Test）            │
│  - Form（EmployeeForm）             │
│  - Validator（BaseValidator）       │
│  - Connection（ConnectionManager）  │
└─────────────────────────────────────┘
```

## 仕様書一覧

### 1. サーブレット層（Servlet）

#### 1.1 IndexServlet
- **ファイル**: [IndexServlet_spec.md](./IndexServlet_spec.md)
- **役割**: トップページへの遷移
- **URL**: /index
- **実装状況**: 基本機能実装済み

#### 1.2 EmployeeMstServlet
- **ファイル**: [EmployeeMstServlet_spec.md](./EmployeeMstServlet_spec.md)
- **役割**: 社員マスタのCRUD操作
- **URL**: /employee
- **実装状況**: 完全実装済み
- **主要機能**:
  - 社員一覧表示
  - 社員情報登録
  - 社員情報更新
  - 社員情報削除
  - 社員情報検索

#### 1.3 ApplicationFormServlet
- **ファイル**: [ApplicationFormServlet_spec.md](./ApplicationFormServlet_spec.md)
- **役割**: 購入申請書作成ページへの遷移
- **URL**: /applicationForm
- **実装状況**: 基本機能のみ、詳細機能未実装

#### 1.4 HistoryViewServlet
- **ファイル**: [HistoryViewServlet_spec.md](./HistoryViewServlet_spec.md)
- **役割**: 購入履歴参照ページへの遷移
- **URL**: /historyView
- **実装状況**: 基本機能のみ、詳細機能未実装

#### 1.5 ItemMstServlet
- **ファイル**: [ItemMstServlet_spec.md](./ItemMstServlet_spec.md)
- **役割**: 物品マスタ管理ページへの遷移
- **URL**: /item
- **実装状況**: 基本機能のみ、CRUD操作未実装

### 2. ビジネスロジック層（BL）

#### 2.1 EmployeeMstBL
- **ファイル**: [EmployeeMstBL_spec.md](./EmployeeMstBL_spec.md)
- **役割**: 社員マスタのビジネスロジック
- **実装状況**: 完全実装済み
- **主要メソッド**:
  - searchEmpolyees(): 社員一覧取得（コンボボックス用）
  - searchAllEmpolyees(): 全社員情報取得（一覧表示用）
  - searchEmpolyeeById(): 特定社員情報取得
  - registerEmpolyee(): 社員情報登録
  - updateEmpolyee(): 社員情報更新
  - deleteEmpolyee(): 社員情報削除

### 3. データアクセス層（DAO）

#### 3.1 EmployeeDAO
- **ファイル**: [EmployeeDAO_spec.md](./EmployeeDAO_spec.md)
- **役割**: 社員テーブルへのデータベースアクセス
- **対象テーブル**: pers（社員情報マスタ）
- **実装状況**: 完全実装済み
- **主要メソッド**:
  - searchEmpolyees(): 社員番号と氏名の取得
  - searchAllEmpolyees(): 全社員データ取得
  - searchEmpolyeeById(): ID指定社員取得
  - registerEmployee(): 社員登録
  - updateEmployee(): 社員更新
  - deleteEmployee(): 社員削除

### 4. 接続管理

#### 4.1 ConnectionManager
- **ファイル**: [ConnectionManager_spec.md](./ConnectionManager_spec.md)
- **役割**: データベース接続管理（Singletonパターン）
- **データベース**: MySQL（refresh）
- **実装状況**: 基本機能実装済み
- **注意事項**:
  - 認証情報がハードコーディング（要改善）
  - コネクションプール未実装（要改善）

### 5. データ転送オブジェクト（DTO）

#### 5.1 Employee
- **ファイル**: [Employee_spec.md](./Employee_spec.md)
- **役割**: 社員情報を保持するDTO
- **対応テーブル**: pers
- **フィールド数**: 12（社員番号、氏名、部署、グループ等）
- **使用技術**: Lombok

#### 5.2 Test
- **ファイル**: [Test_spec.md](./Test_spec.md)
- **役割**: 用途不明のDTO（要改善）
- **実装状況**: 最小限の実装
- **問題点**: クラス名とフィールド名が不適切

### 6. フォームクラス（Form）

#### 6.1 EmployeeForm
- **ファイル**: [EmployeeForm_spec.md](./EmployeeForm_spec.md)
- **役割**: 社員情報入力フォームとバリデーション
- **継承**: BaseValidator
- **主要機能**:
  - フォームデータ保持
  - 入力値バリデーション
  - コンボボックスデータ管理
- **使用技術**: Lombok

### 7. バリデータ（Validator）

#### 7.1 BaseValidator
- **ファイル**: [BaseValidator_spec.md](./BaseValidator_spec.md)
- **役割**: 基底バリデータクラス
- **主要機能**:
  - バイト数チェック
  - 数値チェック
  - エラーメッセージ管理
- **使用技術**: Lombok

#### 7.2 ItemValidator
- **ファイル**: [ItemValidator_spec.md](./ItemValidator_spec.md)
- **役割**: 物品マスタのバリデーション
- **実装状況**: 未実装（クラス定義のみ）

## データベース構造

### persテーブル（社員情報マスタ）
| カラム名 | データ型 | 説明 | 制約 |
|---------|---------|------|------|
| pers_employee | VARCHAR | 社員番号 | 主キー |
| pers_oano | VARCHAR | OA番号 | |
| pers_sei | VARCHAR | 姓 | |
| pers_mei | VARCHAR | 名 | |
| pers_name | VARCHAR | 氏名（漢字） | |
| pers_namek | VARCHAR | 氏名（カナ） | |
| pers_bu | VARCHAR | 所属部署 | |
| pers_gr | VARCHAR | 所属グループ | |
| pers_indate | VARCHAR | 登録日（yyyyMMdd） | |
| pers_intime | VARCHAR | 登録時刻（HHmmss） | |
| pers_update | VARCHAR | 更新日（yyyyMMdd） | |
| pers_uptime | VARCHAR | 更新時刻（HHmmss） | |

## 使用技術・ライブラリ

### バックエンド
- **言語**: Java
- **フレームワーク**: Java Servlet API
- **データベース**: MySQL
- **JDBC**: MySQL Connector/J
- **ライブラリ**: Lombok

### フロントエンド
- **JSP**: JavaServer Pages
- **JavaScript**: 各種UI機能
- **CSS**: Bootstrap

### 開発ツール
- **ビルドツール**: 未確認（推測: Maven または Gradle）
- **アプリケーションサーバー**: 推測: Tomcat

## 実装状況まとめ

### 完全実装済み
- ✅ 社員マスタ管理機能
  - EmployeeMstServlet
  - EmployeeMstBL
  - EmployeeDAO
  - Employee DTO
  - EmployeeForm
  - BaseValidator

### 部分的実装
- ⚠️ トップページ表示（IndexServlet）
- ⚠️ データベース接続管理（ConnectionManager）

### 未実装・要改善
- ❌ 購入申請書機能（ApplicationFormServlet）
- ❌ 購入履歴参照機能（HistoryViewServlet）
- ❌ 物品マスタ管理機能（ItemMstServlet, ItemValidator）
- ❌ 認証・認可機能
- ❌ ログ出力機能
- ❌ エラーハンドリング

## 共通の改善提案

### セキュリティ
1. 認証・認可機能の実装
2. 認証情報の外部化（ConnectionManager）
3. SQLインジェクション対策の徹底（DAO層で実施済み）
4. XSS対策の実装
5. CSRF対策の実装

### パフォーマンス
1. コネクションプールの導入
2. ページネーション機能の実装
3. インデックス最適化
4. キャッシュ機能の導入

### 保守性
1. ログ出力機能の実装（SLF4J/Log4j）
2. エラーハンドリングの統一
3. トランザクション管理の明示化
4. リソース管理の改善（try-with-resources）
5. ユニットテストの追加

### コード品質
1. メソッド名のスペルミス修正（Empolyee → Employee）
2. 適切なクラス名への変更（Test → Item）
3. マジックナンバーの定数化
4. Javadocの追加
5. Bean Validationの導入検討

## ドキュメント作成日
2025-11-02

## バージョン
1.0

## 備考
- 本仕様書は現行のソースコードに基づいて作成されています
- 実装の詳細については各個別仕様書を参照してください
- 改善提案は各仕様書に記載されています
