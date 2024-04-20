
import networkx as nx
import matplotlib.pyplot as plt

class Automaton:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z"]
    nbr_states = 0
    init_states = []
    final_states = []
    transitions = []
    transition_table=[]
    def get_automaton_from_txt(self, automaton_txt):  # Get the automaton from a given text file
        # Open the file and get the data
        auto_infos = [line.strip() for line in open(automaton_txt)]

        # Clear the transitions attribute
        self.transitions = []

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
            self.transitions.append((int(i[0]),i[1],int(i[2])))

    def show_automaton(self):  # Print the specifications of the automaton
        print(f"Specifications:\n - Alphabet: {self.alphabet}\n - Number of state(s): {self.nbr_states}\n - Initial state(s) {self.init_states}\n - Final state(s) {self.final_states}\n - List of the transition(s): {self.transitions}")

    def is_deterministic(self):
        # Initialize variables
        transition={}

        # Create a dictionary where each key is a tuple (start_state, symbol)
        # and each value is a list of end states
        for start_state, symbol, end_state in self.transitions:
            if (start_state, symbol) in transition:
                transition[ (start_state, symbol) ].append(end_state)
            else:
                transition[ (start_state, symbol) ]=[ end_state ]

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
        # Check if there's a transition for every state and input symbol
        for state in range(self.nbr_states):
            for symbol in self.alphabet:
                if not any(t[ 0 ] == state and t[ 1 ] == symbol for t in self.transitions):
                    return False

        # Otherwise it is complete
        return True


    def is_standardizable(self):
        # Vérifier si un des états initiaux a une boucle sur lui-même
        for state in self.init_states:
            for transition in self.transitions:
                if transition[ 0 ] == state and transition[ 2 ] == state:
                    return False
        return True

    def standardize(self):
        if not self.is_standard():
            if not self.is_standardizable():
                print("Cet automate n'est pas standardisable par notre algorithme.")
                return

            # Ajouter un nouvel état initial
            self.nbr_states+=1
            new_init_state=self.nbr_states

            # Copier les transitions des anciens états initiaux
            old_transitions=self.transitions.copy()
            for state, symbol, next_state in old_transitions:
                if state in self.init_states:
                    self.transitions.append((new_init_state, symbol, next_state))

            # Mettre à jour les états initiaux
            self.init_states=[ new_init_state ]

            if not self.is_standard():
                print("Erreur lors de la standardisation")

    def completion(self):
        # If the automaton is not complete, add a new state
        if not self.is_complete():
            # Add missing transitions to the trash state
            for symbol in self.alphabet:
                self.transitions.append((self.nbr_states, symbol, self.nbr_states))
            # Add missing transitions for each state and each symbol
            for state in range(self.nbr_states):
                for symbol in self.alphabet:
                    if not any(t[ 0 ] == state and t[ 1 ] == symbol for t in self.transitions):
                        self.transitions.append((state, symbol, self.nbr_states))

            self.nbr_states+=1



    def determinize(self):
        # Prepare for Conversion
        edges=set()
        reference_table={}
        for transition in self.transitions:
            state, edge, next_state=transition[ 0 ], transition[ 1 ], transition[ 2: ]
            edges.add(edge)
            reference_table[ (state, edge) ]=next_state

        # Initialize DFA
        dfa={(''.join(map(str, self.init_states)), edge): '' for edge in edges}
        final_table={}

        # Convert NFA to DFA
        new_nodes=list(dfa.keys())
        while new_nodes:
            new_node=new_nodes.pop(0)
            for edge in edges:
                next_states=set()
                for state in new_node[ 0 ]:
                    if (state, edge) in reference_table:
                        next_states.update(reference_table[ (state, edge) ])
                next_states=''.join(sorted(next_states))
                if next_states and next_states not in [ node[ 0 ] for node in new_nodes ]:
                    new_nodes.append((next_states, edge))
                dfa[ new_node, edge ]=next_states
                final_table[ (new_node[ 0 ], edge) ]=next_states

        # Modify the NFA to become a DFA
        self.transitions=[ (state_edge[ 0 ], state_edge[ 1 ], next_state) for state_edge, next_state in
                           final_table.items() ]
        self.init_states=[ ''.join(self.init_states) ]
        self.final_states=[ state for state in final_table.keys() if
                            any(final_state in state[ 0 ] for final_state in self.final_states) ]

    def determinization_and_completion_of_automaton(self):
        # If the automaton is not deterministic, apply the determinization algorithm
        if not self.is_deterministic():
            self.determinize()
        # If the automaton is not complete, apply the completion method
        if not self.is_complete():
            self.completion()

    def display_automaton_graph(self):
        G = nx.MultiDiGraph()
        G.add_nodes_from(range(self.nbr_states))
        edge_labels = {}
        for transition in self.transitions:
            start_state = int(transition[0])
            symbol = transition[1]
            end_state = int(transition[2])
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
            for symbol in range(self.nbr_symbols):
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
