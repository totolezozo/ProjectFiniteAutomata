class Automaton:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z"]
    nbr_states = 0
    init_states = []
    final_states = []
    transitions = []

    def get_automaton_from_txt(self, automaton_txt):  # Get the automaton from a given text file
        # Open the file and get the data
        auto_infos = [line.strip() for line in open(automaton_txt)]
        # Rearrange the data and make it usable in the program
        self.alphabet = self.alphabet[0:int(auto_infos[0])]

        self.nbr_states = int(auto_infos[1])

        string_parts = auto_infos[2].split()
        string_parts.pop(0)
        self.init_states = [int(part) for part in string_parts]

        string_parts = auto_infos[3].split()
        string_parts.pop(0)
        self.final_states = [int(part) for part in string_parts]

        for i in auto_infos[5:]:
            self.transitions.append(i)

    def show_automaton(self):  # Print the specifications of the automaton
        print(f"Specifications:\n - Alphabet: {self.alphabet}\n - Number of state(s): {self.nbr_states}\n - Initial state(s) {self.init_states}\n - Final state(s) {self.final_states}\n - List of the transition(s): {self.transitions}")

    def is_deterministic(self):
        # Initialize variables
        seen_start = set()
        transition = {}
        for i in self.transitions:
            transition[i[0]] = i[1]

        # Check if it has only one entry
        if len(self.init_states) != 1:
            return False

        # Check if there are no states in which starts more than one arrow labeled by the same character
        for start_transition, symbol in transition.items():
            if start_transition in seen_start:
                if symbol == transition[start_transition]:
                    return False
            else:
                seen_start.add(start_transition)

        # Otherwise it is deterministic
        return True

    def is_complete(self):
        # Makes a set of all states and symbols
        all_states = set()
        all_symbols = set()
        for state, symbol, next_state in self.transitions:
            all_states.add(state)
            all_states.add(next_state)
            all_symbols.add(symbol)

        # Check if there's a transition for every state and input symbol
        for state in all_states:
            for symbol in all_symbols:
                if (state, symbol) not in self.transitions:
                    return False

        # Otherwise it is complete
        return True

    def is_standard(self):
        # Check if it has only one entry
        if len(self.init_states) != 1:
            return False

        # Check if there are no transitions arriving at the initial state
        initial_state = self.init_states[0]
        for transition in self.transitions:
            if transition[1] == initial_state:
                return False

        # Otherwise, it is standard
        return True
