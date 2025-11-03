# Employee 仕様書

## ファイル概要
- **ファイル名**: Employee.java
- **パッケージ**: dto
- **場所**: src/dto/Employee.java
- **作成日**: 不明

## 目的と役割
EmployeeクラスはDTO（Data Transfer Object）として、社員情報をアプリケーション層間で転送するためのデータ保持クラスです。データベースの「pers」テーブルの1レコードに対応し、社員の詳細情報を格納します。

## クラス構成

### クラス定義
```java
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Employee
```

### 継承関係
- **親クラス**: なし（java.lang.Object）
- **実装インターフェース**: なし

### Lombokアノテーション
- `@Getter`: 全フィールドのgetterメソッドを自動生成
- `@Setter`: 全フィールドのsetterメソッドを自動生成
- `@NoArgsConstructor`: 引数なしのコンストラクタを自動生成
- `@AllArgsConstructor`: 全フィールドを引数に持つコンストラクタを自動生成

## フィールド

### 社員基本情報
| フィールド名 | 型 | 説明 | DBカラム |
|------------|-----|------|---------|
| employee | String | 社員番号 | pers_employee |
| oano | String | OA番号 | pers_oano |
| sei | String | 姓 | pers_sei |
| mei | String | 名 | pers_mei |
| nameKanji | String | 氏名（漢字） | pers_name |
| namekana | String | 氏名（カナ） | pers_namek |
| department | String | 所属部署 | pers_bu |
| group | String | 所属グループ | pers_gr |

### 監査情報
| フィールド名 | 型 | 説明 | DBカラム |
|------------|-----|------|---------|
| indate | String | 作成日 | pers_indate |
| intime | String | 作成時間 | pers_intime |
| update | String | 更新日 | pers_update |
| uptime | String | 更新時間 | pers_uptime |

## 主要メソッド

### コンストラクタ（Lombok生成）

#### 引数なしコンストラクタ
```java
public Employee()
```
- **引数**: なし
- **処理内容**: デフォルトコンストラクタ（全フィールドnull）

#### 全引数コンストラクタ
```java
public Employee(String employee, String oano, String sei, String mei,
                String nameKanji, String namekana, String department, String group,
                String indate, String intime, String update, String uptime)
```
- **引数**: 全12フィールド
- **処理内容**: 全フィールドを初期化

### getSQLResult メソッド
```java
public void getSQLResult(ResultSet rs) throws SQLException
```
- **引数**:
  - `rs`: ResultSet - SQL実行結果
- **戻り値**: void
- **例外**: SQLException
- **処理内容**:
  1. ResultSetから各カラムの値を取得
  2. 対応するフィールドに設定
  3. データベースカラム名とJavaフィールドのマッピング

### マッピング詳細
| DBカラム名 | Javaフィールド | 取得メソッド |
|-----------|--------------|------------|
| pers_employee | employee | rs.getString("pers_employee") |
| pers_oano | oano | rs.getString("pers_oano") |
| pers_sei | sei | rs.getString("pers_sei") |
| pers_mei | mei | rs.getString("pers_mei") |
| pers_name | nameKanji | rs.getString("pers_name") |
| pers_namek | namekana | rs.getString("pers_namek") |
| pers_bu | department | rs.getString("pers_bu") |
| pers_gr | group | rs.getString("pers_gr") |
| pers_indate | indate | rs.getString("pers_indate") |
| pers_intime | intime | rs.getString("pers_intime") |
| pers_update | update | rs.getString("pers_update") |
| pers_uptime | uptime | rs.getString("pers_uptime") |

### Getterメソッド（Lombok自動生成）
全フィールドに対して以下の形式のgetterが生成されます：
```java
public String getEmployee() { return employee; }
public String getOano() { return oano; }
// ... 他のフィールドも同様
```

### Setterメソッド（Lombok自動生成）
全フィールドに対して以下の形式のsetterが生成されます：
```java
public void setEmployee(String employee) { this.employee = employee; }
public void setOano(String oano) { this.oano = oano; }
// ... 他のフィールドも同様
```

## 処理フロー

### オブジェクト生成と値設定
```
1. new Employee() でインスタンス生成
   ↓
2-a. コンストラクタで値を設定
   new Employee(employee, oano, sei, mei, ...)
   ↓
2-b. またはsetterで個別に設定
   employee.setEmployee("1001")
   employee.setNameKanji("山田太郎")
   ↓
3. DTOとして各層で受け渡し
```

