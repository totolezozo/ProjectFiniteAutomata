import networkx as nx
import matplotlib.pyplot as plt


class Automaton:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z"]
    nbr_states = 0
    list_state = []
    init_states = []
    final_states = []
    transitions = []
    transition_table = []

    def get_from_txt(self, automaton_txt):  # Get the automaton from a given text file
        # Open the file and get the data
        auto_infos = [line.strip() for line in open(automaton_txt)]

        # Clear the transitions attribute
        self.transitions = []

        # Rearrange the data and make it usable in the program
        self.alphabet = self.alphabet[0:int(auto_infos[0])]

        self.nbr_states = int(auto_infos[1])

        string_parts = auto_infos[2].split()
        string_parts.pop(0)
        self.init_states = [part for part in string_parts]

        string_parts = auto_infos[3].split()
        string_parts.pop(0)
        self.final_states = [part for part in string_parts]

        for i in auto_infos[5:]:
            self.transitions.append((i[0], i[1], i[2]))

        self.get_all_states() # ad on 21/04

    def show(self):  # Print the specifications of the automaton
        print(
            f"Specifications:\n - Alphabet: {self.alphabet}\n - Number of state(s): {self.nbr_states}\n - Initial state(s) {self.init_states}\n - Final state(s) {self.final_states}\n - List of the transition(s): {self.transitions}")

    def get_all_states(self):
        # Initialise un ensemble vide pour stocker les états
        states = set()

        # Parcoure les transitions
        for transition in self.transitions:
            if transition[0] not in states:
                states.add(str(transition[0]))
            if transition[2] not in states:
                states.add(str(transition[2]))

        # Convertit l'ensemble en liste et le retourne
        self.list_state = list(states)

    def is_deterministic(self):
        # Initialize variables
        transition = {}

        # Create a dictionary where each key is a tuple (start_state, symbol)
        # and each value is a list of end states
        for start_state, symbol, end_state in self.transitions:
            if (start_state, symbol) in transition:
                transition[(start_state, symbol)].append(end_state)
            else:
                transition[(start_state, symbol)] = [end_state]

        # Check if it has only one initial state
        if len(self.init_states) != 1:
            return False

        # Check if there are no states in which starts more than one arrow labeled by the same character
        for end_states in transition.values():
            if len(end_states) > 1:
                return False

        # Otherwise it is deterministic
        return True

    def is_complete(self):
        self.get_all_states()

        starter_states=set()

        # go throught transitions
        for transition in self.transitions:
            if transition[ 0 ] not in starter_states:
                starter_states.add(str(transition[ 0 ]))
        self.list_state=list(starter_states)
        # Check if there's a transition for every state and input symbol
        for state in starter_states:
            for symbol in self.alphabet:
                if not any(t[ 0 ] == state and t[ 1 ] == symbol for t in self.transitions):
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
            if transition[2] == initial_state:
                return False

        # Otherwise, it is standard
        return True

    def is_standardizable(self):
        # Vérifier si un des états initiaux a une boucle sur lui-même
        for state in self.init_states:
            for transition in self.transitions:
                if transition[0] == state and transition[2] == state:
                    return False
        return True

    def standardize(self):
        if not self.is_standard():
            if not self.is_standardizable():
                print("this automata is not stanardizable by our algorithm.")
                return

            # Ajouter un nouvel état initial
            self.nbr_states += 1
            new_init_state = 'i'

            # Copier les transitions des anciens états initiaux
            old_transitions = self.transitions.copy()
            for state, symbol, next_state in old_transitions:
                if state in self.init_states:
                    self.transitions.append((new_init_state, symbol, next_state))

            # Mettre à jour les états initiaux
            self.init_states = [new_init_state]

            if not self.is_standard():
                print("Error during the standardization")

    def completion(self):
        # If the automaton is not complete, add a new state
        if not self.is_complete():
            # Add missing transitions to the trash state
            for symbol in self.alphabet:
                self.transitions.append(('p', symbol, 'p'))
            # Add missing transitions for each state and each symbol
            for state in self.list_state:
                for symbol in self.alphabet:
                    if not any(t[0] == state and t[1] == symbol for t in self.transitions):
                        self.transitions.append((state, symbol, 'p'))

            self.nbr_states += 1

    def determinization_and_completion(self):
        # If the automaton is not deterministic, apply the determinization algorithm
        if not self.is_deterministic():
            self.determinize()
        # If the automaton is not complete, apply the completion method
        if not self.is_complete():
            self.completion()

    def display_graph(self):
        G = nx.MultiDiGraph()
        G.add_nodes_from(self.list_state)
        edge_labels = {}
        for transition in self.transitions:
            start_state = transition[0]
            symbol = transition[1]
            end_state = transition[2]
            G.add_edge(start_state, end_state)
            edge_labels[(start_state, end_state)] = symbol

        node_colors = []
        for node in G.nodes():
            if node in self.init_states and node in self.final_states:
                node_colors.append('orange')
            elif node in self.init_states:
                node_colors.append('green')
            elif node in self.final_states:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1200)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()

    def construct_from_partition(self, partition):
        # Create a new transition table
        new_transition_table = []

        for part in partition:
            # Choose a representative state from the partition
            representative = list(part)[0]

            # Create a new row in the transition table for this partition
            new_row = []
            for symbol in range(len(self.alphabet)):
                next_state = self.transition_table[representative][symbol]

                # Find which partition the next state belongs to
                for i, part2 in enumerate(partition):
                    if next_state in part2:
                        new_row.append(i)
                        break

            new_transition_table.append(new_row)

        # Replace the old transition table with the new one
        self.transition_table = new_transition_table

        # Update the number of states
        self.nbr_states = len(partition)

        # Update the final states
        self.final_states = [i for i, part in enumerate(partition) if self.final_states[0] in part]

    def split(self, states, partition):
        print(f"Splitting states: {states} with partition: {partition}")
        subsets = []
        for symbol in range(len(self.alphabet)):
            groups = {}
            for state in states:
                print(f"Current state: {state}, symbol: {symbol}")
                print(f"Transition table size: {len(self.transition_table)}")
                if state < len(self.transition_table) and symbol < len(self.transition_table[state]):
                    next_state = self.transition_table[state][symbol]
                    print(f"Next state for state {state} and symbol {symbol}: {next_state}")

                    for i, part in enumerate(partition):
                        if next_state in part:
                            groups.setdefault(i, []).append(state)
                            print(f"State {state} grouped in partition {i}")
                            break
                else:
                    print(f"Invalid index: state={state}, symbol={symbol}")
            subsets.extend(groups.values())
            print(f"Subsets after processing symbol {symbol}: {subsets}")
        return subsets

    def minimize(self):
        # Step 1: Partition states into final and non-final
        print("step 1 : Partition states into final and non-final ")
        partition = [set(self.final_states), set(range(self.nbr_states)) - set(self.final_states)]
        for i, subset in enumerate(partition):
            print(f"Contenu du sous-ensemble {i + 1} :")
            for state in subset:
                print(state)

        # Step 2: Iteratively refine the partition
        print("step 2")
        while True:
            new_partition = []
            for part in partition:
                subsets = self.split(part, partition)
                new_partition.extend(subsets)
            if len(new_partition) == len(partition):
                break
            partition = new_partition

        # Step 3: Construct the new minimized DFA from the partition
        self.construct_from_partition(partition)

        # Step 4: Display the minimized DFA
        self.display_minimal_automaton(partition)

    def display_minimal_automaton(self, partition):
        print("Minimized DFA:")
        for i, part in enumerate(partition):
            print(f"State {i}: corresponds to {part} in the original DFA")
            for symbol in range(len(self.alphabet)):
                next_state = self.transition_table[list(part)[0]][symbol]
                for j, part2 in enumerate(partition):
                    if next_state in part2:
                        print(f"  On symbol {symbol}, transitions to state {j}")
                        break

    def update_self(self, other):
        self.alphabet = other.alphabet
        self.nbr_states = other.nbr_states
        self.init_states = other.init_states
        self.final_states = other.final_states
        self.transitions = other.transitions

    def add_transition(self, source, letter, target):
        self.transitions.append((source, letter, target))

    def set_final(self, state):
        self.final_states.append(state)

    def set_initial(self, state):
        self.init_states.append(state)

    def determinize(self):
        print("Starting determinization...")
        self.show()
        state_dealt_with=[ ]
        state_to_deal_with=self.init_states
        new_transition=[ ]
        while state_to_deal_with != [ ]:
            state_in_treatment_transition_s=[ ]
            state_in_treatment=state_to_deal_with[ 0 ]
            print("State in treatment:", state_in_treatment)
            for start_state, symbol, end_state in self.transitions:
                if start_state in state_in_treatment[ 0 ]:
                    state_in_treatment_transition_s.append((start_state, symbol, end_state))
            for letter in self.alphabet:
                transition_to_add= [ state_in_treatment, letter, '' ]
                for starter, symb, ender in state_in_treatment_transition_s:
                    if symb == letter:
                        if len(transition_to_add[ 2 ]) != 0:
                            transition_to_add[ 2 ]=transition_to_add[ 2 ] + ',' + ender
                        else:
                            transition_to_add[ 2 ]=ender
                if transition_to_add[ 2 ] != '':
                    new_transition.append(tuple(transition_to_add))
                    if transition_to_add[ 2 ] not in state_to_deal_with and transition_to_add[2 ] not in state_dealt_with:
                        state_to_deal_with.append(transition_to_add[ 2 ])
            state_to_deal_with.remove(transition_to_add[ 0 ])
            state_dealt_with.append(transition_to_add[ 0 ])
            print("States dealt with:", state_dealt_with)
        self.transitions=new_transition
        self.get_all_states()
        self.nbr_states=len(self.list_state)
        print("Determinization completed. New transitions:", self.transitions)

    def recognize_word(self, word):
        current_states = set(self.init_states)

        for letter in word:
            next_states = set()

            for state in current_states:
                for transition in self.transitions:
                    if transition[0] == state and transition[1] == letter:
                        next_states.add(transition[2])

            if not next_states:
                return False  # If there are no transitions for the current letter, the word is not recognized

            current_states = next_states

        # Check if any of the current states are final states
        if any(state in current_states for state in self.final_states):
            return True
        else:
            return False

    def create_complement(self):
        # Invert final and non-final states
        complement_final_states = list(set(self.list_state) - set(self.final_states))

        # Create a new instance of Automaton
        complement_automaton = Automaton()

        # Update the attributes of the new automaton
        complement_automaton.alphabet = self.alphabet
        complement_automaton.nbr_states = self.nbr_states
        complement_automaton.init_states = self.init_states
        complement_automaton.final_states = complement_final_states

        # Invert the transitions for non-final to final states and vice versa
        complement_transitions = []
        for transition in self.transitions:
            start_state = transition[0]
            letter = transition[1]
            end_state = transition[2]

            # If the start state is final and the end state is non-final, swap them
            if start_state in self.final_states and end_state not in self.final_states:
                complement_transitions.append((start_state, letter, end_state))

            # If the start state is non-final and the end state is final, swap them
            elif start_state not in self.final_states and end_state in self.final_states:
                complement_transitions.append((start_state, letter, end_state))

        complement_automaton.transitions = complement_transitions

        return complement_automaton
