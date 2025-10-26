import glob
import os
import random
import io
from collections import defaultdict


def input_and_save(log_output, string):
    log_output.write(string)
    inserted_string = input(string)
    log_output.write(f'{inserted_string}\n')
    return inserted_string


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
        self.cards_stats = {}

    def add_card(self, log_output=None):
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
        self.cards_stats[term] = 0
        print(f'The pair ("{term}":"{definition}") has been added.')

    def check_add_input_correctness(self, log_output=None):
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

    def remove_card(self, log_output=None):
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
            self.cards_tally.pop(card_term, None)
            print(f'The card has been removed.')
        else:
            print(f'Can\'t remove "{card_term}": there is no such card.')

    def ask_for_cards(self, log_output=None):
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
                self.ask_for_single_card(term, log_output)
        except ValueError:
            return False

    def ask_for_single_card(self, key, log_output=None):
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
            self.cards_stats[key] += 1
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
                file.write(f'{term},{definition},{self.cards_stats.get(term)}\n')

    def import_data(self, filename: str, log_output=None):
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
        temp_mistakes_stats = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                temp_term, temp_definition, mistakes = line.split(',')
                temp_cards[temp_term] = temp_definition
                temp_mistakes_stats[temp_term] = int(mistakes)

        self.cards_tally = {**self.cards_tally, **temp_cards}

        # TODO - Check whether values should be summed - now they are overwritten
        self.cards_stats = {**self.cards_stats, **temp_mistakes_stats}

        print(f'{len(temp_cards)} cards have been loaded.')

    def reset_stats(self, log_output=None):
        self.cards_stats = dict.fromkeys(self.cards_stats, 0)
        print('Card statistics have been reset.')

    def get_hardest_card(self, log_output=None):

        result = self.check_misses_rating()

        if not result:
            return 'There are no cards with errors.'

        mistakes, cards = result

        if len(cards) == 1:
            return f'The hardest card is "{cards[0]}". You have {mistakes} errors answering it.'
        else:
            cards_to_string = f'{"\", \"".join(cards)}'
            return f'The hardest card are "{cards_to_string}". You have {mistakes} errors answering it.'

    def check_misses_rating(self):
        temp_misses_stats = defaultdict(list)
        for term, misses in self.cards_stats.items():
            temp_misses_stats[misses].append(term)

        key = sorted(temp_misses_stats, reverse=True)[0] if temp_misses_stats else None

        if key is None or key == 0:
            return None
        return key, temp_misses_stats[key]

    def log_data(self, log_output=None):
        print('File name:', file=log_output)
        file_name = input()

        with open(file_name, 'a') as file:
            file.write(log_output.getvalue())

        print('The log has been saved.', file=log_output)



class FlashcardsMenu:
    MAIN_MESSAGE = 'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n'
    EXIT = 'exit'

    def __init__(self):
        self.flashcards_tally = FlashcardsTally()
        self.menu_options = {
            'add': self.flashcards_tally.add_card,
            'remove': self.flashcards_tally.remove_card,
            'ask': self.flashcards_tally.ask_for_cards,
            'export': self.export_to_file,
            'import': self.import_from_file,
            'reset stats': self.flashcards_tally.reset_stats,
            'hardest card': self.hardest_card_stats,
            'log': self.flashcards_tally.log_data,
        }
        self.logs = io.StringIO()
        self.get_str = FileUtils

    def default_fn(self):
        print("incorrect input, please try again.")

    def run_interface(self):
        # self.logs.write(self.MAIN_MESSAGE)
        # user_choice = input(self.MAIN_MESSAGE)
        user_choice = input_and_save(self.logs, self.MAIN_MESSAGE)

        while user_choice != self.EXIT:
            self.menu_options.get(user_choice, self.default_fn)(self.logs)
            print()
            user_choice = input_and_save(self.logs, self.MAIN_MESSAGE)

        print('Bye bye!')

    def export_to_file(self, log_output=None):
        filename = input('Filename:\n')

        self.flashcards_tally.export_data(filename)

        print(f'{len(self.flashcards_tally.cards_tally)} cards have been saved.')

    def import_from_file(self, log_output=None):
        filename = input('Filename:\n')

        check_file_exists = FileUtils(filename).check_file_exists()

        if check_file_exists:
            self.flashcards_tally.import_data(filename)
        else:
            print('File not found.')

    def hardest_card_stats(self, log_output=None):
        print(self.flashcards_tally.get_hardest_card(log_output))





def main():
    flashcards_menu = FlashcardsMenu()
    flashcards_menu.run_interface()


if __name__ == '__main__':
    main()

