# ItemValidator 仕様書

## ファイル概要
- **ファイル名**: ItemValidator.java
- **パッケージ**: validator
- **場所**: src/validator/ItemValidator.java
- **実装状況**: クラス定義のみ、機能は未実装

## 目的と役割
ItemValidatorは、物品マスタのフォーム入力データのバリデーション機能を提供するクラスとして設計されています。BaseValidatorを継承し、物品情報特有のバリデーションロジックを実装することを想定していますが、現在は未実装です。

## クラス構成

### クラス定義
```java
public class ItemValidator extends BaseValidator
```

### 継承関係
- **親クラス**: `validator.BaseValidator`
- **実装インターフェース**: なし

### 継承元の機能（BaseValidatorから）
- `checkByte()`: バイト数チェック
- `isNumber()`: 数値チェック
- `getErrorMessage()`: エラーメッセージ取得
- `getInfoMessage()`: 情報メッセージ取得
- `isHasError()`: エラー有無確認

## 主要メソッド

### validate メソッド
```java
public List<String> validate(Test test)
```
- **引数**:
  - `test`: Test - バリデーション対象のDTOオブジェクト
- **戻り値**: `List<String>` - エラーメッセージのリスト（現在はnull）
- **処理内容**:
  - 現在は実装されておらず、常にnullを返す
- **実装状況**: 未実装

## 依存関係

### 依存クラス
- `java.util.List`
- `dto.Test`
- `validator.BaseValidator`（継承）

### 呼び出し元
- 現在は使用されていない
- 想定: `servlet.ItemMstServlet`

### 呼び出し先
- なし（実装なし）

## 実装状況
- **クラス定義**: 完了
- **メソッドシグネチャ**: 定義済み
- **実装**: 未完成（nullを返すのみ）

## 設計上の問題点

### 1. DTOの命名
- `Test` という汎用的な名前は不適切
- 物品情報を表すDTOであれば `Item` または `ItemDto` が適切

### 2. 戻り値の設計
- BaseValidatorは errorMessage（ArrayList<String>）を持っている
- validate()メソッドが独自にList<String>を返すのは冗長
- 統一されたエラー管理方式が必要

### 3. 実装の欠如
- 実際のバリデーションロジックが全くない
- nullを返すため、呼び出し側でNullPointerExceptionのリスク

## 改善提案

### 1. 適切なDTO使用
```java
public class ItemValidator extends BaseValidator {

    // 物品情報のバリデーション
    public boolean validate(Item item) throws UnsupportedEncodingException {
        // 物品コードのチェック
        checkByte(item.getItemCode(), 10, "物品コードは10文字以内で入力してください");
        isNumber(item.getItemCode(), "物品コードは数値で入力してください");

        // 物品名のチェック
        checkByte(item.getItemName(), 50, "物品名は50文字以内で入力してください");

        // 単価のチェック
        if (item.getUnitPrice() < 0) {
            getErrorMessage().add("単価は0以上で入力してください");
            setHasError(true);
        }

        // エラーがなければtrue
        return !isHasError();
    }
}
```

### 2. フォームオブジェクトの使用
```java
public class ItemForm extends BaseValidator {
    private String itemCode;
    private String itemName;
    private String category;
    private String unitPrice;

    // 自身でバリデーション
    public boolean validateInputData() {
        try {
            // 必須チェック＆バイト数チェック
            checkByte(this.itemCode, 10, "物品コードは必須で10文字以内です");
            checkByte(this.itemName, 50, "物品名は必須で50文字以内です");
            checkByte(this.category, 20, "カテゴリは20文字以内です");

            // 数値チェック
            isNumber(this.itemCode, "物品コードは数値で入力してください");
            isNumber(this.unitPrice, "単価は数値で入力してください");

            // カスタムチェック
            if (Integer.parseInt(this.unitPrice) < 0) {
                getErrorMessage().add("単価は0以上で入力してください");
                setHasError(true);
            }

            return !isHasError();

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}
```

