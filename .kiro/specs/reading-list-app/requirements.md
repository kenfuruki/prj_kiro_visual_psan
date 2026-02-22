# 要件定義書

## はじめに

本ドキュメントは、COBOLソース群からCALL依存関係を抽出し、インタラクティブなネットワーク図としてオフラインで可視化するツール「COBOL Call Graph Visualizer」の要件を定義します。

## 用語集

- **COBOLソース**: 解析対象の `.cbl` 拡張子を持つCOBOLプログラムファイル
- **PROGRAM-ID**: COBOLプログラムの識別子
- **CALL文**: COBOLプログラム内で他のプログラムを呼び出す命令
- **呼び出し順序**: 1つのプログラム内でCALL文が出現する順番（1番目、2番目…）
- **料率TBLモジュール**: 6文字IDかつ末尾2文字がアルファベット（A-Z）のプログラム。VCOPYで料率マスター値を保持する
- **ノード**: ネットワーク図上のプログラムを表す図形要素
- **エッジ**: ネットワーク図上のプログラム間の呼び出し関係を表す線
- **オフライン動作**: 外部通信（CDN等）を一切行わず、HTMLファイル単体で動作すること

---

## 要件

### 要件1: COBOLソースの解析

**ユーザーストーリー:** COBOL保守担当者として、複数のCOBOLソースファイルからPROGRAM-IDとCALL文を自動抽出したい。そうすることで、手作業でのドキュメント作成を不要にできる。

#### 受け入れ基準

1. WHEN ユーザーが `cobol_src/` フォルダに `.cbl` ファイルを配置して解析を実行したとき、THE System SHALL すべての `.cbl` ファイルを読み込む
2. THE System SHALL 各ファイルをShift-JIS (cp932) エンコーディングで読み込み、エラー時は `errors='replace'` でフォールバックする
3. WHEN COBOLソース内にPROGRAM-ID文が存在するとき、THE System SHALL 正規表現 `PROGRAM-ID\.\s+([A-Za-z0-9\-]+)` でプログラムIDを抽出する
4. WHEN COBOLソース内にCALL文が存在するとき、THE System SHALL 正規表現 `CALL\s+['\"]?([^\s\'\"]+)['\"]?` で呼び出し先プログラムIDを抽出する
5. THE System SHALL COBOLのコメント行（7カラム目が `*` または `/`）をスキップする
6. THE System SHALL 抽出したすべてのプログラムIDを大文字（`.upper()`）に正規化する
7. THE System SHALL 各CALL文の出現順序（1番目、2番目…）を記録する

---

### 要件2: 料率TBLモジュールの自動判定

**ユーザーストーリー:** システムアーキテクトとして、料率テーブル保持モジュールを自動判定して視覚的に強調したい。そうすることで、データ参照専用モジュールを一目で識別できる。

#### 受け入れ基準

1. WHEN プログラムIDが6文字 かつ 末尾2文字がアルファベット（A-Z）のとき、THE System SHALL そのプログラムを料率TBLモジュールとして判定する
2. THE System SHALL 正規表現 `^[A-Z0-9]{4}[A-Z]{2}$` で料率TBLモジュールを判定する
3. WHEN プログラムが料率TBLモジュールと判定されたとき、THE System SHALL ノードの色をオレンジ（`#FF9800`）に設定する
4. WHEN プログラムが料率TBLモジュールと判定されたとき、THE System SHALL ノードの形状をデータベース型（`database`）に設定する
5. WHEN プログラムが料率TBLモジュールと判定されたとき、THE System SHALL ノードのサイズを30に設定する
6. WHEN プログラムが通常プログラムのとき、THE System SHALL ノードの色を青（`#2196F3`）、形状を四角形（`box`）、サイズを20に設定する

---

### 要件3: ネットワーク図の生成

**ユーザーストーリー:** COBOL保守担当者として、プログラム間の呼び出し関係をネットワーク図として可視化したい。そうすることで、システム全体の構造を直感的に把握できる。

#### 受け入れ基準

1. WHEN 解析が完了したとき、THE System SHALL networkxの有向グラフ（DiGraph）を生成する
2. THE System SHALL 各プログラムをノードとして追加する
3. THE System SHALL 各CALL関係をエッジとして追加する
4. WHEN エッジを追加するとき、THE System SHALL 呼び出し順序を `[1]`, `[2]` … の形式でラベルとして設定する
5. THE System SHALL エッジのツールチップに `呼出順: N番目` の形式で詳細情報を設定する
6. THE System SHALL pyvisのNetworkクラスを使用してHTMLを生成する
7. THE System SHALL ネットワーク図の背景色を `#222222`（ダークグレー）、フォント色を白に設定する
8. THE System SHALL ノードが重ならないよう物理演算パラメータ（`node_distance=250`, `central_gravity=0.1`, `spring_length=200`, `spring_strength=0.05`）を設定する

---

### 要件4: 完全オフライン対応

**ユーザーストーリー:** 閉域網環境の担当者として、インターネット接続なしでネットワーク図を閲覧したい。そうすることで、セキュリティ制約のある環境でも利用できる。

#### 受け入れ基準

1. WHEN HTMLファイルを生成するとき、THE System SHALL pyvisの `cdn_resources='in_line'` オプションを使用する
2. THE System SHALL 生成されたHTMLファイルに外部CDNへの参照を含めない
3. THE System SHALL 必要なJavaScriptライブラリをHTMLファイル内に埋め込む
4. WHEN ユーザーがインターネット非接続の端末でHTMLファイルを開いたとき、THE System SHALL 正常にネットワーク図を表示する
5. THE System SHALL 生成されたHTMLファイルを `offline_call_graph.html` として保存する

---

### 要件5: インタラクティブ操作

**ユーザーストーリー:** COBOL保守担当者として、ネットワーク図をマウスで拡大・縮小・移動したい。そうすることで、大規模なシステムでも詳細を確認できる。

#### 受け入れ基準

1. WHEN ユーザーがネットワーク図上でマウスホイールを操作したとき、THE System SHALL 図を拡大・縮小する
2. WHEN ユーザーがネットワーク図上でドラッグ操作をしたとき、THE System SHALL 図全体を移動する
3. WHEN ユーザーがノードをクリックしたとき、THE System SHALL そのノードを選択状態にする
4. WHEN ユーザーがノードにマウスカーソルを重ねたとき、THE System SHALL ツールチップ（プログラム種別）を表示する
5. WHEN ユーザーがエッジにマウスカーソルを重ねたとき、THE System SHALL ツールチップ（呼び出し順序）を表示する

---

### 要件6: エラーハンドリング

**ユーザーストーリー:** ツール利用者として、解析エラーが発生した場合に適切なメッセージを受け取りたい。そうすることで、問題を特定して修正できる。

#### 受け入れ基準

1. WHEN `cobol_src/` フォルダが存在しないとき、THE System SHALL 警告メッセージを表示する
2. WHEN `cobol_src/` フォルダ内に `.cbl` ファイルが存在しないとき、THE System SHALL 警告メッセージを表示する
3. WHEN 特定のファイルの読み込みに失敗したとき、THE System SHALL エラーメッセージとファイル名を表示し、他のファイルの処理を継続する
4. WHEN 解析結果にノードが1つも存在しないとき、THE System SHALL 「可視化するデータがありません」というメッセージを表示する
5. THE System SHALL すべての処理完了時に「✅ 完了！ 完全オフライン対応のHTMLを offline_call_graph.html に出力しました。」というメッセージを表示する
