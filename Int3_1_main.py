from Int3_1_automaton import Automaton

loop = True
nbr_of_automata = 44  # Total number of automata
automata = []  # List to store all automata

# Load all automata at the start of the program
for i in range(1, nbr_of_automata + 1):
    if i != 31 and i != 32 and i != 33 and i != 34 and i != 35:
        auto = Automaton()
        auto.get_from_txt(f"test_automata/Int3-1-{i}.txt")
        automata.append(auto)
print(f"{'Automaton':<10}{'Deterministic':<15}{'Complete':<10}{'Standard':<10}")

# Iterate over each automaton
for i, auto in enumerate(automata, start=1):
    # Determine if the automaton is deterministic, complete, and standard
    is_deterministic = 'Yes' if auto.is_deterministic() else 'No'
    is_complete = 'Yes' if auto.is_complete() else 'No'
    is_standard = 'Yes' if auto.is_standard() else 'No'
    # Print the automaton information
    print(f"{i:<10}{is_deterministic:<15}{is_complete:<10}{is_standard:<10}")

while loop:  # Loop the entire program
    while True:
        try:
            # Get the automaton number
            auto_nbr = int(input(f"Choose an automaton between 1 and {nbr_of_automata} (0 to exit): "))
            if 1 <= auto_nbr <= nbr_of_automata:
                print(f"\n\n--- Automaton #{auto_nbr}")
                auto = automata[auto_nbr - 1]  # Retrieve the automaton from the list
                break
            if auto_nbr == 0:
                print("Exiting ...")
                loop = False
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")
    if auto_nbr != 0:
        while True:  # Loop until the user input is valid
            try:
                # Asks for the action wanted
                user_input = int(input(" 1- Show the automaton specifications"
                                       "\n 2 - Deterministic verification"
                                       "\n 3 - Complete verification"
                                       "\n 4 - Standard verification"
                                       "\n 5 - Standardize automata"
                                       "\n 6 - Complete and determinize automata"
                                       "\n 7 - display graph"
                                       "\n 8 - completion"
                                       "\n 9 - determinization"
                                       "\n 10- minimisation"
                                       "\n 11- word recognition"
                                       "\n 12- create complement"
                                       "\nChoose an action:"))
                # Calls the function associated with the action asked
                if 1 <= user_input <= 12:
                    print(f"\n\n--- Automaton #{auto_nbr}")
                    if user_input == 1:
                        auto.show()
                    elif user_input == 2:
                        print("This automaton is deterministic" if auto.is_deterministic() else "This automaton is not deterministic")
                    elif user_input == 3:
                        print("This automaton is complete" if auto.is_complete() else "This automaton is not complete")
                    elif user_input == 4:
                        print("This automaton is standard" if auto.is_standard() else "This automaton is not standard")
                    elif user_input == 5:
                        auto.standardize()
                        print("The automaton has been standardized\n\nNew standardized automaton ", end="")
                        auto.show()
                    elif user_input == 6:
                        auto.determinization_and_completion()
                        print("The automaton is now complete deterministic\n\nNew complete deterministic automaton ", end="")
                        auto.show()
                    elif user_input == 7:
                        print("if the node is both an initial state and a final state, its color is orange. "
                              "\nIf the node is only an initial state, its color is green. "
                              "\nIf the node is only a final state, its color is red. "
                              "\nOtherwise, its color is light blue.")
                        auto.display_graph()
                    elif user_input == 8:
                        auto.completion()
                        print("The automaton is now complete\n\nNew complete automaton ", end="")
                        auto.show()
                    elif user_input == 9:
                        auto.determinize()
                        print("The automaton is now determinized\n\nNew determinized automaton ", end="")
                        auto.show()
                    elif user_input == 10:
                        auto.minimize()
                        print("The automaton is now minimized\n\nNew minimized automaton ", end="")
                        auto.show()
                    elif user_input == 11:
                        word = input("Enter the word to test:")
                        if auto.recognize_word(word):
                            print("\nword recognized")
                        else:
                            print("\nword not recognized")
                    elif user_input == 12:
                        complementary_auto = auto.create_complement()
                        print("\nNew automaton reading the complementary language", end="")
                        complementary_auto.show()
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        input("Press ENTER to continue")
        print("\n\n\n")
