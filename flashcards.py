import glob
import os
import random

class FileUtils:
    def __init__(self, path):
        self.path = path

    def add_filename_returns(self):
        self.path = os.path.join(self.path, "*.txt")
        self.path = glob.escape(self.path)

    def check_file_exists(self):
        result = glob.glob(self.path)
        if not result:
            self.add_filename_returns()
        return glob.glob(self.path)


class FlashcardsTally:
    def __init__(self):
        self.cards_tally = {}

    def add_card(self):
        """
        add — create a new flashcard with a unique term and definition.
        After adding the card, output the message The pair ("term":"definition") has been added,
        where "term" is the term entered by the user and "definition" is the definition entered by the user.
        If a term or a definition already exists, output the line
        "The <term/definition> already exists. Try again:"
        and accept a new term or definition.

        :return: None
        """
        term, definition = self.check_add_input_correctness()
        self.cards_tally[term] = definition
        print(f'The pair ("{term}":"{definition}") has been added.')

    def check_add_input_correctness(self):
        term_not_correct = True
        term = input(f'The card:\n')

        while term_not_correct:
            if term in self.cards_tally.keys():
                term = input(f'The term "{term}" already exists. Try again:\n')
            else:
                term_not_correct = False

        definition_not_correct = True
        definition = input(f'The definition of the card:\n')

        while definition_not_correct:
            if definition in self.cards_tally.values():
                definition = input(f'The definition "{definition}" already exists. Try again:\n')
            else:
                definition_not_correct = False

        return term, definition

    def remove_card(self):
        """
        remove — ask the user for the term of the card they want to remove
        with the message Which card?, and read the user's input from the next line.
        If a matching flashcard exists, remove it from the set and output the message
        "The card has been removed."
        If there is no such flashcard in the set, output the message
        "Can't remove "card": there is no such card.",
        where "card" is the user's input.
        :return:
        """
        card_term = input(f'Which card?:\n')

        if self.cards_tally.pop(card_term, None):
            print(f'The card has been removed.')
        else:
            print(f'Can\'t remove "{card_term}": there is no such card.')

    def ask_for_cards(self):
        """
        ask — ask the user about the number of cards they want and then prompt them for definitions.
        When the user enters the wrong definition for the requested term,
        but this definition is correct for another term, print the appropriate message:
        'Wrong. The right answer is "correct answer", but your definition is correct for "term for user's answer".',
        where "correct answer" is the actual definition for the requested term,
        and "term for user's answer" is the appropriate term for the user-entered definition.

        :return: None
        """
        asks_number = input('How many times to ask?\n')
        try:
            asks_number = int(asks_number)
            keys_to_check = tuple(self.cards_tally.keys())

            for _ in range(asks_number):
                term = random.choice(keys_to_check)
                self.ask_for_single_card(term)
        except ValueError:
            return False

    def ask_for_single_card(self, key):
        """
        Checks if the user's answer is correct.
        If not, it additionally checks whether the same description is associated with the other card.
        If so, the user is informed about it.
        Additionally correct answer is also displayed. 
        :param key: key of term in cards_tally.
        :return:
        """
        reversed_cards = {value: key for key, value in self.cards_tally.items()}

        definition = self.cards_tally.get(key)

        print(f'Print the definition of "{key}":')
        user_definition = input()

        if definition == user_definition:
            output = 'Correct!'
        else:
            indication = f', but your definition is correct for "{reversed_cards[user_definition]}"' if (
                        user_definition in reversed_cards) else ''
            output = f'Wrong. The right answer is "{definition}"{indication}.'

        print(output)

    def export_data(self, filename):
        """
        export — request the file name with the line "File name:"
        and write all currently available flashcards into this file.
        Print the message "n cards have been saved.",
        where n is the number of cards exported to the file.

        :param filename: path of the file to export
        :return: None
        """
        with open(filename, 'w') as file:
            for term, definition in self.cards_tally.items():
                file.write(f'{term},{definition}\n')

    def import_data(self, filename: str):
        """
        import — print the line "File name:", read the user's input from the next line,
        which is the file name, and import all the flashcards written to this file.
        If there is no file with such name, print the message: "File not found."
        After importing the cards, print the message "n cards have been loaded.",
        where n is the number of cards in the file.
        The imported cards should be added to the ones that already exist in the memory of the program.
        However, the imported cards have priority:
        if you import a card with the name that already exists in the memory,
        the card from the file should overwrite the one in memory.

        :param filename: name of the file to import
        :return: None
        """
        temp_cards = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                temp_term, temp_definition = line.split(',')
                temp_cards[temp_term] = temp_definition

        self.cards_tally = {**self.cards_tally, **temp_cards}

        print(f'{len(temp_cards)} cards have been loaded.')



class FlashcardsMenu:
    MAIN_MESSAGE = 'Input the action (add, remove, import, export, ask, exit):\n'
    EXIT = 'exit'

    def __init__(self):
        self.flashcards_tally = FlashcardsTally()
        self.menu_options = {
            'add': self.flashcards_tally.add_card,
            'remove': self.flashcards_tally.remove_card,
            'ask': self.flashcards_tally.ask_for_cards,
            'export': self.export_to_file,
            'import': self.import_from_file,
        }

    def default_fn(self):
        print("incorrect input, please try again.")

    def run_interface(self):
        user_choice = input(self.MAIN_MESSAGE)
        while user_choice != self.EXIT:
            self.menu_options.get(user_choice, self.default_fn)()
            print()
            user_choice = input(self.MAIN_MESSAGE)

        print('Bye bye!')

    def export_to_file(self):
        filename = input('Filename:\n')

        self.flashcards_tally.export_data(filename)

        print(f'{len(self.flashcards_tally.cards_tally)} cards have been saved.')

    def import_from_file(self):
        filename = input('Filename:\n')

        check_file_exists = FileUtils(filename).check_file_exists()

        if check_file_exists:
            self.flashcards_tally.import_data(filename)
        else:
            print('File not found.')


def main():
    flashcards_menu = FlashcardsMenu()
    flashcards_menu.run_interface()


if __name__ == '__main__':
    main()
