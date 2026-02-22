import os
import glob
import re
import networkx as nx
from pyvis.network import Network

def analyze_cobol_folder(folder_path):
    """COBOLソースフォルダを解析してグラフを生成"""
    G = nx.DiGraph()
    cbl_files = glob.glob(os.path.join(folder_path, '*.cbl'))
    
    if not cbl_files:
        print(f"警告: {folder_path} に .cbl ファイルが見つかりません。")
        return G
    
    # PROGRAM-IDとCALLを抽出する正規表現
    prog_id_pattern = re.compile(r"PROGRAM-ID\.\s+([A-Za-z0-9\-]+)", re.IGNORECASE)
    call_pattern = re.compile(r"CALL\s+['\"]?([^\s\'\"]+)['\"]?", re.IGNORECASE)
    # 日付パターン（変更履歴除外用）
    date_pattern = re.compile(r'\d{4}[/-]\d{2}[/-]\d{2}|\d{8}')
    
    def extract_program_description(lines, start_index):
        """PROGRAM-ID直後のコメントからプログラム説明を抽出"""
        for i in range(start_index, min(start_index + 10, len(lines))):
            line = lines[i]
            # コメント行でない場合は終了
            if len(line) <= 6 or line[6] not in ['*', '/']:
                break
            
            # コメント部分を取得（7カラム目以降）
            comment = line[7:].strip()
            
            # 除外条件：空行、区切り線、日付を含む行
            if not comment:
                continue
            if re.match(r'^[-=*]+$', comment):  # 区切り線
                continue
            if date_pattern.search(comment):  # 日付を含む
                continue
            
            # 有効な説明文を発見
            # Shift-JISバイト列として再エンコード→UTF-8デコード（文字化け対策）
            try:
                # 既にUnicode文字列なのでそのまま返す
                return comment
            except:
                return comment
        
        return None
    
    # ノード追加用のヘルパー関数（料率TBL判定を行う）
    def add_smart_node(graph, node_name, description=None, step_count=0):
        # 6文字 かつ 末尾2文字がアルファベット(A-Z) か判定
        is_rate_tbl = re.match(r'^[A-Z0-9]{4}[A-Z]{2}$', node_name)
        
        # ステップ数に応じてサイズを調整（対数スケール）
        if step_count > 0:
            import math
            # 対数スケールでサイズを計算（最小20、最大80）
            # 10ステップ = 20, 100ステップ = 40, 1000ステップ = 60, 2000ステップ = 66
            base_size = 20
            if step_count >= 10:
                log_size = base_size + (math.log10(step_count) * 20)
                size = min(int(log_size), 80)
            else:
                size = base_size
        else:
            size = 20  # ステップ数不明の場合はデフォルト
        
        # ツールチップの作成
        tooltip_parts = []
        if is_rate_tbl:
            tooltip_parts.append("料率TBL (VCOPY)")
        if description:
            tooltip_parts.append(description)
        if step_count > 0:
            tooltip_parts.append(f"実ステップ数: {step_count}行")
        
        tooltip = "\n".join(tooltip_parts) if tooltip_parts else ("料率TBL (VCOPY)" if is_rate_tbl else "Program")
        
        if is_rate_tbl:
            # 料率テーブルはオレンジ色の四角形（太枠）
            graph.add_node(node_name, 
                          title=tooltip, 
                          color="#FF9800", 
                          shape="box", 
                          size=size,
                          borderWidth=4,
                          borderWidthSelected=6)
        else:
            # 通常プログラムは青色の四角形
            graph.add_node(node_name, 
                          title=tooltip, 
                          color="#2196F3", 
                          shape="box", 
                          size=size)
    
    for filepath in cbl_files:
        caller = os.path.basename(filepath).split('.')[0].upper()
        caller_description = None
        caller_step_count = 0
        call_order = 1
        in_procedure_division = False  # PROCEDURE DIVISION以降かどうかのフラグ
        
        try:
            # ファイルをUTF-8で読み込み（COBOLファイルがUTF-8の場合）
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                # UTF-8で失敗した場合はShift-JIS (cp932) で試行
                with open(filepath, 'rb') as f:
                    raw_bytes = f.read()
                content = raw_bytes.decode('cp932', errors='replace')
                lines = content.splitlines(keepends=True)
                
            for idx, line in enumerate(lines):
                # PROCEDURE DIVISIONの検出
                if re.search(r'PROCEDURE\s+DIVISION', line, re.IGNORECASE):
                    in_procedure_division = True
                
                # 実ステップ数カウント（PROCEDURE DIVISION以降のみ、コメント行・空行を除く）
                if in_procedure_division and len(line) > 6 and line[6] not in ['*', '/'] and line.strip():
                    caller_step_count += 1
                
                # コメント行スキップ（PROGRAM-ID検出以外）
                if len(line) > 6 and line[6] in ['*', '/']:
                    continue
                
                # PROGRAM-IDの特定
                prog_match = prog_id_pattern.search(line)
                if prog_match:
                    caller = prog_match.group(1).upper()
                    # PROGRAM-ID直後のコメントから説明を抽出
                    caller_description = extract_program_description(lines, idx + 1)
                
                # CALL文の特定
                call_match = call_pattern.search(line)
                if call_match:
                    callee = call_match.group(1).upper()
                    # 呼び出し先のノードが未登録の場合のみ追加（説明なし、ステップ数不明）
                    if callee not in G.nodes:
                        add_smart_node(G, callee)
                    
                    # 順序付きエッジの追加
                    label_text = f"[{call_order}]"
                    G.add_edge(caller, callee, 
                              label=label_text, 
                              title=f"呼出順: {call_order}番目")
                    call_order += 1
            
            # ファイル解析完了後、呼び出し元ノードを追加（ステップ数付き）
            add_smart_node(G, caller, caller_description, caller_step_count)
                    
        except Exception as e:
            print(f"エラー: {filepath} ({e})")
    
    return G

