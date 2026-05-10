from dictionary import load_dictionary, save_dictionary
from numerals import parse_numerals, view_numerals
from dictionary import add_new_entries, open_dictionary
from sentence_approx import sentence_approximation
from morphology import parse_lexical

def display_menu():
    print("\n=== Etruscan Concordance Dictionary v0.0.7 ===")
    print("1. Add new entries")
    print("2. Open dictionary")
    print("3. View numerals")
    print("4. Parse")
    print("5. Exit")

def parse_menu():
    print("\n[Parse]")
    print("1. Parse numerals")
    print("2. Parse lexical")
    print("3. Sentence Approximation")
    print("4. Back")

def main():
    dictionary = load_dictionary()
    print("Dictionary loaded successfully.")

    while True:
        display_menu()
        choice = input("Select an option (1–5): ").strip()
        if choice == "1":
            add_new_entries(dictionary)
        elif choice == "2":
            open_dictionary(dictionary)
        elif choice == "3":
            view_numerals(dictionary)
        elif choice == "4":
            while True:
                parse_menu()
                sub = input("Select option: ").strip()
                if sub == "1":
                    parse_numerals()
                elif sub == "2":
                    parse_lexical()
                elif sub == "3":
                    sentence_approximation()
                elif sub == "4":
                    break
        elif choice == "5":
            print("Exiting program")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
