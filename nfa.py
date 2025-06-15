from typing import Set, Dict
from graphviz import Digraph

class NFA:
    def __init__(self, states: Set[str], alphabet: Set[str], 
                 transitions: Dict[str, Dict[str, Set[str]]],
                 initial_states: Set[str], final_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_states = initial_states
        self.final_states = final_states

    def process_string(self, input_string: str) -> bool:
        current_states = self.initial_states.copy()
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])
            current_states = next_states
        return bool(current_states & self.final_states)

    def visualize(self) -> Digraph:
        dot = Digraph(format="png")
        dot.attr(rankdir='LR')
        dot.node('', shape='none')
        for state in self.initial_states:
            dot.edge('', state)
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')
        for from_state, symbol_dict in self.transitions.items():
            for symbol, to_states in symbol_dict.items():
                for to_state in to_states:
                    dot.edge(from_state, to_state, label=symbol)
        return dot
