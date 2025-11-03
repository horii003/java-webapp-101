# EmployeeForm 仕様書

## ファイル概要
- **ファイル名**: EmployeeForm.java
- **パッケージ**: form
- **場所**: src/form/EmployeeForm.java
- **作成日**: 不明

## 目的と役割
EmployeeFormは、社員情報の入力フォームデータを保持し、バリデーション機能を提供するクラスです。BaseValidatorを継承してバリデーション機能を実装し、Webフォームからの入力データの検証とエラーメッセージ管理を行います。

## クラス構成

### クラス定義
```java
@Getter
@Setter
public class EmployeeForm extends BaseValidator
```

### 継承関係
- **親クラス**: `validator.BaseValidator`
- **実装インターフェース**: なし

### Lombokアノテーション
- `@Getter`: 全フィールドのgetterメソッドを自動生成
- `@Setter`: 全フィールドのsetterメソッドを自動生成

## フィールド

### コンボボックス用リスト
| フィールド名 | 型 | 説明 | 初期値 |
|------------|-----|------|--------|
| departmentList | ArrayList\<String\> | 部署名のリスト | "システム開発部", "ラボシステム部", "システム管理部" |
| groupList | ArrayList\<String\> | グループ名のリスト | "SIG", "運用G" |

### 社員情報フィールド
| フィールド名 | 型 | 説明 |
|------------|-----|------|
| employee | String | 社員番号 |
| oano | String | OA番号 |
| nameKanji | String | 氏名（漢字） |
| namekana | String | 氏名（カナ） |
| department | String | 所属部署 |
| group | String | 所属グループ |

### 継承フィールド（BaseValidatorから）
- `errorMessage`: ArrayList\<String\> - エラーメッセージのリスト
- `infoMessage`: ArrayList\<String\> - 情報メッセージのリスト
- `hasError`: boolean - エラー有無フラグ

## 主要メソッド

### コンストラクタ
```java
public EmployeeForm()
```
- **引数**: なし
- **処理内容**:
  1. 親クラス（BaseValidator）のコンストラクタ呼び出し
  2. departmentListの初期化
     - "システム開発部"
     - "ラボシステム部"
     - "システム管理部"
  3. groupListの初期化
     - "SIG"
     - "運用G"

### validateInputData メソッド
```java
public boolean validateInputData()
```
- **引数**: なし
- **戻り値**: boolean - バリデーション成功時true、失敗時false
- **処理内容**:
  1. バイト数チェック
  2. エラーがあればfalseを返す
  3. 数値チェック
  4. エラーがあればfalseを返す
  5. 全てのチェックをパスしたらtrueを返す
- **例外処理**: 例外発生時はfalseを返す

### バイト数チェックの詳細
| フィールド | 最大バイト数 | エラーメッセージ |
|-----------|------------|----------------|
| employee | 4 | "社員番号は半角4文字以内で入力してください。" |
| oano | 7 | "OA番号は半角7文字以内で入力してください。" |
| nameKanji | 22 | "氏名（漢字）は全角11文字以内で入力してください。" |
| namekana | 21 | "氏名（カナ）は半角21文字以内で入力してください。" |
| department | 20 | "部署は全角10文字以内で入力してください。" |
| group | 30 | "グループ名は全角15文字以内で入力してください。" |

※エンコーディング: Shift-JIS（全角1文字=2バイト、半角1文字=1バイト）

### 数値チェックの詳細
| フィールド | エラーメッセージ |
|-----------|----------------|
| employee | "社員番号は数字で入力してください。" |
| oano | "OA番号は数値で入力してください。" |

### mapSQLResult メソッド
```java
public void mapSQLResult(Employee employee)
```
- **引数**:
  - `employee`: Employee - Employeeオブジェクト
- **戻り値**: void
- **処理内容**:
  1. EmployeeオブジェクトからフィールドをコピーしてEmployeeFormに設定
  2. フィールドマッピング:
     - employee.getEmployee() → this.employee
     - employee.getOano() → this.oano
     - employee.getNameKanji() → this.nameKanji
     - employee.getNamekana() → this.namekana
     - employee.getDepartment() → this.department
     - employee.getGroup() → this.group

## 処理フロー

### バリデーション処理フロー
```
1. validateInputData() 呼び出し
   ↓
2. バイト数チェック（6項目）
   - checkByte()を各フィールドに対して実行
   - 空文字チェック
   - 最大バイト数チェック
   ↓
3. エラーチェック
   - isHasError() が true の場合 → return false
   ↓
4. 数値チェック（2項目）
   - isNumber()を社員番号とOA番号に対して実行
   - 数値変換可能かチェック
   ↓
5. エラーチェック
   - isHasError() が true の場合 → return false
   ↓
6. 全チェック合格
   → return true
```

### SQL結果のマッピングフロー
```
1. mapSQLResult(employee) 呼び出し
   ↓
2. Employeeオブジェクトから各フィールドを取得
   ↓
3. 対応するEmployeeFormのフィールドに設定
   - employee → this.employee
   - oano → this.oano
   - nameKanji → this.nameKanji
   - namekana → this.namekana
   - department → this.department
   - group → this.group
   ↓
4. マッピング完了
```

## 依存関係

