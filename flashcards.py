def create_new_flashcard(card_number: int, cards_dict: dict, save_to_file: bool):

    term, definition = check_inputs_correctness(card_number, cards_dict)

    if save_to_file:
        with open('flashcards.txt', 'a') as file:
            file.write(f'{card_number}{term},{definition}\n')
    else:

        cards_dict[term] = definition
        return cards_dict
    return None

def check_inputs_correctness(card_number: int, cards_dict: dict) -> tuple[str, str]:
    term_not_correct = True
    term = input(f'The term for card #{card_number}:\n')

    while term_not_correct:
        if term in cards_dict.keys():
            term = input(f'The term "{term}" already exists. Try again:\n')
        else:
            term_not_correct = False

    definition_not_correct = True
    definition = input(f'The definition for card #{card_number}:\n')

    while definition_not_correct:
        if definition in cards_dict.values():
            definition = input(f'The definition "{definition}" already exists. Try again:\n')
        else:
            definition_not_correct = False

    return term, definition

def ask_for_card(card_dict: dict, key):
    reversed_cards = {value: key for key, value in card_dict.items()}

    definition = card_dict.get(key)

    print(f'Print the definition of "{key}":')
    user_definition = input()

    if definition == user_definition:
        output = 'Correct!'
    else:
        indication = f', but your definition is correct for "{reversed_cards[user_definition]}"' if (user_definition in reversed_cards) else ''
        output = f'Wrong. The right answer is "{definition}"{indication}.'

    print(output)

def check_knowledge(card_dict: dict):
    for key in card_dict.keys():
        ask_for_card(card_dict, key)


def main():
    flashcards = dict()
    num_of_flashcards = int(input('Input the number of cards:\n'))

    for i in range(1, num_of_flashcards + 1):
        flashcards = create_new_flashcard(i, flashcards, False)
    check_knowledge(flashcards)



if __name__ == '__main__':
    main()
