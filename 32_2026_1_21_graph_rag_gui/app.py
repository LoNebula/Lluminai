import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------------------------------------
# 0. 全体設定とセッション管理
# ---------------------------------------------------------
st.set_page_config(page_title="GraphRAG Visual Editor", layout="wide", page_icon="🕸️")

# グラフデータ（NetworkX）をセッションで保持
if 'graph' not in st.session_state:
    st.session_state['graph'] = nx.DiGraph()

# 接続操作用のステート（始点と終点を保持）
if 'source_node' not in st.session_state:
    st.session_state['source_node'] = None
if 'target_node' not in st.session_state:
    st.session_state['target_node'] = None

# チャット履歴
if "messages" not in st.session_state:
    st.session_state.messages = []

# APIキー管理
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

# ---------------------------------------------------------
# 1. ページ定義
# ---------------------------------------------------------

def page_editor():
    """1ページ目: グラフエディタ"""
    st.title("🕸️ Graph Editor")
    st.markdown("ノードを作成し、クリックして接続してください。")

    # --- サイドバー：ノード追加 ---
    st.sidebar.header("📦 ノード（要素）の追加")
    new_node = st.sidebar.text_input("新しいノード名を入力", placeholder="例: ルミナイ株式会社")

    if st.sidebar.button("➕ ノードを追加"):
        if new_node:
            if not st.session_state['graph'].has_node(new_node):
                st.session_state['graph'].add_node(new_node)
                st.sidebar.success(f"追加しました: {new_node}")
            else:
                st.sidebar.warning("そのノードは既に存在します。")
        else:
            st.sidebar.warning("ノード名を入力してください。")

    st.sidebar.divider()
    st.sidebar.markdown(f"**現在の要素数:** {st.session_state['graph'].number_of_nodes()}")
    st.sidebar.markdown(f"**現在の関係数:** {st.session_state['graph'].number_of_edges()}")

    if st.sidebar.button("🗑️ 全データをリセット", type="primary"):
        st.session_state['graph'].clear()
        st.session_state['source_node'] = None
        st.session_state['target_node'] = None
        st.session_state['messages'] = []
        st.rerun()

    # --- メインエリア：可視化と操作 ---
    col_graph, col_control = st.columns([3, 1])

    with col_graph:
        nodes = []
        edges = []
        # ノード設定
        for n in st.session_state['graph'].nodes():
            color = "#F7A7A6" # Default Pink
            if n == st.session_state['source_node']:
                color = "#5D5CDE" # Blue for Source
            elif n == st.session_state['target_node']:
                color = "#4CAF50" # Green for Target
            nodes.append(Node(id=n, label=n, size=25, color=color))

        # エッジ設定
        for u, v, d in st.session_state['graph'].edges(data=True):
            edges.append(Edge(source=u, target=v, label=d.get('relation', ''), type="CURVE_SMOOTH"))

        config = Config(width="100%", height=500, directed=True, 
                        nodeHighlightBehavior=True, highlightColor="#F7A7A6",
                        collapsible=False, physics=True)

        selected_node_id = agraph(nodes=nodes, edges=edges, config=config)

    with col_control:
        st.subheader("🛠️ 接続操作")
        if selected_node_id:
            st.info(f"選択中: **{selected_node_id}**")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("始点に設定"):
                    st.session_state['source_node'] = selected_node_id
                    st.rerun()
            with c2:
                if st.button("終点に設定"):
                    st.session_state['target_node'] = selected_node_id
                    st.rerun()
        else:
            st.write("👈 グラフの丸をクリック")

        st.divider()

        src = st.session_state['source_node']
        tgt = st.session_state['target_node']
        st.write(f"**始点:** {src if src else '---'}")
        st.write(f"**終点:** {tgt if tgt else '---'}")

        if src and tgt and src != tgt:
            relation_label = st.text_input("関係名 (例: 所属)", key="rel_input")
            if st.button("🔗 接続する"):
                if relation_label:
                    st.session_state['graph'].add_edge(src, tgt, relation=relation_label)
                    st.session_state['source_node'] = None
                    st.session_state['target_node'] = None
                    st.success("接続完了")
                    st.rerun()
                else:
                    st.error("関係名を入力してください")
        
        if src or tgt:
            if st.button("選択クリア"):
                st.session_state['source_node'] = None
                st.session_state['target_node'] = None
                st.rerun()
    
    # JSON確認用
    st.divider()
    with st.expander("📊 グラフデータ (JSON)"):
        st.json(nx.node_link_data(st.session_state['graph']))


