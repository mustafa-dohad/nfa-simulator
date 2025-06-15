# Mustafa Dohad's NFA Simulator (with GUI) 

This project is a GUI-based Non-deterministic Finite Automaton (NFA) Simulator written in Python using PySimpleGUI. It allows users to:
- Define states and alphabets
- Interactively edit a transition table
- Select initial and final states using checkboxes
- Input a string to test whether the NFA accepts or rejects it
- Visualize the generated NFA using Graphviz

---

## Features

- Fully interactive GUI
- Visual state transition table with clickable cell editing
- Supports multiple initial and final states
- Automatically names states as q0, q1, ..., qN
- Validates input string against the constructed NFA
- Displays result (ACCEPTED / REJECTED) using popup
- Graphviz-based NFA visualization in PNG format

---

## How to Clone This Repo

1. Open a terminal.
2. Navigate to the folder where you want to clone the project.
3. Run the following command:

```
git clone https://github.com/mustafa-dohad/nfa-simulator.git
```

4. Navigate into the project directory:

```
cd nfa-simulator
```

5. (Optional) Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

6. Install required packages:

```
pip install -r requirements.txt
```

7. Run the simulator:

```
python3 main.py
```

---

## Requirements

- Python 3.6+
- PySimpleGUI
- graphviz (both Python package and system tool)
    - macOS: `brew install graphviz`
    - Ubuntu: `sudo apt install graphviz`
    - Windows: Use the Graphviz installer from the official website

---

## File Structure

- `nfa.py` – Contains the logic for the NFA including the transition function and simulation.
- `gui.py` – Handles the user interface, table editing, input, and Graphviz visualization.
- `main.py` – Entry point that runs the GUI.

---

## How It Works

- User is prompted to enter the number of states and the input alphabet.
- User selects initial and final states using checkboxes.
- Transition table is editable by clicking cells and entering next states.
- Input string is simulated against the NFA.
- Results (Accepted or Rejected) are shown in a popup.
- NFA structure is displayed as an image.

---

## 📺 YouTube Video Explanation

To better understand how the NFA Simulator works, check out the video tutorial below:

**▶️ [Watch the NFA Simulator Demo on YouTube](https://youtu.be/5VZsjyMqn4s?si=5l0K09kO1MducQYL)**  

The video covers:

- Setting number of states and input alphabet  
- Creating the transition table  
- Using checkboxes for initial/final states  
- Simulating strings and viewing the result  
- Visualizing the NFA with Graphviz  
---

## Author

Mustafa Murtaza Dohad 