### ResultSetからのデータマッピング
```
1. SQLクエリ実行
   ↓
2. ResultSet取得
   ↓
3. new Employee() でインスタンス生成
   ↓
4. employee.getSQLResult(rs) 呼び出し
   ↓
5. ResultSetの各カラムから値を取得
   ↓
6. 対応するフィールドにsetterで設定
   ↓
7. マッピング済みEmployeeオブジェクト完成
```

## 依存関係

### 依存クラス
- `java.sql.ResultSet`
- `java.sql.SQLException`
- `lombok.AllArgsConstructor`
- `lombok.Getter`
- `lombok.NoArgsConstructor`
- `lombok.Setter`

### 呼び出し元
- `dao.EmployeeDAO` - DAOからのデータ取得時
- `bl.EmployeeMstBL` - ビジネスロジック層での処理
- `form.EmployeeForm` - フォームクラスでのマッピング

### 呼び出し先
- なし（純粋なデータ保持クラス）

## 使用技術・ライブラリ

### Lombok
- ボイラープレートコードの削減
- アノテーションによるコード自動生成
- コンパイル時に処理される

### JDBC
- ResultSetからのデータ取得

### デザインパターン
- **DTO（Data Transfer Object）パターン**: 層間のデータ転送
- **JavaBeans規約**: getter/setterによるプロパティアクセス

## データ型の考慮事項

### 全てStringフィールド
- **現状**: 日付・時刻もString型で保持
- **形式**:
  - 日付: yyyyMMdd（例: "20240101"）
  - 時刻: HHmmss（例: "093000"）

### 問題点
1. 型安全性の欠如
2. 日付計算が困難
3. フォーマットエラーの可能性
4. NULLとブランクの区別が曖昧

## シリアライゼーション
- Serializableインターフェースを実装していない
- セッション保存やリモート転送には不向き

## イミュータブル性
- setterが存在するため、ミュータブル（可変）
- 並行処理での注意が必要

## 改善提案

### 1. 日付・時刻型の改善
```java
private LocalDate indate;        // String → LocalDate
private LocalTime intime;        // String → LocalTime
private LocalDate update;        // String → LocalDate
private LocalTime uptime;        // String → LocalTime
```

### 2. バリデーション
```java
@NotNull
@Size(max = 4)
private String employee;

@Pattern(regexp = "\\d{7}")
private String oano;
```

### 3. イミュータブル化（必要に応じて）
```java
@Value  // Lombokの@Valueでイミュータブル化
public class Employee {
    // フィールドがfinal、setterなし
}
```

### 4. シリアライゼーション対応
```java
public class Employee implements Serializable {
    private static final long serialVersionUID = 1L;
    // ...
}
```

### 5. toString、equals、hashCode の追加
```java
@ToString
@EqualsAndHashCode
public class Employee {
    // ...
}
```

### 6. Builderパターンの導入
```java
@Builder
public class Employee {
    // 複雑なオブジェクト生成を簡潔に
}
```

### 7. フィールドの整理
```java
// seiとmeiが未使用のため、削除を検討
// またはnameKanjiを廃止してsei+meiで構成
```

### 8. ネーミングの改善
```java
private String nameKana;  // namekana → nameKana（キャメルケース）
```

### 9. ドキュメンテーション
```java
/**
 * 社員情報を保持するDTOクラス
 * データベースのpersテーブルに対応
 */
@Getter
@Setter
public class Employee {
    /** 社員番号（主キー） */
    private String employee;
    // ...
}
```

### 10. NULL安全性
```java
@NonNull  // Lombokの@NonNull
private String employee;
```

## 使用例

### インスタンス生成
```java
// 引数なしコンストラクタ
Employee emp1 = new Employee();
emp1.setEmployee("1001");
emp1.setNameKanji("山田太郎");

// 全引数コンストラクタ
Employee emp2 = new Employee("1001", "OA00001", "", "",
    "山田太郎", "ヤマダタロウ", "システム開発部", "SIG",
    "20240101", "090000", null, null);

// ResultSetからのマッピング
Employee emp3 = new Employee();
emp3.getSQLResult(resultSet);
```

### データ取得
```java
String employeeId = emp.getEmployee();
String name = emp.getNameKanji();
String dept = emp.getDepartment();
```