### 依存クラス
- `java.util.ArrayList`
- `dto.Employee`
- `lombok.Getter`
- `lombok.Setter`
- `validator.BaseValidator`

### 継承元メソッド（BaseValidatorから）
- `checkByte(String str, int maxBytes, String errorMsg)`: バイト数チェック
- `isNumber(String str, String errorMsg)`: 数値チェック
- `getErrorMessage()`: エラーメッセージリスト取得
- `getInfoMessage()`: 情報メッセージリスト取得
- `isHasError()`: エラー有無確認
- `setHasError(boolean hasError)`: エラーフラグ設定

### 呼び出し元
- `servlet.EmployeeMstServlet` - フォームデータの保持とバリデーション

### 呼び出し先
- `validator.BaseValidator` - バリデーション機能
- `dto.Employee` - データマッピング

## バリデーションルール

### 必須チェック
- 全フィールドが必須（空文字・nullはエラー）
- checkByte()内で実施

### 文字数制限
| 項目 | 最大文字数 | エンコーディング |
|------|----------|----------------|
| 社員番号 | 半角4文字 | Shift-JIS |
| OA番号 | 半角7文字 | Shift-JIS |
| 氏名（漢字） | 全角11文字 | Shift-JIS |
| 氏名（カナ） | 半角21文字 | Shift-JIS |
| 部署 | 全角10文字 | Shift-JIS |
| グループ | 全角15文字 | Shift-JIS |

### 形式チェック
- 社員番号: 数値のみ
- OA番号: 数値のみ

## 使用技術・ライブラリ

### Lombok
- ボイラープレートコードの削減
- getter/setterの自動生成

### デザインパターン
- **Form Object パターン**: Webフォームデータの保持
- **継承によるバリデーション**: BaseValidatorから機能を継承

## エラーハンドリング

### バリデーションエラー
- エラーメッセージは errorMessage リストに追加
- 複数のエラーを蓄積可能
- hasError フラグで一括チェック

### 例外処理
- validateInputData()内のtry-catch
- 例外発生時はfalseを返す
- スタックトレースは出力しない（BaseValidatorに委譲）

## 改善提案

### 1. Bean Validation (JSR-380) の導入
```java
@NotBlank(message = "社員番号は必須です")
@Size(max = 4, message = "社員番号は4文字以内で入力してください")
@Pattern(regexp = "\\d{4}", message = "社員番号は数字で入力してください")
private String employee;
```

### 2. エンコーディングの統一
- Shift-JIS → UTF-8
- 現代的な文字列処理

### 3. マジックナンバーの定数化
```java
private static final int MAX_EMPLOYEE_LENGTH = 4;
private static final int MAX_OANO_LENGTH = 7;
// ...
```

### 4. バリデーショングループの導入
- 登録時と更新時で異なるルール適用

### 5. カスタムバリデータの実装
```java
@EmployeeIdFormat
private String employee;
```

### 6. 正規表現によるフォーマットチェック
```java
// カナのチェック
if (!namekana.matches("[ァ-ヶー]+")) {
    // エラー
}
```

### 7. 部署・グループの動的取得
- ハードコーディングをやめ、データベースから取得
- マスタテーブルの作成

### 8. ビルダーパターンの導入
```java
@Builder
public class EmployeeForm extends BaseValidator {
    // ...
}
```

### 9. イミュータブルなリスト
```java
private final List<String> departmentList =
    Collections.unmodifiableList(Arrays.asList(
        "システム開発部", "ラボシステム部", "システム管理部"
    ));
```

### 10. エラーメッセージの外部化
- プロパティファイルで管理
- 国際化（i18n）対応

## 使用例

### インスタンス生成とバリデーション
```java
// フォームオブジェクトの生成
EmployeeForm form = new EmployeeForm();

// フォームデータの設定
form.setEmployee("1001");
form.setOano("OA00001");
form.setNameKanji("山田太郎");
form.setNamekana("ヤマダタロウ");
form.setDepartment("システム開発部");
form.setGroup("SIG");

// バリデーション実行
if (form.validateInputData()) {
    // バリデーション成功
    // 登録処理へ
} else {
    // バリデーション失敗
    List<String> errors = form.getErrorMessage();
    // エラーメッセージを表示
}
```

### SQL結果のマッピング
```java
// DAOから取得したEmployeeオブジェクト
Employee employee = dao.searchEmployeeById("1001");

// フォームオブジェクトへマッピング
EmployeeForm form = new EmployeeForm();
form.mapSQLResult(employee);

// フォームデータの利用
String name = form.getNameKanji();
```

### コンボボックスデータの取得
```java
EmployeeForm form = new EmployeeForm();
List<String> departments = form.getDepartmentList();
List<String> groups = form.getGroupList();

// JSPへ渡す
request.setAttribute("departmentList", departments);
request.setAttribute("groupList", groups);
```

## セキュリティ考慮事項

### 入力値のサニタイズ
- 現状は文字数とフォーマットのみチェック
- XSS対策として特殊文字のエスケープが必要

### SQLインジェクション対策
- DAO層でPreparedStatementを使用しているため安全
- フォーム層での対策は不要

## パフォーマンス考慮事項
- バリデーションは軽量処理のため問題なし
- コンボボックスリストはインスタンス毎に生成（最適化の余地あり）
