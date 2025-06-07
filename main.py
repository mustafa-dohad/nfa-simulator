# main.py
# -------------------------------
# Entry point: combine logic and GUI
# -------------------------------

import PySimpleGUI as sg
import time
from nfa import NFA
import gui

# Create first window to gather basic inputs
window1 = gui.create_initial_input_window()

while True:
    event, values = window1.read()
    if event == sg.WIN_CLOSED:
        exit()
    if event == 'Create Table':
        try:
            n = int(values['-N-'])
            initials = {int(x) for x in values['-INIT-'].split(',')}
            finals = {int(x) for x in values['-FINAL-'].split(',')}
            alpha = [x.strip() for x in values['-ALPHA-'].split(',')]
            if not alpha or n <= 0:
                raise ValueError
        except:
            sg.popup_error('Invalid input!')
            continue
        break
window1.close()

# Create main simulation window
window2 = gui.create_transition_table_window(n, alpha)

nfa = None

while True:
    event, values = window2.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Generate NFA':
        transitions = {}
        for i in range(n):
            for sym in alpha:
                cell = values[(i, sym)].strip()
                if cell:
                    transitions[(i, sym)] = [int(x) for x in cell.split(',')]
        nfa = NFA(n, alpha, transitions, initials, finals)
        img_file = gui.draw_nfa(nfa, initials)
        window2['-GRAPH-'].update(filename=img_file)
        window2['-LOG-'].update('')
        window2['-RESULT-'].update('')
    if event == 'Simulate' and nfa:
        s = values['-STRING-']
        curr = set(initials)
        window2['-LOG-'].update('')
        for c in s:
            nxt = nfa.next_states(curr, c)
            window2['-LOG-'].print(f"{curr} --{c}--> {nxt}")
            img_file = gui.draw_nfa(nfa, nxt)
            window2['-GRAPH-'].update(filename=img_file)
            window2.refresh()
            time.sleep(0.5)
            curr = nxt
        result = 'ACCEPTED' if curr & finals else 'REJECTED'
        window2['-RESULT-'].update(f"Result: {result}")

window2.close()
