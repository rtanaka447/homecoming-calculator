class Edge:
    """
    グラフの辺を表すクラス。
    Attributes:
        u (str): 辺の始点。
        v (str): 辺の終点。
        cost (float): 辺の移動にかかる費用（円）。
        time (float): 辺の移動にかかる時間（分）。
        weight (float): 辺の重み。cost + time * cost_per_minで計算される。
        method (str): 交通手段
    """

    cost_per_hour: float = 2000
    cost_per_min: float = cost_per_hour / 60

    @classmethod
    def update_costs(cls, new_cost: float) -> None:
        cls.cost_per_hour = new_cost
        cls.cost_per_min = new_cost / 60

    def __init__(
        self,
        u: str,
        v: str,
        cost: float,
        time: float,
        method: str,
    ):
        self.u: str = u
        self.v: str = v
        self.cost: float = cost
        self.time: float = time
        self.method: str = method
        self.weight: float = self.get_weight()

    def get_weight(self) -> float:
        return self.cost + self.time * Edge.cost_per_min


def str_path(path: list[Edge]) -> str:
    """いい感じに経路を文字列にする関数"""
    ret = f"**Total cost**: {sum(edge.cost for edge in path)} yen<br>"
    ret += f"**Total time**: {sum(edge.time for edge in path)} minutes<br>"
    ret += f"**Total value**: {sum(edge.weight for edge in path)} yen<br>"
    ret += f"**{path[0].u}** -[{path[0].method}]-> **{path[0].v}**"
    for edge in path[1:]:
        ret += f" -[{edge.method}]-> **{edge.v}**"
    return ret
