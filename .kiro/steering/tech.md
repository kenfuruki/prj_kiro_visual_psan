# 技術スタック

## 解析スクリプト
- 言語: Python 3.x
- ライブラリ: networkx, pyvis

## 依存ライブラリのインストール

```
pip install networkx pyvis
```

## 主要コンポーネント

- `analyze.py` : COBOLソース解析 + HTML生成スクリプト
- `cobol_src/` : 解析対象の `.cbl` ファイル格納フォルダ
- `offline_call_graph.html` : 出力される可視化HTML（完全オフライン対応）

## 実行コマンド

```
python analyze.py
```

## PowerShell 初期操作（新規セッション開始時のみ）

新しいターミナルセッションを開いた最初の1回だけ実行する。セッションが継続している間は不要。

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\Activate.ps1
```

## 文字コード

- COBOLソースの読み込み: Shift-JIS (cp932)、エラー時は `errors='replace'` でフォールバック

## オフライン対応

- pyvis の `cdn_resources='in_line'` オプションを使用し、外部通信なしで動作するHTMLを生成する
