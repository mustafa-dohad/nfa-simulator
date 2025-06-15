import PySimpleGUI as sg
from nfa import NFA
import os

class NFAGUI:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transition_table_data = []
        self.transition_table = {}
        self.initial_states = set()
        self.final_states = set()

    def run(self):
        sg.theme("DarkBlue3")
        layout = [
            [sg.Text("Enter number of states:"), sg.Input(key="-NUM_STATES-", size=(5, 1)),
             sg.Text("Enter alphabet (comma-separated):"), sg.Input(key="-ALPHABET-", size=(15, 1))],
            [sg.Button("Set States and Alphabet"), sg.Button("Exit")]
        ]
        window = sg.Window("NFA Simulator Setup", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Exit"):
                break
            elif event == "Set States and Alphabet":
                try:
                    self.set_states_and_alphabet(window, values["-NUM_STATES-"], values["-ALPHABET-"])
                    window.close()
                    self.build_main_window()
                except Exception as e:
                    sg.popup_error(f"Error setting states or alphabet: {e}")
        window.close()

    def set_states_and_alphabet(self, window, num_states_str, alphabet_str):
        num_states = int(num_states_str)
        self.states = [f"q{i}" for i in range(num_states)]
        self.alphabet = [sym.strip() for sym in alphabet_str.split(",") if sym.strip()]
        self.transition_table_data = [["" for _ in self.alphabet] for _ in self.states]
        self.transition_table = {state: {symbol: set() for symbol in self.alphabet} for state in self.states}

    def build_main_window(self):
        table = sg.Table(
            values=self.transition_table_data,
            headings=self.alphabet,
            key="-TABLE-",
            enable_events=True,
            justification="center",
            num_rows=min(10, len(self.states)),
            auto_size_columns=True,
            expand_x=True,
            expand_y=True,
        )

        checkbox_col = [[
            sg.Checkbox(f"{state} (Initial)", key=f"-INIT-{state}"),
            sg.Checkbox(f"{state} (Final)", key=f"-FINAL-{state}")
        ] for state in self.states]

        layout = [
            [sg.Text("Transition Table:"), table],
            [sg.Column(checkbox_col, key="-CHECKBOX_COL-")],
            [sg.Text("Enter input string:"), sg.Input(key="-INPUT-", size=(20, 1))],
            [sg.Button("Generate NFA"), sg.Button("Simulate"), sg.Button("Exit")]
        ]

        window = sg.Window("NFA Simulator", layout, finalize=True)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Exit"):
                break

            elif event == "-TABLE-":
                selected_rows = values["-TABLE-"]
                if selected_rows:
                    row = selected_rows[0]

                    col_layout = [[sg.Text(f"Choose symbol column for {self.states[row]}:")]]
                    for idx, sym in enumerate(self.alphabet):
                        col_layout.append([sg.Button(f"{idx}: {sym}", key=f"-SYMBOL-{idx}-")])
                    col_win = sg.Window("Choose Symbol", col_layout)
                    col_event, _ = col_win.read()
                    col_win.close()

                    if col_event and col_event.startswith("-SYMBOL-"):
                        col = int(col_event.split("-")[2])
                        symbol = self.alphabet[col]
                        state = self.states[row]
                        result = sg.popup_get_text(f"Enter next states for {state} on symbol '{symbol}' (comma-separated):")
                        if result is not None:
                            next_states = {s.strip() for s in result.split(",") if s.strip()}
                            self.transition_table_data[row][col] = ", ".join(next_states)
                            self.transition_table[state][symbol] = next_states
                            window["-TABLE-"].update(values=self.transition_table_data)

            elif event == "Generate NFA":
                self.initial_states = {state for state in self.states if values.get(f"-INIT-{state}")}
                self.final_states = {state for state in self.states if values.get(f"-FINAL-{state}")}
                try:
                    nfa = NFA(
                        states=self.states,
                        alphabet=self.alphabet,
                        transition_function=self.transition_table,
                        initial_states=self.initial_states,
                        final_states=self.final_states
                    )
                    nfa.visualize("nfa_graph")
                    os.system("open nfa_graph.png" if os.name == "posix" else "start nfa_graph.png")
                except Exception as e:
                    sg.popup_error(f"Error generating NFA: {e}")

            elif event == "Simulate":
                input_str = values["-INPUT-"]
                try:
                    nfa = NFA(
                        states=self.states,
                        alphabet=self.alphabet,
                        transition_function=self.transition_table,
                        initial_states={s for s in self.states if values.get(f"-INIT-{s}")},
                        final_states={s for s in self.states if values.get(f"-FINAL-{s}")}
                    )
                    accepted = nfa.accepts(input_str)
                    sg.popup("Result", f"String {'ACCEPTED' if accepted else 'REJECTED'} by the NFA.")
                except Exception as e:
                    sg.popup_error(f"Error during simulation: {e}")

        window.close()
