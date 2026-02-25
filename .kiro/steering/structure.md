# プロジェクト構造

## フォルダ構成

```
作業フォルダ/
├── .venv/                      # Python仮想環境（Git管理対象外）
├── .kiro/                      # Kiroステアリングファイル
│   └── steering/
│       ├── tech.md             # 技術スタック
│       ├── product.md          # プロダクト概要
│       ├── structure.md        # プロジェクト構造
│       ├── str_jpn.md          # 日本語出力ルール
│       └── str_powershell.md   # PowerShell初期操作
├── cobol_src/                  # 解析対象のCOBOLソースファイル（.cbl）
│   ├── QB7000.cbl
│   ├── QB712345.cbl
│   └── QB71RC.cbl
├── analyze.py                  # COBOLソース解析・可視化スクリプト
├── README.md                   # プロジェクトドキュメント
├── .gitignore                  # Git管理除外設定
├── offline_call_graph.html     # 出力：可視化HTML（Git管理対象外）
├── call_graph_structure.txt    # 出力：AI向け依存関係リスト（Git管理対象外）
└── step_count_report.txt       # 出力：ステップ数集計レポート（Git管理対象外）
```

## 規約

- COBOLファイルの拡張子は `.cbl`
- PROGRAM-IDとCALL文は正規表現で抽出（AST不使用）
- CALL文の抽出には単語境界（`\b`）を使用し、段落名やラベル名に含まれる「CALL」文字列を除外
- ファイル名フィルタ（先頭N桁指定、複数指定可能）により、特定のプログラム群のみを処理対象にできる
- COBOLのコメント行（7カラム目が `*` または `/`）はスキップ
- ノード名・プログラムIDはすべて大文字（`.upper()`）に正規化

## 料率TBLモジュールの判定ルール

- 条件: プログラム内に `COPY VB7` で始まるVCOPY句が存在する
- 正規表現: `\bCOPY\s+VB7`
- 表示: オレンジ色（`#FF9800`）、四角形（`box`）、太枠（borderWidth=4）、実ステップ数に応じて可変サイズ

## 通常プログラムの表示

- 表示: 青色（`#2196F3`）、四角形（`box`）、実ステップ数に応じて可変サイズ

## ノードサイズの計算

- 実ステップ数（PROCEDURE DIVISION以降のコメント行・空行を除く行数）に応じて対数スケールで変化
- 10ステップ: サイズ 20
- 100ステップ: サイズ 40
- 1000ステップ: サイズ 60
- 2000ステップ: サイズ 66
- 最大: サイズ 80

## エッジ（呼び出し関係）

- ラベル: `[1]`, `[2]` … （ファイル内での呼び出し順序）
- ツールチップ: `呼出順: N番目` または `呼出順: N番目 (動的CALL)`

## 動的CALL（動的リンク）の判定と表示

- 静的CALL: `CALL 'PROGRAM'` のように引用符で囲まれたプログラム名
  - 表示: グレーの実線
- 動的CALL: `CALL WS-VARIABLE` のように変数を使用
  - 表示: 赤色の破線（太め）
  - WORKING-STORAGE SECTIONのVALUE句やMOVE文で変数に代入された実際のプログラム名を表示
