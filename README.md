# COBOL Call Graph Visualizer

COBOLソース群からCALL依存関係を抽出し、インタラクティブなネットワーク図としてオフラインで可視化するツールです。

## 特徴

- **正規表現による軽量解析**: 複雑なAST生成を行わず、高速かつ柔軟にPROGRAM-IDとCALL文を抽出
- **完全オフライン動作**: 生成されるHTMLは外部通信（CDN等）を一切行わず、閉域網環境でも利用可能
- **料率TBLモジュールの自動判定**: 6文字IDかつ末尾2文字がアルファベットのプログラムを自動判定し、視覚的に強調表示
- **プログラム説明の自動抽出**: PROGRAM-ID直後のコメントからプログラム説明を抽出し、ツールチップに表示
- **インタラクティブ操作**: マウスで拡大・縮小・移動が可能なネットワーク図
- **呼び出し順序の可視化**: プログラム内でのCALL順序（1番目、2番目…）をエッジラベルとして表示

## 対象ユーザー

- COBOLシステムの保守・解析を担当する開発者・SE
- システム全体像の把握が必要なアーキテクト・管理者
- インターネット非接続の閉域網環境で作業するユーザー

## 必要環境

- Python 3.x
- pip（Pythonパッケージ管理ツール）
- Webブラウザ（Chrome、Firefox、Edge等）

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd prj_kiro_visual_psan
```

### 2. Python仮想環境の作成

```bash
python -m venv .venv
```

### 3. 仮想環境のアクティベート

**Windows (PowerShell):**

```powershell
# 初回のみ実行ポリシーを設定
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 仮想環境をアクティベート
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 4. 依存ライブラリのインストール

```bash
pip install networkx pyvis
```

## 使い方

### 1. COBOLソースファイルの配置

解析対象の `.cbl` ファイルを `cobol_src/` フォルダに配置します。

```
cobol_src/
├── QB7000.cbl
├── QB712345.cbl
└── QB71RC.cbl
```

### 2. 解析スクリプトの実行

```bash
python analyze.py
```

### 3. 結果の確認

`offline_call_graph.html` が生成されるので、Webブラウザで開いて確認します。

```bash
# Windowsの場合
start offline_call_graph.html

# macOSの場合
open offline_call_graph.html

# Linuxの場合
xdg-open offline_call_graph.html
```

## プロジェクト構成

```
.
├── README.md                   # このファイル
├── .gitignore                  # Git管理除外設定
├── analyze.py                  # COBOLソース解析・可視化スクリプト
├── cobol_src/                  # 解析対象のCOBOLソースファイル（.cbl）
│   ├── QB7000.cbl             # サンプル: メイン処理
│   ├── QB712345.cbl           # サンプル: サブモジュール
│   └── QB71RC.cbl             # サンプル: 料率TBL保持モジュール
├── offline_call_graph.html    # 出力: 可視化HTML（Git管理対象外）
└── .venv/                      # Python仮想環境（Git管理対象外）
```

## ファイルの役割

### `analyze.py`

COBOLソースファイルを解析し、ネットワーク図を生成するメインスクリプトです。

**主な機能:**
- `.cbl` ファイルの読み込み（UTF-8 / Shift-JIS自動判定）
- PROGRAM-IDとCALL文の正規表現による抽出
- COBOLコメント行（7カラム目が `*` または `/`）のスキップ
- PROGRAM-ID直後のコメントからプログラム説明を自動抽出（日付を含む行は除外）
- 料率TBLモジュールの自動判定（6文字ID + 末尾2文字がアルファベット）
- NetworkXによる有向グラフの生成
- PyvisによるインタラクティブなHTML出力

### `cobol_src/`

解析対象のCOBOLソースファイル（`.cbl`）を格納するフォルダです。

**サンプルファイル:**
- `QB7000.cbl`: 火災＆超保険のメイン保険料計算処理
- `QB712345.cbl`: 自火超更新・帳票バッチ共通のサブモジュール
- `QB71RC.cbl`: 職域＆e-Auto料率TBL保持プログラム（末尾2文字がアルファベット）

### `offline_call_graph.html`

解析結果として生成されるインタラクティブなネットワーク図です。

**特徴:**
- 完全オフライン動作（外部CDN不使用）
- マウスホイールで拡大・縮小
- ドラッグで図全体を移動
- ノード・エッジにマウスオーバーでツールチップ表示

## 可視化ルール

### ノードの表示

| プログラム種別 | 判定条件 | 色 | 形状 | サイズ | 枠線 | ツールチップ |
|--------------|---------|-----|------|-------|------|------------|
| 料率TBLモジュール | 6文字ID + 末尾2文字がアルファベット | オレンジ (#FF9800) | 四角形 (box) | 実ステップ数に応じて可変 | 太枠 (4px) | 料率TBL (VCOPY) + プログラム説明 + 実ステップ数 |
| 通常プログラム | 上記以外 | 青 (#2196F3) | 四角形 (box) | 実ステップ数に応じて可変 | 標準 | プログラム説明 + 実ステップ数 |

### ノードサイズの計算

ノードのサイズは実ステップ数（コメント行・空行を除いた行数）に応じて対数スケールで変化します。

**サイズの目安:**
- 10ステップ: サイズ 20
- 100ステップ: サイズ 40
- 1000ステップ: サイズ 60
- 2000ステップ: サイズ 66
- 最大: サイズ 80

**実ステップ数のカウント方法:**
- PROCEDURE DIVISION以降の行のみをカウント
- コメント行（7カラム目が `*` または `/`）を除外
- 空行を除外
- 上記以外の行をカウント

### エッジの表示

- **ラベル**: `[1]`, `[2]`, `[3]` ... （ファイル内での呼び出し順序）
- **ツールチップ**: `呼出順: N番目`

## トラブルシューティング

### `ModuleNotFoundError: No module named 'networkx'`

仮想環境がアクティブになっていないか、ライブラリがインストールされていません。

```bash
# 仮想環境をアクティベート
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # macOS/Linux

# ライブラリをインストール
pip install networkx pyvis
```

### `警告: ./cobol_src に .cbl ファイルが見つかりません。`

`cobol_src/` フォルダが存在しないか、`.cbl` ファイルが配置されていません。

```bash
# フォルダを作成
mkdir cobol_src

# .cbl ファイルを配置
# （解析対象のCOBOLソースをコピー）
```

### PowerShellで `Activate.ps1` が実行できない

実行ポリシーが制限されています。

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグ報告や機能追加の提案は、GitHubのIssueまでお願いします。
