# gui.py
# ---------------------------------
# This module handles GUI creation & drawing the NFA diagram
# ---------------------------------

import PySimpleGUI as sg
import networkx as nx
import os
import tempfile
from networkx.drawing.nx_agraph import to_agraph

def create_initial_input_window():
    """
    Create the first window for getting:
    - number of states
    - initial states
    - final states
    - input alphabet
    """
    sg.theme('LightBlue')

    layout = [
        [sg.Text('Number of States:'), sg.Input(key='-N-', size=(5,1))],
        [sg.Text('Initial State(s):'), sg.Input(key='-INIT-', size=(10,1))],
        [sg.Text('Final State(s):'), sg.Input(key='-FINAL-', size=(10,1))],
        [sg.Text('Alphabet (comma separated):'), sg.Input(key='-ALPHA-', size=(20,1))],
        [sg.Button('Create Table')]
    ]
    return sg.Window('NFA Builder', layout)

def create_transition_table_window(num_states, alphabet):
    """
    Create the main simulation window, with:
    - Transition table
    - Graph visualization
    - String input
    - Log output
    """
    table_layout = [[sg.Text('State/Sym')] + [sg.Text(s, size=(5,1)) for s in alphabet]]
    for i in range(num_states):
        row = [sg.Text(str(i))]
        for sym in alphabet:
            row.append(sg.Input(size=(5,1), key=(i, sym)))
        table_layout.append(row)

    layout = [
        [sg.Frame('Transitions', table_layout)],
        [sg.Button('Generate NFA'), sg.Button('Simulate'), sg.Image(key='-GRAPH-')],
        [sg.Text('Input String:'), sg.Input(key='-STRING-')],
        [sg.Multiline(key='-LOG-', size=(50,10), disabled=True)],
        [sg.Text('', size=(40,1), key='-RESULT-', text_color='red')],
        [sg.Button('Exit')]
    ]
    return sg.Window('NFA Simulator', layout, finalize=True)

def draw_nfa(nfa, active_states):
    """
    Draw the NFA diagram using networkx and graphviz.
    Highlight active_states with yellow fill color.
    Returns path to the generated PNG image.
    """
    G = nx.DiGraph()
    G.add_node('null', shape='none', label='', width=0.01)

    for i in range(nfa.num_states):
        shape = 'doublecircle' if i in nfa.final_states else 'circle'
        G.add_node(str(i), shape=shape)

    for init in nfa.initial_states:
        G.add_edge('null', str(init))

    for (src, sym), dests in nfa.transitions.items():
        for d in dests:
            G.add_edge(str(src), str(d), label=sym)

    for s in active_states:
        if str(s) in G.nodes:
            G.nodes[str(s)]['style'] = 'filled'
            G.nodes[str(s)]['fillcolor'] = 'yellow'

    A = to_agraph(G)
    A.graph_attr.update(rankdir='LR')

    tmp_dir = tempfile.gettempdir()
    img_file = os.path.join(tmp_dir, 'nfa.png')
    A.layout('dot')
    A.draw(img_file)
    return img_file
