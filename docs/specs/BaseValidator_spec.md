# BaseValidator 仕様書

## ファイル概要
- **ファイル名**: BaseValidator.java
- **パッケージ**: validator
- **場所**: src/validator/BaseValidator.java
- **作成日**: 不明

## 目的と役割
BaseValidatorは、フォーム入力データのバリデーション機能を提供する基底クラスです。共通的なバリデーションロジック（桁数チェック、数値チェック）とエラーメッセージ管理機能を実装し、他のフォームクラスに継承して使用されます。

## クラス構成

### クラス定義
```java
@Getter
@Setter
public class BaseValidator
```

### 継承関係
- **親クラス**: なし（java.lang.Object）
- **実装インターフェース**: なし
- **サブクラス**: `form.EmployeeForm`

### Lombokアノテーション
- `@Getter`: 全フィールドのgetterメソッドを自動生成
- `@Setter`: 全フィールドのsetterメソッドを自動生成

## フィールド

### バリデーション状態管理
| フィールド名 | 型 | 説明 | 初期値 |
|------------|-----|------|--------|
| hasError | boolean | エラー有無フラグ | false（デフォルト） |

### メッセージ管理
| フィールド名 | 型 | 説明 | 初期値 |
|------------|-----|------|--------|
| errorMessage | ArrayList\<String\> | エラーメッセージのリスト | 空のリスト |
| infoMessage | ArrayList\<String\> | 情報メッセージのリスト | 空のリスト |

## 主要メソッド

### コンストラクタ
```java
public BaseValidator()
```
- **引数**: なし
- **処理内容**:
  1. errorMessageを空のArrayListで初期化
  2. infoMessageを空のArrayListで初期化

### checkByte メソッド
```java
public boolean checkByte(String str, int maxBytes, String errorMsg)
    throws UnsupportedEncodingException
```
- **引数**:
  - `str`: String - チェック対象の文字列
  - `maxBytes`: int - 最大バイト数
  - `errorMsg`: String - エラー時のメッセージ
- **戻り値**: boolean - チェック成功時true、失敗時false
- **例外**: UnsupportedEncodingException
- **処理内容**:
  1. Nullチェック
     - strがnullまたは長さ0の場合、エラー
  2. バイト数チェック
     - Shift-JISエンコーディングでバイト数を取得
     - maxBytes以下の場合、trueを返す
     - maxBytesを超える場合、falseを返す
  3. エラー時の処理
     - errorMessageにエラーメッセージを追加
     - hasErrorをtrueに設定

### isNumber メソッド
```java
public boolean isNumber(String str, String errorMsg)
```
- **引数**:
  - `str`: String - チェック対象の文字列
  - `errorMsg`: String - エラー時のメッセージ
- **戻り値**: boolean - 数値の場合true、数値でない場合false
- **処理内容**:
  1. Integer.parseInt()で数値変換を試行
  2. 変換成功時: trueを返す
  3. 変換失敗時（NumberFormatException）:
     - errorMessageにエラーメッセージを追加
     - hasErrorをtrueに設定
     - falseを返す

### Getterメソッド（Lombok自動生成）
```java
public boolean isHasError() { return hasError; }
public ArrayList<String> getErrorMessage() { return errorMessage; }
public ArrayList<String> getInfoMessage() { return infoMessage; }
```

### Setterメソッド（Lombok自動生成）
```java
public void setHasError(boolean hasError) { this.hasError = hasError; }
public void setErrorMessage(ArrayList<String> errorMessage) {
    this.errorMessage = errorMessage;
}
public void setInfoMessage(ArrayList<String> infoMessage) {
    this.infoMessage = infoMessage;
}
```

## 処理フロー

### バイト数チェックフロー
```
1. checkByte(str, maxBytes, errorMsg) 呼び出し
   ↓
2. Nullチェック
   - str == null または str.length() == 0 ?
   ↓
3-a. Nullの場合:
   errorMessage.add(errorMsg)
   hasError = true
   return false
   ↓
3-b. Nullでない場合:
   str.getBytes("Shift-JIS").length でバイト数取得
   ↓
4. バイト数比較
   - バイト数 <= maxBytes ?
   ↓
5-a. OK: return true
5-b. NG:
   errorMessage.add(errorMsg)
   hasError = true
   return false
```

### 数値チェックフロー
```
1. isNumber(str, errorMsg) 呼び出し
   ↓
2. try-catch で数値変換
   Integer.parseInt(str)
   ↓
3-a. 変換成功:
   return true
   ↓
3-b. 変換失敗（NumberFormatException）:
   errorMessage.add(errorMsg)
   hasError = true
   return false
```

## 依存関係

### 依存クラス
- `java.io.UnsupportedEncodingException`
- `java.util.ArrayList`
- `lombok.Getter`
- `lombok.Setter`

### 呼び出し元
- `form.EmployeeForm` - 社員フォームバリデーション

### 継承クラス
- `form.EmployeeForm` - BaseValidatorを継承

## バリデーションルール

### checkByte メソッドのルール
1. **必須チェック**
   - nullまたは空文字列はエラー

2. **バイト数チェック**
   - エンコーディング: Shift-JIS
   - 全角文字: 2バイト
   - 半角文字: 1バイト
   - 指定されたmaxBytesを超えた場合エラー

