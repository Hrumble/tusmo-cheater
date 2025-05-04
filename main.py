import unicodedata
from collections import Counter

# After these lines, the words become obsolete
# FR dict = 166080
# English_UK dict = 107150
# English dict = 466550 (no limit really)
LINE_TO_STOP = 466550
MAX_SHOWN_SUGGESTIONS = 5
DIC_PATH = "./dictionaries/English.txt"


def start():
    word_dic = load_dic(DIC_PATH)
    while True:
        display_separator()
        initial_letter = input("Enter initial letter: ").upper()
        while True:
            try:
                word_length = input("Enter word length: ")
                word_length = int(word_length)
                break
            except ValueError:
                print("PLEASE enter a valid length")

        main_loop(word_dic, initial_letter, word_length)


def main_loop(word_dic, initial_letter, word_length):
    word_found = False
    # Gets only the words that start with initial_letter and are the correct length
    word_dic = [
        word for word in word_dic
        if word[0] == initial_letter and len(word) == word_length
    ]
    # The suggestions are sorted based on repetition count
    suggestions = sorted([
        count_repetitions(word) for word in word_dic
    ], key=lambda x: x[1])
    display_suggestions(suggestions[:MAX_SHOWN_SUGGESTIONS])

    while not word_found:
        print("📝 Did we find out the position of any fixed letters?")
        fixed_letters_input = input("Format 'a--o---d': ").strip()
        print("📝 Did we find out if any letters are existant but misplaced?")
        misplaced_letters_input = input("Format '-o---a': ").strip()
        print("📝 Did we find out if any letters are excluded?")
        excluded_letters_input = input("Format 'abcd': ").strip()

        display_separator()
        print("🤔 Processing")
        display_separator()

        # Handles input formatting
        try:
            fixed_letters = {
                position: letter.upper() for (position, letter) in enumerate(fixed_letters_input)
                if letter != "-"
            }

            misplaced_letters = {
                position: letter.upper() for (position, letter) in enumerate(misplaced_letters_input)
                if letter != "-"
            }

            excluded_letters = list(excluded_letters_input.upper())
            print(f"User Input:\nfixed: {fixed_letters}\nmisplaced: {
                  misplaced_letters}\nexcluded: {excluded_letters}")
        except Exception as e:
            print(e)
            print("❌ Could not parse your input, try again...")
            break

        word_dic = [
            word for word in word_dic
            if matches_criterias(word, fixed_letters, misplaced_letters, excluded_letters)
        ]

        suggestions = sorted([
            count_repetitions(word) for word in word_dic
        ], key=lambda x: x[1])
        display_suggestions(suggestions[:MAX_SHOWN_SUGGESTIONS])
        print("👋Did we find the word yet?")
        u = input("y/n: ").upper()
        if u == 'Y' or u == 'YES':
            word_found = True

    display_separator()
    print("🥳 Let's keep cheating!")


def matches_criterias(word, fixed_letters, misplaced_letters, excluded_letters):
    does_word_match = True
    for letter_position, word_letter in enumerate(word):

        # Verifies that it correctly has the fixed letters
        if word_letter != fixed_letters.get(letter_position, word_letter):
            does_word_match = False
            break

        # if the letter is misplaced, and at the same position
        if word_letter == misplaced_letters.get(letter_position):
            does_word_match = False
            break

        # If the word contains excluded letters that are not
        # 1. In the fixed letters
        # 2. In the misplaced letters
        # it does not match
        if word_letter in excluded_letters:
            if not (word_letter in fixed_letters.values() or word_letter in misplaced_letters.values()):
                does_word_match = False
                break

    # Makes sure the word contains all misplaced letters
    if not all(letter in word for letter in misplaced_letters.values()):
        does_word_match = False

    return does_word_match


def display_suggestions(suggestions):
    display_separator()
    print("⭐ Suggestions")
    for s in suggestions:
        print(s[2])
    print("...")
    display_separator()


def display_separator():
    print("==============================")


def count_repetitions(word):
    c = Counter(word)

    return c, sum(1 for count in c.values() if count > 1), word


def load_dic(file_path):
    word_list = []
    try:
        with open(file_path, 'r', encoding='latin1') as file:
            for line_num, word in enumerate(file, start=1):
                if line_num > LINE_TO_STOP:
                    break
                if word:
                    # removes any accents if any
                    if "+" in word:
                        # the dic file creates separations with "+++++++", don't include those
                        continue
                        #remove words that have an amperstand as they are not accepted in tusmo
                    if "\'" in word:
                        continue
                    word = word.strip()
                    word = remove_accents(word)
                    word_list.append(word.upper())
        print("Sucessfully parsed dictionary")
        return word_list
    except Exception as e:
        print(f"Failed to parse the file: {e}")
        exit(1)


def remove_accents(word):
    nfkd_form = unicodedata.normalize('NFD', word)

    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


start()
