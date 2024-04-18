from Int3_1_automaton import Automaton

Nombre_automata = 8
loop = True
automata=[]  # list to store all automata

# Load all automata at the start of the program
for i in range(1, Nombre_automata + 1):
    auto=Automaton()
    auto.get_automaton_from_txt(f"automata/Int3-1-{i}.txt")
    automata.append(auto)
print(f"{'Automaton':<10}{'Deterministic':<15}{'Complete':<10}{'Standard':<10}")

# Iterate over each automaton
for i, auto in enumerate(automata, start=1):
    # Determine if the automaton is deterministic, complete, and standard
    is_deterministic='Yes' if auto.is_deterministic() else 'No'
    is_complete='Yes' if auto.is_complete() else 'No'
    is_standard='Yes' if auto.is_standard() else 'No'

    # Print the automaton information
    print(f"{i:<10}{is_deterministic:<15}{is_complete:<10}{is_standard:<10}")
while loop:  # Loop the entire program
    while True:
        try:
            auto_nbr=int(input("Choose an automaton between 1 and " + str(Nombre_automata) + " (0 to exit): "))
            if 1 <= auto_nbr <= Nombre_automata:
                print(f"\n\n--- Automaton #{auto_nbr}")
                auto=automata[ auto_nbr-1 ]  # Retrieve the automaton from the list
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")
    if auto_nbr != 0:
        while True:  # Loop until the user input is valid
            #try:
            # Asks for the action wanted and calls the associated function
            user_input = int(input(" 1- Show the automaton specifications"
                                   "\n 2- Deterministic verification"
                                   "\n 3- Complete verification"
                                   "\n 4- Standard verification"
                                   "\n 5- Standardize automata"
                                   "\n 6- Complete an determinize automata"
                                   "\n 7- display graph"
                                   "\n 8- completion"
                                   "\n 9- determinization"
                                   "\nChoose an action:"))
            if 1 <= user_input <= 9:
                print(f"\n\n--- Automaton #{auto_nbr}")
                if user_input == 1:
                    auto.show_automaton()
                elif user_input == 2:
                    if auto.is_deterministic():
                        print("This automaton is deterministic")
                    else:
                        print("This automaton is not deterministic")
                elif user_input == 3:
                    if auto.is_complete():
                        print("This automaton is complete")
                    else:
                        print("This automaton is not complete")
                elif user_input == 4:
                    if auto.is_standard():
                        print("This automaton is standard")
                    else:
                        print("This automaton is not standard")
                elif user_input == 5:
                    auto.standardize()
                    print("The automaton has been standardized")
                elif user_input == 6:
                    auto.determinization_and_completion_of_automaton()
                    print("The automaton is now complete deterministic")
                elif user_input == 7:
                    print("if the node is both an initial state and a final state, its color is orange. "
                          "\nIf the node is only an initial state, its color is green. "
                          "\nIf the node is only a final state, its color is red. "
                          "\nOtherwise, its color is light blue.")
                    auto.display_automaton_graph()
                elif user_input == 8:
                    auto.completion()
                    print("The automaton is now complete")
                elif user_input == 9:
                    auto.determinize()
                    print("The automaton is now determinized")
                break
            else:
                print("Invalid input. Please enter a number between 1 and 44.")
            #except ValueError:
                #print("Invalid input. Please enter an integer.")
        input("Press ENTER to continue")
        print("\n\n\n")