### isNumber メソッドのルール
1. **数値形式チェック**
   - Integer.parseInt()で変換可能な文字列のみOK
   - 許容範囲: -2,147,483,648 〜 2,147,483,647
   - 小数点、カンマ、スペースは不可

## 使用技術・ライブラリ

### 文字エンコーディング
- **Shift-JIS**: レガシーな日本語エンコーディング
- 全角1文字 = 2バイト
- 半角1文字 = 1バイト

### Lombok
- ボイラープレートコードの削減
- getter/setterの自動生成

### デザインパターン
- **Template Method パターン**: 共通処理を基底クラスに実装
- **継承による機能拡張**: サブクラスで具体的なバリデーションを実装

## エラーハンドリング

### 例外処理
1. **UnsupportedEncodingException**
   - checkByte()でスロー
   - 呼び出し元でtry-catchが必要
   - 実際にはShift-JISは常にサポートされているため発生しない

2. **NumberFormatException**
   - isNumber()内でcatch
   - エラーメッセージを追加してfalseを返す

### エラーメッセージ管理
- 複数のエラーを蓄積可能
- エラーメッセージはArrayListで管理
- 画面表示時に全エラーを一括表示可能

## 改善提案

### 1. エンコーディングの現代化
```java
// Shift-JIS → UTF-8
public boolean checkByte(String str, int maxBytes, String errorMsg) {
    if (str.getBytes(StandardCharsets.UTF_8).length <= maxBytes) {
        return true;
    }
    // ...
}
```

### 2. Bean Validation (JSR-380) への移行
```java
// アノテーションベースのバリデーション
@Size(max = 4)
@NotBlank
private String employee;
```

### 3. 汎用的なバリデーションメソッドの追加
```java
// 正規表現チェック
public boolean matchesPattern(String str, String pattern, String errorMsg)

// 範囲チェック
public boolean isInRange(int value, int min, int max, String errorMsg)

// 日付チェック
public boolean isValidDate(String str, String format, String errorMsg)

// メールアドレスチェック
public boolean isValidEmail(String str, String errorMsg)
```

### 4. エラーメッセージの構造化
```java
// エラー情報を保持するクラス
public class ValidationError {
    private String fieldName;
    private String errorMessage;
    private String errorCode;
}

private List<ValidationError> errors;
```

### 5. メソッドチェーン対応
```java
public BaseValidator checkByte(String str, int maxBytes, String errorMsg) {
    // ... バリデーション処理
    return this;  // メソッドチェーン可能に
}

// 使用例
validator
    .checkByte(str1, 10, "エラー1")
    .isNumber(str2, "エラー2")
    .validate();
```

### 6. バリデーショングループ
```java
public enum ValidationGroup {
    CREATE, UPDATE, DELETE
}

public boolean validate(ValidationGroup group) {
    // グループに応じたバリデーション実行
}
```

### 7. 非同期バリデーション対応
```java
public CompletableFuture<Boolean> validateAsync() {
    // 非同期バリデーション
}
```

### 8. カスタムバリデータの登録
```java
private Map<String, Predicate<String>> customValidators = new HashMap<>();

public void registerValidator(String name, Predicate<String> validator) {
    customValidators.put(name, validator);
}
```

### 9. 国際化（i18n）対応
```java
private ResourceBundle messages;

public BaseValidator(Locale locale) {
    this.messages = ResourceBundle.getBundle("ValidationMessages", locale);
}

public boolean checkByte(String str, int maxBytes, String messageKey) {
    String errorMsg = messages.getString(messageKey);
    // ...
}
```

### 10. ユニットテスト用のビルダー
```java
public static class Builder {
    public Builder addError(String message) { ... }
    public Builder addInfo(String message) { ... }
    public BaseValidator build() { ... }
}
```

## 使用例

### 基本的な使用方法
```java
// BaseValidatorを継承したクラス
public class MyForm extends BaseValidator {
    private String employeeId;
    private String name;

    public boolean validate() {
        try {
            // バイト数チェック
            checkByte(employeeId, 4, "社員番号は4文字以内です");
            checkByte(name, 20, "名前は10文字以内です");

            // 数値チェック
            isNumber(employeeId, "社員番号は数値です");

            // エラーがあればfalse
            return !isHasError();

        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return false;
        }
    }
}

// 使用
MyForm form = new MyForm();
form.setEmployeeId("1001");
form.setName("山田太郎");

if (form.validate()) {
    // バリデーション成功
} else {
    // エラーメッセージ表示
    for (String error : form.getErrorMessage()) {
        System.out.println(error);
    }
}
```

### 情報メッセージの使用
```java
// 成功メッセージの追加
form.getInfoMessage().add("登録が完了しました");

// JSPで表示
<c:forEach items="${infoMsg}" var="msg">
    <div class="alert alert-success">${msg}</div>
</c:forEach>
```

## セキュリティ考慮事項

### 入力値検証の限界
- 文字数とフォーマットのみチェック
- 特殊文字やスクリプトの検証は別途必要
- XSS対策は出力時に実施

### エラーメッセージの内容
- システム内部情報の露出に注意
- ユーザーフレンドリーなメッセージ推奨

## パフォーマンス考慮事項

### バイト数計算のコスト
- getBytes()は文字列のコピーを作成
- 大量データの場合はキャッシュ検討

### エラーメッセージのメモリ管理
- ArrayListは動的拡張
- 大量のエラーが蓄積しないよう注意