def page_rag():
    """2ページ目: RAG検索（OpenAI利用）"""
    st.title("💬 Graph RAG Chat")
    st.markdown("作成したナレッジグラフに基づいて質問できます。")

    # APIキー入力
    api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_api_key)
    if api_key:
        st.session_state.openai_api_key = api_key
    
    if not st.session_state.openai_api_key:
        st.warning("チャットを行うにはOpenAI APIキーを入力してください。")
        return

    st.divider()

    # --- RAG ロジック (修正版) ---
    def retrieve_context(query, graph):
        """グラフから関連情報を検索する簡易ロジック"""
        triplets = []
        found_nodes = []
        
        # 1. キーワードマッチ（質問文に含まれるノードを探す）
        for node in graph.nodes():
            if node in query:
                found_nodes.append(node)
        
        if not found_nodes:
            # マッチしない場合は全ノード情報を返す
            data = nx.node_link_data(graph)
            # 修正箇所: バージョン依存のキーエラーを防ぐため .get() を使用
            all_links = data.get('links') or data.get('edges') or []
            
            return "（キーワードに一致するノードが見つかりませんでした。全知識を参照します）\n" + str(all_links)

        # 2. サブグラフ抽出（見つかったノードに接続するエッジを取得）
        for node in found_nodes:
            # Outgoing
            for neighbor in graph.neighbors(node):
                rel = graph.get_edge_data(node, neighbor).get('relation', 'related')
                triplets.append(f"- {node} は {neighbor} に「{rel}」しています。")
            # Incoming
            for predecessor in graph.predecessors(node):
                rel = graph.get_edge_data(predecessor, node).get('relation', 'related')
                triplets.append(f"- {predecessor} は {node} に「{rel}」しています。")
        
        return "\n".join(set(triplets))

    # --- チャットUI ---
    # 履歴表示
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 入力処理
    if prompt := st.chat_input("グラフについて聞いてください..."):
        # ユーザーの入力を表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 検索 (Retrieval)
        context = retrieve_context(prompt, st.session_state['graph'])

        # LLM生成 (Generation)
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", api_key=st.session_state.openai_api_key, temperature=0)
            
            # ▼▼▼ プロンプトを修正（ここから） ▼▼▼
            system_prompt = """
            あなたはナレッジグラフを持つAIアシスタントです。
            ユーザーの質問に対し、以下の【既知の事実 (Context)】にある情報を『最大限活用して』答えてください。
            
            【回答のルール】
            1. 「〇〇とは何か？」と聞かれた際、定義がなくても、それに接続している他のノード（関係性）について説明してください。
            2. 文脈にある事実はすべて回答に含めてください。
            3. 文脈に全く関連情報がない場合のみ、「グラフからは分かりません」と答えてください。

            【既知の事実 (Context)】
            {context}
            """
            # ▲▲▲ プロンプトを修正（ここまで） ▲▲▲
            
            chat_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("user", "{input}")
            ])
            chain = chat_template | llm | StrOutputParser()
            
            with st.chat_message("assistant"):
                # contextを変数として渡す（前の修正と同じ）
                response = chain.invoke({
                    "input": prompt,
                    "context": context
                })
                st.markdown(response)
                
                # デバッグ用に参照したコンテキストを表示
                with st.expander("🔍 参照した知識"):
                    st.text(context)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")


# ---------------------------------------------------------
# 2. ナビゲーション制御
# ---------------------------------------------------------
# サイドバーでページ切り替え
page = st.sidebar.radio("ページ選択", ["📝 1. Graph Editor", "🔍 2. RAG Search"])

if page == "📝 1. Graph Editor":
    page_editor()
elif page == "🔍 2. RAG Search":
    page_rag()