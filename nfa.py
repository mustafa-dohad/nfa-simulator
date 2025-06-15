from graphviz import Digraph

class NFA:
    def __init__(self, states, alphabet, transition_function, initial_states, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.initial_states = initial_states
        self.final_states = final_states

    def accepts(self, input_str):
        current_states = self.initial_states
        for symbol in input_str:
            next_states = set()
            for state in current_states:
                if symbol in self.transition_function[state]:
                    next_states.update(self.transition_function[state][symbol])
            current_states = next_states
        return any(state in self.final_states for state in current_states)

    def visualize(self, filename="nfa_graph"):
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')

        dot.node("", shape="none")  # Starting arrow

        for state in self.states:
            shape = "doublecircle" if state in self.final_states else "circle"
            dot.node(state, shape=shape)

        for init in self.initial_states:
            dot.edge("", init)

        for state in self.transition_function:
            for symbol in self.transition_function[state]:
                for next_state in self.transition_function[state][symbol]:
                    dot.edge(state, next_state, label=symbol)

        dot.render(filename, cleanup=True)
