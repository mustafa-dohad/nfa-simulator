"""
gui.py - PySimpleGUI interface for NFA simulator
"""

import PySimpleGUI as sg
from typing import Dict, Set, List, Optional, Tuple
from nfa import NFA

sg.theme('LightBlue2')

class NFAGUI:
    def __init__(self):
        self.nfa = None
        self.state_count = 0
        self.alphabet = set()
        self.transitions = {}
        self.initial_states = set()
        self.final_states = set()

    def create_state_input_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Text("Number of States:", size=(15, 1)), 
             sg.InputText("3", key='-STATE_COUNT-', size=(5, 1))],
            [sg.Text("Initial State(s):", size=(15, 1)), 
             sg.InputText("0", key='-INITIAL_STATES-', size=(20, 1)),
             sg.Text("(comma separated)")],
            [sg.Text("Final State(s):", size=(15, 1)), 
             sg.InputText("2", key='-FINAL_STATES-', size=(20, 1)),
             sg.Text("(comma separated)")],
        ]

    def create_alphabet_input_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Text("Alphabet:", size=(15, 1)), 
             sg.InputText("a,b", key='-ALPHABET-', size=(20, 1)),
             sg.Text("(comma separated symbols)")]
        ]

    def create_transition_table_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Text("Transition Table:", font=('Helvetica', 12, 'bold'))],
            [sg.Table(values=[], 
                     headings=['State'] + sorted(list(self.alphabet) or ['a', 'b']), 
                     key='-TRANSITION_TABLE-',
                     col_widths=[8]*3,
                     auto_size_columns=False,
                     display_row_numbers=False,
                     justification='center',
                     num_rows=5,
                     alternating_row_color='lightyellow',
                     tooltip='Double click to edit transitions',
                     enable_click_events=True)],
            [sg.Button("Update Transition Table", key='-UPDATE_TRANS_TABLE-')],
            [sg.Text("Double-click a cell to edit transitions", font=('Helvetica', 8))]
        ]

    def create_visualization_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Text("NFA Diagram:", font=('Helvetica', 12, 'bold'))],
            [sg.Image(key='-NFA_IMAGE-', size=(400, 300))],
            [sg.Button("Generate NFA", key='-GENERATE_NFA-')]
        ]

    def create_simulation_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Text("Input String:", size=(10, 1)), 
             sg.InputText("", key='-INPUT_STRING-', size=(20, 1)),
             sg.Button("Simulate", key='-SIMULATE-')],
            [sg.Text("Simulation Steps:", font=('Helvetica', 12, 'bold'))],
            [sg.Multiline("", key='-SIMULATION_STEPS-', size=(50, 10), 
             disabled=True, autoscroll=True)],
            [sg.Button("Step", key='-STEP-', disabled=True),
             sg.Button("Reset Simulation", key='-RESET_SIMULATION-')]
        ]

    def create_layout(self) -> List[List[sg.Element]]:
        return [
            [sg.Column(self.create_state_input_layout()), 
             sg.Column(self.create_alphabet_input_layout())],
            [sg.HorizontalSeparator()],
            [sg.Column(self.create_transition_table_layout(), key='-TRANS_TABLE_COL-')],
            [sg.HorizontalSeparator()],
            [sg.Column(self.create_visualization_layout()),
             sg.Column(self.create_simulation_layout())],
            [sg.Button("Reset All", key='-RESET_ALL-'), sg.Button("Exit")]
        ]

    def parse_states_input(self, states_str: str) -> Set[int]:
        try:
            states = {int(s.strip()) for s in states_str.split(',') if s.strip()}
            for state in states:
                if state < 0 or state >= self.state_count:
                    raise ValueError(f"State {state} is out of range (0-{self.state_count-1})")
            return states
        except ValueError as e:
            raise ValueError(f"Invalid state input: {e}")

    def parse_alphabet_input(self, alphabet_str: str) -> Set[str]:
        symbols = {s.strip() for s in alphabet_str.split(',') if s.strip()}
        if not symbols:
            raise ValueError("Alphabet cannot be empty")
        return symbols

    def update_transition_table(self, window: sg.Window):
        try:
            self.state_count = int(window['-STATE_COUNT-'].get())
            self.alphabet = self.parse_alphabet_input(window['-ALPHABET-'].get())
        except ValueError as e:
            sg.popup_error(f"Invalid input: {e}")
            return

        table_data = []
        for state in range(self.state_count):
            row = [str(state)]
            for symbol in sorted(self.alphabet):
                transitions = self.transitions.get(state, {}).get(symbol, set())
                row.append(','.join(str(s) for s in sorted(transitions)) if transitions else '∅')
            table_data.append(row)

        headings = ['State'] + sorted(self.alphabet)
        window['-TRANS_TABLE_COL-'].update(
            self.create_transition_table_layout()
        )
        window['-TRANSITION_TABLE-'].update(values=table_data)


    def handle_table_edit(self, window: sg.Window, row: int, col: int):
        if col == 0:
            return

        alphabet = sorted(self.alphabet)
        symbol = alphabet[col - 1]
        state = row

        table_data = window['-TRANSITION_TABLE-'].Values
        current_value = table_data[row][col]

        new_value = sg.popup_get_text(
            f"Transition from state {state} on symbol '{symbol}'",
            default_text=current_value if current_value != '∅' else '',
            keep_on_top=True)

        if new_value is not None:
            try:
                to_states = {int(s.strip()) for s in new_value.split(',') if s.strip()} if new_value.strip() else set()
                for s in to_states:
                    if s < 0 or s >= self.state_count:
                        raise ValueError(f"State {s} is out of range")

                if state not in self.transitions:
                    self.transitions[state] = {}
                self.transitions[state][symbol] = to_states

                table_data[row][col] = ','.join(str(s) for s in sorted(to_states)) if to_states else '∅'
                window['-TRANSITION_TABLE-'].update(values=table_data)

            except ValueError as e:
                sg.popup_error(f"Invalid input: {e}")

    def create_nfa(self, window: sg.Window) -> bool:
        try:
            self.state_count = int(window['-STATE_COUNT-'].get())
            states = set(range(self.state_count))

            self.initial_states = self.parse_states_input(window['-INITIAL_STATES-'].get())
            self.final_states = self.parse_states_input(window['-FINAL_STATES-'].get())
            self.alphabet = self.parse_alphabet_input(window['-ALPHABET-'].get())

            self.nfa = NFA(states, self.alphabet, self.transitions,
                           self.initial_states, self.final_states)
            return True
        except ValueError as e:
            sg.popup_error(f"Invalid input: {e}")
            return False

    def update_nfa_image(self, window: sg.Window, highlight_states: Optional[Set[int]] = None):
        if self.nfa is None:
            return
        image_data = self.nfa.visualize(highlight_states)
        window['-NFA_IMAGE-'].update(data=image_data)

    def run_simulation_step(self, window: sg.Window, input_string: str, step: int) -> Tuple[bool, bool]:
        if step == 0:
            self.nfa.reset()
            current_symbol = "Start"
            current_states = self.nfa.current_states
            window['-SIMULATION_STEPS-'].update("")
        elif step <= len(input_string):
            current_symbol = input_string[step-1]
            current_states = self.nfa.step(current_symbol)
        else:
            return True, self.nfa.is_accepted()

        window['-SIMULATION_STEPS-'].print(f"On '{current_symbol}': {current_states}\n")
        self.update_nfa_image(window, current_states)
        return False, False

    def run(self):
        layout = self.create_layout()
        window = sg.Window("NFA Simulator", layout, finalize=True)

        self.update_transition_table(window)
        simulation_step = 0
        simulation_running = False
        input_string = ""

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == '-UPDATE_TRANS_TABLE-':
                self.update_transition_table(window)

            elif event == '-GENERATE_NFA-':
                if self.create_nfa(window):
                    sg.popup("NFA Created successfully!")
                    self.update_nfa_image(window)

            elif event == '-RESET_ALL-':
                window['-STATE_COUNT-'].update("3")
                window['-INITIAL_STATES-'].update("0")
                window['-FINAL_STATES-'].update("2")
                window['-ALPHABET-'].update("a,b")
                self.transitions = {}
                self.alphabet = {'a', 'b'}
                self.state_count = 3
                self.initial_states = {0}
                self.final_states = {2}
                self.nfa = None
                simulation_step = 0
                simulation_running = False
                input_string = ""
                window['-SIMULATION_STEPS-'].update("")
                window['-INPUT_STRING-'].update("")
                window['-STEP-'].update(disabled=True)
                self.update_transition_table(window)
                window['-NFA_IMAGE-'].update(data=None)

            elif event == '-SIMULATE-':
                if self.nfa is None:
                    sg.popup_error("Create the NFA first!")
                    continue
                input_string = values['-INPUT_STRING-']
                if not input_string:
                    sg.popup_error("Input string cannot be empty")
                    continue
                simulation_step = 0
                simulation_running = True
                window['-SIMULATION_STEPS-'].update("")
                window['-STEP-'].update(disabled=False)
                self.nfa.reset()
                self.update_nfa_image(window, self.nfa.current_states)

            elif event == '-STEP-':
                if not simulation_running:
                    continue
                done, accepted = self.run_simulation_step(window, input_string, simulation_step)
                simulation_step += 1
                if done:
                    sg.popup("Accepted!" if accepted else "Rejected!")
                    simulation_running = False
                    window['-STEP-'].update(disabled=True)

            elif event == '-RESET_SIMULATION-':
                simulation_step = 0
                simulation_running = False
                window['-SIMULATION_STEPS-'].update("")
                window['-STEP-'].update(disabled=True)
                if self.nfa:
                    self.nfa.reset()
                    self.update_nfa_image(window, self.nfa.current_states)

            elif isinstance(event, tuple) and event[0] == '-TRANSITION_TABLE-':
                if len(event) >= 2 and isinstance(event[1], tuple) and len(event[1]) == 2:
                    row, col = event[1]
                    self.handle_table_edit(window, row, col)

        window.close()

def main():
    app = NFAGUI()
    app.run()

if __name__ == "__main__":
    main()
