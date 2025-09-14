"""Graph database integration using NetworkX."""

import networkx as nx
from typing import Dict, List


class CitationGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_case(self, case_id: int) -> None:
        self.graph.add_node(case_id)

    def add_citation(self, source: int, target: int) -> None:
        self.graph.add_edge(source, target)

    def citations_for(self, case_id: int) -> Dict[str, List[int]]:
        return {
            "incoming": list(self.graph.predecessors(case_id)),
            "outgoing": list(self.graph.successors(case_id)),
        }


citation_graph = CitationGraph()
