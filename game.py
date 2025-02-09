def create_word_list() -> list[str]:
    # words_alpha.txt contains every english word, each word being on its own line
    # The file was downloaded from 'https://github.com/dwyl/english-words/blob/master/words_alpha.txt'

    censored_words = []  # Words in this list will be removed from the valid entry of words

    with open('words_alpha.txt', 'r') as words_file:                                # Open the text file
        word_list = [word.strip() for word in words_file if len(word.strip()) > 3]  # Save words longer than 3 letters
        word_list = [word for word in word_list if word not in censored_words]      # Remove any censored words

        return word_list


def score(word: str) -> int:
    if word in VALID_WORDS:                # If the word is valid
        if len(word) == 4:                 # If it's four letters long
            return 1                       # It's worth one point
        else:                              # Otherwise if it's longer:
            if len(list(set(word))) == 7:  # If it has seven unique letters it must have used all seven letters
                return len(word) + 7       # So it is worth seven extra points
            return len(word)               # Otherwise it's worth its own length

    return 0  # No points if the word is invalid


def generate_letters() -> list[str]:  # TODO: algorithim to generate letters for a game
    # Return static letters for testing
    # Return letters used on Feb 8th, 2025's puzzle by Sam Ezersky
    return ['l', 'h', 'n', 'r', 'a', 'c', 'i']


VALID_WORDS = (create_word_list())
