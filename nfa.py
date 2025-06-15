# Importing required standard libraries
from typing import Set, Dict, Optional  # For type hinting
from graphviz import Digraph  # Used for drawing the NFA as a graph

class NFA:
    """
    Class representing a Non-deterministic Finite Automaton (NFA).
    It supports state transitions, processing input strings, and visualization.
    """
    
    def __init__(self, states: Set[str], alphabet: Set[str], 
                 transitions: Dict[str, Dict[str, Set[str]]],
                 initial_states: Set[str], final_states: Set[str]):
        """
        Constructor for initializing the NFA.

        Args:
            states: All possible states in the NFA, e.g., {'q0', 'q1'}
            alphabet: Input symbols the NFA recognizes, e.g., {'a', 'b'}
            transitions: Transition function in the form:
                         {'q0': {'a': {'q1'}, 'b': {'q0'}}}
            initial_states: States where input starts; may be multiple
            final_states: Accepting states where strings are accepted
        """
        self.states = states  # Store all NFA states
        self.alphabet = alphabet  # Store all input symbols
        self.transitions = transitions  # Store transitions dict
        self.initial_states = initial_states  # Starting states
        self.final_states = final_states  # Accepting states

    def process_string(self, input_string: str) -> bool:
        """
        Process an input string and return whether it's accepted by the NFA.

        Args:
            input_string: The string to be tested

        Returns:
            True if string is accepted, False otherwise
        """
        current_states = self.initial_states.copy()  # Start from initial states

        for symbol in input_string:
            next_states = set()  # Temporary set for new states

            # For each active state, follow transitions via current symbol
            for state in current_states:
                if state in self.transitions:
                    if symbol in self.transitions[state]:
                        # Add all destination states for (state, symbol)
                        next_states.update(self.transitions[state][symbol])
            current_states = next_states  # Move to next set of states

        # If any final state is in current states, string is accepted
        return bool(current_states & self.final_states)

    def visualize(self) -> Digraph:
        """
        Visualize the NFA using Graphviz and return a Digraph object.

        Returns:
            Digraph: A visual graph of the NFA
        """
        dot = Digraph(format="png")
        dot.attr(rankdir='LR')  # Layout from left to right

        # Dummy invisible start node pointing to initial states
        dot.node('', shape='none')
        for state in self.initial_states:
            dot.edge('', state)  # Arrow to initial state

        # Draw all states
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')  # Final state
            else:
                dot.node(state, shape='circle')  # Normal state

        # Add transitions (edges)
        for from_state, symbol_dict in self.transitions.items():
            for symbol, to_states in symbol_dict.items():
                for to_state in to_states:
                    dot.edge(from_state, to_state, label=symbol)

        return dot  # Return graph object to be rendered elsewhere
