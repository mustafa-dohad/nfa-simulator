"""
nfa.py - Core NFA logic and visualization
"""

from typing import Set, Dict, Optional
import networkx as nx
from matplotlib import pyplot as plt
from io import BytesIO

class NFA:
    """Class representing a Non-deterministic Finite Automaton."""
    
    def __init__(self, states: Set[int], alphabet: Set[str], 
                 transitions: Dict[int, Dict[str, Set[int]]],
                 initial_states: Set[int], final_states: Set[int]):
        """
        Initialize the NFA.
        
        Args:
            states: Set of state identifiers
            alphabet: Set of input symbols
            transitions: Dictionary mapping (state, symbol) to set of states
            initial_states: Set of initial states
            final_states: Set of final/accepting states
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_states = initial_states
        self.final_states = final_states
        self.current_states = set()
        self.history = []
        
    def reset(self):
        """Reset the NFA to its initial state."""
        self.current_states = self.initial_states.copy()
        self.history = [('Start', self.current_states.copy())]
        
    def step(self, symbol: str) -> Set[int]:
        """
        Process a single input symbol and return the new set of active states.
        
        Args:
            symbol: Input symbol to process
            
        Returns:
            New set of active states after processing the symbol
        """
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' not in alphabet")
            
        new_states = set()
        for state in self.current_states:
            next_states = self.transitions.get(state, {}).get(symbol, set())
            new_states.update(next_states)
            
        self.history.append((symbol, new_states.copy()))
        self.current_states = new_states
        return new_states
    
    def process_string(self, input_string: str) -> bool:
        """
        Process an entire input string and return whether it's accepted.
        
        Args:
            input_string: String to process
            
        Returns:
            True if the string is accepted, False otherwise
        """
        self.reset()
        for symbol in input_string:
            self.step(symbol)
        return self.is_accepted()
    
    def is_accepted(self) -> bool:
        """Check if the current state is an accepting state."""
        return not self.current_states.isdisjoint(self.final_states)
    
    def visualize(self, highlight_states: Optional[Set[int]] = None) -> bytes:
        """
        Generate a visualization of the NFA as a PNG image.
        
        Args:
            highlight_states: Set of states to highlight (current active states)
            
        Returns:
            Bytes of the PNG image
        """
        if highlight_states is None:
            highlight_states = set()
            
        G = nx.MultiDiGraph()
        
        for state in self.states:
            is_final = state in self.final_states
            is_initial = state in self.initial_states
            is_highlighted = state in highlight_states
            
            G.add_node(state, final=is_final, initial=is_initial, highlighted=is_highlighted)
        
        for from_state, transitions in self.transitions.items():
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    G.add_edge(from_state, to_state, label=symbol)
        
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        plt.figure(figsize=(10, 6))
        
        node_colors = []
        for node in G.nodes():
            if G.nodes[node]['highlighted']:
                node_colors.append('lightgreen')
            elif G.nodes[node]['final']:
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightblue')
                
        nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=node_colors)
        nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
        
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        
        labels = {node: str(node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels)
        
        for node in G.nodes():
            if G.nodes[node]['final']:
                nx.draw_networkx_nodes(G, pos, nodelist=[node], 
                                      node_size=1200, node_color='none', 
                                      edgecolors='black', linewidths=2.0)
        
        for node in G.nodes():
            if G.nodes[node]['initial']:
                plt.annotate('', xy=(pos[node][0]-30, pos[node][1]), 
                             xytext=(pos[node][0]-100, pos[node][1]),
                             arrowprops=dict(arrowstyle='-|>', lw=2))
        
        plt.title("NFA Visualization")
        plt.axis('off')
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return buf.read()
