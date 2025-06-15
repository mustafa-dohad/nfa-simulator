import PySimpleGUI as sg
from nfa import NFA
import base64

class NFAGUI:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transition_table = []
        self.initial_states = set()
        self.final_states = set()

    def run(self):
        layout = [
            [sg.Text("Number of States:"), sg.Input(key="-NUM_STATES-", size=(5,1)),
             sg.Text("Alphabet (comma separated):"), sg.Input(key="-ALPHABET-")],
            [sg.Button("Set States"), sg.Button("Exit")]
        ]
        window = sg.Window("NFA Simulator", layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            if event == "Set States":
                try:
                    num_states = int(values["-NUM_STATES-"])
                    self.states = [f"q{i}" for i in range(num_states)]
                    self.alphabet = [a.strip() for a in values["-ALPHABET-"].split(",") if a.strip()]
                    self.transition_table = [[""] * len(self.alphabet) for _ in self.states]
                    window.close()
                    self.state_selection()
                except:
                    sg.popup("Invalid input")
        window.close()

    def state_selection(self):
        layout = [
            [sg.Text("Select initial and final states:")]
        ]
        for state in self.states:
            layout.append([
                sg.Text(state),
                sg.Checkbox("Initial", key=f"INIT-{state}"),
                sg.Checkbox("Final", key=f"FINAL-{state}")
            ])
        layout.append([sg.Button("Next")])
        window = sg.Window("Select States", layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == "Next":
                self.initial_states = {s for s in self.states if values.get(f"INIT-{s}")}
                self.final_states = {s for s in self.states if values.get(f"FINAL-{s}")}
                window.close()
                self.transition_input()
        window.close()

    def transition_input(self):
        headers = ["State"] + self.alphabet
        data = [[self.states[i]] + self.transition_table[i][:] for i in range(len(self.states))]

        layout = [
            [sg.Table(values=data, headings=headers, key="-TABLE-", enable_events=True,
                      justification='center', auto_size_columns=False,
                      col_widths=[8]+[10]*len(self.alphabet), num_rows=min(10, len(self.states)))],
            [sg.Input(key="-EDIT-", size=(20,1)), sg.Button("Apply")],
            [sg.Button("Generate NFA")]
        ]
        window = sg.Window("Transition Table", layout, finalize=True)
        selected = None
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == "-TABLE-":
                if values["-TABLE-"]:
                    row = values["-TABLE-"][0]
                    col = window["-TABLE-"].Widget.identify_column(window["-TABLE-"].Widget.winfo_pointerx() - window["-TABLE-"].Widget.winfo_rootx())
                    col = int(col.replace("#", "")) - 1
                    if col > 0:
                        selected = (row, col - 1)
            if event == "Apply" and selected:
                row, col = selected
                new_val = values["-EDIT-"]
                self.transition_table[row][col] = new_val
                data = [[self.states[i]] + self.transition_table[i][:] for i in range(len(self.states))]
                window["-TABLE-"].update(values=data)
            if event == "Generate NFA":
                transitions = {}
                for i, state in enumerate(self.states):
                    for j, symbol in enumerate(self.alphabet):
                        val = self.transition_table[i][j]
                        next_states = set(s.strip() for s in val.split(",") if s.strip())
                        if state not in transitions:
                            transitions[state] = {}
                        transitions[state][symbol] = next_states
                nfa = NFA(set(self.states), set(self.alphabet), transitions,
                          self.initial_states, self.final_states)
                image_bytes = nfa.visualize()
                b64 = base64.b64encode(image_bytes).decode("utf-8")
                window.close()
                self.simulation(nfa, b64)
                break
        window.close()

    def simulation(self, nfa, image_b64):
        layout = [
            [sg.Text("Enter input string:"), sg.Input(key="-STRING-")],
            [sg.Image(data=base64.b64decode(image_b64))],
            [sg.Button("Verify"), sg.Text("", key="-RESULT-")],
            [sg.Button("Exit")]
        ]
        window = sg.Window("Simulate String", layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            if event == "Verify":
                result = nfa.process_string(values["-STRING-"])
                window["-RESULT-"].update("Accepted" if result else "Rejected")
        window.close()
