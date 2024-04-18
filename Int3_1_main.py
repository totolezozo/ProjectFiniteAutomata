from Int3_1_automaton import Automaton


loop = True
while loop:  # Loop the entire program
    while True:  # Loop until the user input is valid
        try:
            # Asks for the automaton wanted and calls the function to create it from the text file
            auto_nbr = int(input("Choose an automaton between 1 and 44 (0 to exit): "))
            if 1 <= auto_nbr <= 44:
                print(f"\n\n--- Automaton #{auto_nbr}")
                auto = Automaton()
                auto.get_automaton_from_txt(f"test_automata/Int3-1-{auto_nbr}.txt")
                break  # Exit the loop if valid input
            elif auto_nbr == 0:  # Exit teh program
                loop = False
                break
            else:
                print("Invalid input. Please enter a number between 1 and 44.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
    if auto_nbr != 0:
        while True:  # Loop until the user input is valid
            try:
                # Asks for the action wanted and calls the associated function
                user_input = int(input(" 1- Show the automaton specifications\n 2- Deterministic verification\n 3- Complete verification\n 4- Standard verification\nChoose an action:"))
                if 1 <= user_input <= 4:
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
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 44.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        input("Press ENTER to continue")
        print("\n\n\n")
