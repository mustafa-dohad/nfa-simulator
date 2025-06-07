# nfa.py
# -------------------------------
# This module defines the NFA class for logic
# -------------------------------

class NFA:
    def __init__(self, num_states, alphabet, transitions, initial_states, final_states):
        """
        Initialize the NFA object with:
        - num_states: total number of states
        - alphabet: list of input symbols
        - transitions: dictionary of transitions {(state, symbol): [list of next states]}
        - initial_states: set of initial states
        - final_states: set of final (accepting) states
        """
        self.num_states = num_states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_states = initial_states
        self.final_states = final_states

    def next_states(self, current_states, symbol):
        """
        Given a set of current states and an input symbol,
        compute the next set of states after transition.
        """
        next_set = set()
        for state in current_states:
            # Add next states for this (state, symbol) pair if available
            next_set.update(self.transitions.get((state, symbol), []))
        return next_set