### 3. 特定フィールドのバリデーション
```java
public class ItemValidator extends BaseValidator {

    // 物品コードのバリデーション
    public boolean validateItemCode(String itemCode) {
        try {
            // 必須チェック
            if (itemCode == null || itemCode.isEmpty()) {
                getErrorMessage().add("物品コードは必須です");
                setHasError(true);
                return false;
            }

            // フォーマットチェック（例: 10桁の数字）
            if (!itemCode.matches("\\d{10}")) {
                getErrorMessage().add("物品コードは10桁の数字で入力してください");
                setHasError(true);
                return false;
            }

            return true;

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    // 物品名のバリデーション
    public boolean validateItemName(String itemName) {
        try {
            return checkByte(itemName, 50, "物品名は50文字以内で入力してください");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return false;
        }
    }

    // 単価のバリデーション
    public boolean validateUnitPrice(String unitPrice) {
        // 数値チェック
        if (!isNumber(unitPrice, "単価は数値で入力してください")) {
            return false;
        }

        // 範囲チェック
        int price = Integer.parseInt(unitPrice);
        if (price < 0 || price > 10000000) {
            getErrorMessage().add("単価は0〜10,000,000の範囲で入力してください");
            setHasError(true);
            return false;
        }

        return true;
    }
}
```

### 4. Bean Validationへの移行
```java
public class Item {

    @NotBlank(message = "物品コードは必須です")
    @Pattern(regexp = "\\d{10}", message = "物品コードは10桁の数字で入力してください")
    private String itemCode;

    @NotBlank(message = "物品名は必須です")
    @Size(max = 50, message = "物品名は50文字以内で入力してください")
    private String itemName;

    @NotNull(message = "単価は必須です")
    @Min(value = 0, message = "単価は0以上で入力してください")
    @Max(value = 10000000, message = "単価は10,000,000以下で入力してください")
    private Integer unitPrice;
}

// バリデータの使用
ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
Validator validator = factory.getValidator();
Set<ConstraintViolation<Item>> violations = validator.validate(item);

if (!violations.isEmpty()) {
    for (ConstraintViolation<Item> violation : violations) {
        System.out.println(violation.getMessage());
    }
}
```

### 5. カスタムバリデーションルール
```java
public class ItemValidator extends BaseValidator {

    // 物品コードの重複チェック（DB参照）
    public boolean validateItemCodeUnique(String itemCode, ItemDAO dao) {
        if (dao.existsByItemCode(itemCode)) {
            getErrorMessage().add("この物品コードは既に登録されています");
            setHasError(true);
            return false;
        }
        return true;
    }

    // カテゴリの妥当性チェック
    public boolean validateCategory(String category, List<String> validCategories) {
        if (!validCategories.contains(category)) {
            getErrorMessage().add("無効なカテゴリが選択されています");
            setHasError(true);
            return false;
        }
        return true;
    }
}
```

## 使用例（実装後の想定）

### パターン1: 直接バリデータを使用
```java
ItemValidator validator = new ItemValidator();
Item item = new Item();
item.setItemCode("1234567890");
item.setItemName("ノートPC");
item.setUnitPrice(150000);

if (validator.validate(item)) {
    // バリデーション成功
    dao.insert(item);
} else {
    // エラー表示
    List<String> errors = validator.getErrorMessage();
    for (String error : errors) {
        System.out.println(error);
    }
}
```

### パターン2: フォームクラスに組み込み
```java
ItemForm form = new ItemForm();
form.setItemCode(request.getParameter("itemCode"));
form.setItemName(request.getParameter("itemName"));

if (form.validateInputData()) {
    // 登録処理
    bl.registerItem(form);
} else {
    // エラーメッセージをJSPへ
    request.setAttribute("errors", form.getErrorMessage());
    request.getRequestDispatcher("itemMst.jsp").forward(request, response);
}
```

## まとめ
ItemValidatorは物品マスタのバリデーション機能を提供する予定のクラスですが、現在は完全に未実装です。実装にあたっては、DTOの適切な命名、BaseValidatorとの統合、具体的なバリデーションロジックの追加が必要です。
