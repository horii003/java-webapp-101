import os
from pathlib import Path
import sys

def should_process_file(file_path: Path) -> bool:
    if file_path.name.startswith('.') or '.git' in file_path.parts or file_path.suffix == '.md':
        return False
    binary_extensions = {'.class', '.jar', '.war', '.png', '.jpg', '.jpeg', '.gif', '.pyc', '.pyo'}
    return file_path.suffix not in binary_extensions

def get_file_type_description(file_suffix: str) -> str:
    descriptions = {
        '.java': 'Javaソースファイル',
        '.jsp': 'JavaServer Pagesファイル',
        '.xml': 'XML設定ファイル',
        '.properties': 'プロパティ設定ファイル',
        '.txt': 'テキストファイル',
        '.py': 'Pythonソースファイル'
    }
    return descriptions.get(file_suffix, 'その他のファイル')

def generate_markdown_description(file_path: Path) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        file_type = get_file_type_description(file_path.suffix)
        relative_path = file_path.relative_to(Path(__file__).parent)
        content_analysis = analyze_file_content(content, file_type)
        
        description = f"""# {file_path.name}

## ファイル情報
- ファイルタイプ: {file_type}
- 場所: {relative_path}

## 概要
{content_analysis}

## ファイルの内容
このファイルには以下のコードが含まれています：

```{file_path.suffix[1:] if file_path.suffix else ''}
{content}
```

## 技術的な説明
このファイルは{file_type}で、java-webapp-101プロジェクトの一部として以下の役割を果たしています：

- Webアプリケーションの{file_type}として機能します
- ファイル内のコードは、アプリケーションの重要なコンポーネントとして動作します
- このファイルは他のコンポーネントと連携して、Webアプリケーションの機能を実現します
"""
        return description
    except UnicodeDecodeError:
        print(f"Warning: {file_path} appears to be a binary file, skipping...")
        return None
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def analyze_file_content(content: str, file_type: str) -> str:
    if file_type == 'Javaソースファイル':
        if 'class' in content:
            return 'Javaのクラスファイルです。クラスの定義と実装が含まれています。'
        elif 'interface' in content:
            return 'Javaのインターフェースファイルです。インターフェースの定義が含まれています。'
    elif file_type == 'JavaServer Pagesファイル':
        return 'JSPファイルです。HTMLとJavaコードを組み合わせたWebページのテンプレートが含まれています。'
    elif file_type == 'XML設定ファイル':
        if 'web-app' in content:
            return 'Webアプリケーションの設定ファイルです。サーブレットやフィルターの設定が含まれています。'
        return 'XML形式の設定ファイルです。アプリケーションの設定情報が含まれています。'
    return 'ファイルの内容を確認してください。'

def main():
    repo_path = Path(__file__).parent
    processed_files = 0
    skipped_files = 0
    
    print("ドキュメント生成を開始します...")
    
    for file_path in repo_path.rglob('*'):
        if not file_path.is_file() or not should_process_file(file_path):
            skipped_files += 1
            continue
            
        markdown_path = file_path.with_suffix('.md')
        description = generate_markdown_description(file_path)
        
        if description:
            try:
                with open(markdown_path, 'w', encoding='utf-8') as f:
                    f.write(description)
                print(f"✓ {file_path.name}のドキュメントを生成しました")
                processed_files += 1
            except Exception as e:
                print(f"✗ {file_path.name}の処理中にエラーが発生しました: {e}")
                skipped_files += 1
    
    print(f"\n処理完了:")
    print(f"- 生成されたドキュメント: {processed_files}個")
    print(f"- スキップされたファイル: {skipped_files}個")

if __name__ == '__main__':
    main()
