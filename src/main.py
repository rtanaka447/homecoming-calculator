from pathlib import Path

import networkx as nx
import pandas as pd
import streamlit as st

from Edge import Edge, str_path


def read_input_dataframe(df: pd.DataFrame) -> list[Edge]:
    """DataFrameを読み込み、Edgeのリストを返す関数"""
    edges = []
    print(f"{Edge.cost_per_hour=}")
    for _, row in df.iterrows():
        u = row["u"]
        v = row["v"]
        cost = row["cost"]
        time = row["time"]
        method = row["method"]
        if u is None:
            continue
        edge = Edge(u, v, cost, time, method)
        edges.append(edge)
    return edges


def get_node_list(df: pd.DataFrame) -> list[str]:
    """頂点集合を取得する関数"""
    node_set = set(df["u"]).union(set(df["v"]))
    return list(node_set)


def build_graph(edges: list[Edge]) -> nx.Graph:
    """
    辺の集合から有向グラフを構築する関数。多重辺はコスパのよいものを選ぶ。
    Args:
        edges (list[Edge]): 辺のリスト
    Returns:
        nx.Graph: グラフ
    """
    G = nx.Graph()
    for edge in edges:
        if (edge.u, edge.v) in G.edges:
            existing_weight = G[edge.u][edge.v]["weight"]
            if edge.weight < existing_weight:
                G[edge.u][edge.v]["weight"] = edge.weight
                G[edge.u][edge.v]["cost"] = edge.cost
                G[edge.u][edge.v]["time"] = edge.time
                G[edge.u][edge.v]["method"] = edge.method
        else:
            G.add_edge(
                edge.u,
                edge.v,
                weight=edge.weight,
                time=edge.time,
                cost=edge.cost,
                method=edge.method,
            )
    return G


st.title("帰省の経路計算くん")
st.markdown("""
    - このアプリは、帰省の経路を計算するためのものです。出発地と目的地を選択してボタンを押下すると良さげな経路を出してくれます。
    - 日本語の入力が少し面倒なので、Googleスプレッドシートなどに記入してからコピペすると楽です。
    """)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
input_files = list(DATA_DIR.glob("*.csv"))
input_file = st.selectbox(
    "CSVファイルを選択してください",
    options=input_files,
    format_func=lambda x: x.name,
    index=input_files.index(DATA_DIR / "input.csv"),
)

df = st.data_editor(
    pd.read_csv(input_file),
    num_rows="dynamic",
    use_container_width=True,
    key="input_table",
)

node_set = get_node_list(df)
start_node = st.selectbox(
    "出発地を選択してください",
    options=node_set,
    index=node_set.index("自宅") if "自宅" in node_set else 0,
)
end_node = st.selectbox(
    "目的地を選択してください",
    options=node_set,
    index=node_set.index("実家") if "実家" in node_set else 0,
)
cost_per_hour = st.number_input(
    "時給を入力してください",
    min_value=0,
    value=2000,
    step=1,
)
if st.button("経路計算"):
    Edge.update_costs(cost_per_hour)
    E = read_input_dataframe(df)
    G = build_graph(E)
    paths = nx.all_simple_paths(G, source=start_node, target=end_node)
    paths = sorted(
        paths,
        key=lambda path: sum([G[u][v]["weight"] for u, v in zip(path[:-1], path[1:])]),
    )
    st.write("最適な経路:")
    for path in paths:
        st.markdown(
            str_path(
                [
                    Edge(u, v, G[u][v]["cost"], G[u][v]["time"], G[u][v]["method"])
                    for u, v in zip(path[:-1], path[1:])
                ]
            ),
            unsafe_allow_html=True,
        )
        st.write("---")
    df.to_csv(input_file, index=False)
