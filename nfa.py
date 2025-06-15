from typing import Set, Dict
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

class NFA:
    def __init__(self, states: Set[str], alphabet: Set[str],
                 transitions: Dict[str, Dict[str, Set[str]]],
                 initial_states: Set[str], final_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_states = initial_states
        self.final_states = final_states
        self.current_states = set()

    def reset(self):
        self.current_states = self.initial_states.copy()

    def step(self, symbol: str):
        new_states = set()
        for state in self.current_states:
            if state in self.transitions and symbol in self.transitions[state]:
                new_states.update(self.transitions[state][symbol])
        self.current_states = new_states

    def process_string(self, input_string: str) -> bool:
        self.reset()
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            self.step(symbol)
        return any(state in self.final_states for state in self.current_states)

    def visualize(self) -> bytes:
        G = nx.MultiDiGraph()

        for state in self.states:
            G.add_node(state, shape='circle')
        for from_state, symbol_dict in self.transitions.items():
            for symbol, to_states in symbol_dict.items():
                for to_state in to_states:
                    G.add_edge(from_state, to_state, label=symbol)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
        nx.draw_networkx_labels(G, pos)

        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        for state in self.initial_states:
            plt.annotate("", xy=pos[state], xytext=(pos[state][0]-0.1, pos[state][1]),
                         arrowprops=dict(arrowstyle="->", color="green", lw=2))

        for state in self.final_states:
            nx.draw_networkx_nodes(G, pos, nodelist=[state], node_color='none',
                                   edgecolors='red', node_size=900, linewidths=2)

        plt.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.read()