def export_structure_data(G, output_file="call_graph_structure.txt"):
    """AI向けの構造データをテキストファイルに出力"""
    if len(G.nodes) == 0:
        print("出力するデータがありません。")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# COBOL Call Graph Dependency List\n")
        f.write("# Format: [Caller] --calls [order]--> [Callee]\n\n")
        
        # 呼び出し関係を1行ずつ出力
        # 呼び出し元でソート
        edges_sorted = sorted(G.edges(data=True), key=lambda x: (x[0], x[2].get('label', '')))
        
        for source, target, data in edges_sorted:
            label = data.get('label', '').strip('[]')  # [1] -> 1
            
            # 呼び出し先が料率TBLかチェック
            target_title = G.nodes[target].get('title', '')
            is_rate_tbl = "料率TBL" in target_title
            callee_suffix = " (RateTable)" if is_rate_tbl else ""
            
            f.write(f"- {source} --calls [{label}]--> {target}{callee_suffix}\n")
    
    print(f"✅ AI向け構造データを {output_file} に出力しました。")


def visualize_offline_graph(G, output_html="offline_call_graph.html"):
    """完全オフライン対応のHTMLを生成"""
    if len(G.nodes) == 0:
        print("可視化するデータがありません。")
        return
    
    # cdn_resources='in_line' により完全オフライン対応のHTMLを生成
    net = Network(height="800px", 
                  width="100%", 
                  bgcolor="#222222", 
                  font_color="white", 
                  directed=True, 
                  cdn_resources='in_line')
    
    net.from_nx(G)
    
    # ノードが重ならないよう物理演算を調整
    net.repulsion(node_distance=250, 
                  central_gravity=0.1, 
                  spring_length=200, 
                  spring_strength=0.05)
    
    # UTF-8で出力（cp932エンコードエラー回避 + 文字化け対策）
    html_content = net.generate_html()
    
    # HTMLにUTF-8メタタグを追加（文字化け対策）
    if '<head>' in html_content and '<meta charset' not in html_content:
        html_content = html_content.replace('<head>', '<head>\n<meta charset="utf-8">')
    
    with open(output_html, 'w', encoding='utf-8', errors='surrogatepass') as f:
        f.write(html_content)
    print(f"✅ 完了！ 完全オフライン対応のHTMLを {output_html} に出力しました。")

# 実行
if __name__ == "__main__":
    TARGET_FOLDER = "./cobol_src"
    graph = analyze_cobol_folder(TARGET_FOLDER)
    visualize_offline_graph(graph)
    export_structure_data(graph)
