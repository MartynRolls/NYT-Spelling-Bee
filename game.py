def create_word_list() -> list[str]:
    # words_alpha.txt contains every english word, each word being on its own line
    # The file was downloaded from 'https://github.com/dwyl/english-words/blob/master/words_alpha.txt'

    censored_words = []  # Words in this list will be removed from the valid entry of words

    with open('words_alpha.txt', 'r') as words_file:                                # Open the text file
        word_list = [word.strip() for word in words_file if len(word.strip()) > 3]  # Save words longer than 3 letters
        word_list = [word for word in word_list if word not in censored_words]      # Remove any censored words

        return word_list


VALID_WORDS = (create_word_list())


class Word:
    def __init__(self):
        self.word = ''
        self.letters = []
        self.used_words = []

    def __add__(self, other: str):
        if other in self.letters:  # If the letter is in the current set
            self.word += other     # Add it to the word
        return self

    def __sub__(self, other):
        self.word = self.word[:-1]  # Set the word to one character shorter than what it is
        return self

    def __str__(self):
        return self.word

    def score(self) -> int:
        score = 0
        if (self.word in VALID_WORDS                  # If the word is actually a word,
                and self.word not in self.used_words  # Hasn't been used,
                and self.letters[0] in self.word):    # And contains the center letter:
            self.used_words.append(self.word)         # Note the word
            if len(self.word) == 4:                   # If it's four letters long
                score = 1                             # It's worth one point
            else:                                     # Otherwise if it's longer:
                score = len(self.word)                # It's worth its own length
                if len(list(set(self.word))) == 7:    # And if it has seven unique letters it's used all seven letters
                    score += 7                        # So it's worth seven extra points

        self.word = ''  # Clear the word
        return score    # And return the score

    def generate_letters(self) -> list[str]:
        # Return static letters for testing. TODO: algorithim to generate letters for a game
        # Return letters used on Feb 8th, 2025's puzzle by Sam Ezersky
        letters = ['l', 'h', 'n', 'r', 'a', 'c', 'i']

        self.letters = letters
        return letters
