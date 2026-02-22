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
- `call_graph_structure.txt` : AI向けシンプルな依存関係リスト
- `step_count_report.txt` : ステップ数集計レポート（TOP_PROGRAMS指定時）

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

- COBOLソースの読み込み: UTF-8優先、失敗時はShift-JIS (cp932) でフォールバック（`errors='replace'`）
- HTML出力: UTF-8エンコーディング、`<meta charset="utf-8">` タグ追加、`errors='surrogatepass'` で出力

## オフライン対応

- pyvis の `cdn_resources='in_line'` オプションを使用し、外部通信なしで動作するHTMLを生成する
