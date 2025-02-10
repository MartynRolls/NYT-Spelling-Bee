from math import sin, cos, radians
import pygame


def create_word_list() -> list[str]:
    # words_alpha.txt contains every english word, each word being on its own line
    # The file was downloaded from 'https://github.com/dwyl/english-words/blob/master/words_alpha.txt'

    censored_words = []  # Words in this list will be removed from the valid entry of words

    with open('words_alpha.txt', 'r') as words_file:                                # Open the text file
        word_list = [word.strip() for word in words_file if len(word.strip()) > 3]  # Save words longer than 3 letters
        word_list = [word for word in word_list if word not in censored_words]      # Remove any censored words

        return word_list


VALID_WORDS = (create_word_list())

HEXAGON_RADIUS = 10
HEXAGON_SEPERATION = 1.5

hexagon_distance = HEXAGON_SEPERATION + HEXAGON_RADIUS * 2 * cos(radians(30))

start_positions = [(0, 0)]  # Seven hexagon positions. One in the center, and six more surrounding it
start_positions += [(round(hexagon_distance * sin(radians(60 * i)), 2),
                     round(hexagon_distance * cos(radians(60 * i)), 2))
                    for i in range(6)]


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

    def draw(self, window_size: tuple[int, int]) -> pygame.surface.Surface:

        surface = pygame.Surface(window_size, pygame.SRCALPHA)  # Create an empty surface

        scaler = min(window_size[0], window_size[1]) * 0.01  # Calculate how large it should be
        x_offset, y_offset = window_size[0] * 0.5, window_size[1] * 0.2  # Calculate its position on the screen

        font = pygame.font.Font('aptos-bold.ttf', int(7 * scaler))
        text = font.render(self.word.upper(), True, (0, 0, 0))
        rect = text.get_rect(center=(x_offset, y_offset))
        dest = (round(rect.topleft[0]), round(rect.topleft[1]))
        surface.blit(text, dest)

        return surface

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


class Tile:
    points = [(round(cos(radians(60 * i)), 2), round(sin(radians(60 * i)), 2))
              for i in range(6)]  # Six points of the hexagon

    colours = [(245, 220, 65), (230, 230, 230)]  # Colour for center and surrounding hexagons

    def __init__(self, letter: str, start_pos: tuple[int, int]):
        self.letter = letter

        self.x, self.y = start_pos
        self.dest_x, self.dest_y = start_pos

        self.size = HEXAGON_RADIUS
        self.animation_step = 0

        self.colour = self.colours[0] if start_pos == (0, 0) else self.colours[1]  # Yellow colour if in the center

    def draw(self, window_size: tuple[int, int]) -> pygame.Surface:
        surface = pygame.Surface(window_size, pygame.SRCALPHA)           # Create an empty surface

        scaler = min(window_size[0], window_size[1]) * 0.01              # Calculate how large it should be
        x_offset, y_offset = window_size[0] * 0.5, window_size[1] * 0.6  # Calculate its position on the screen

        hexagon_corners = [(int((self.x + self.size * x) * scaler + x_offset),
                            int((self.y + self.size * y) * scaler + y_offset))
                           for x, y in self.points]                      # Calculate all six points of the hexagon

        pygame.draw.polygon(surface, self.colour, hexagon_corners)       # Draw the hexagon onto the surface

        font = pygame.font.Font('aptos-bold.ttf', int(6 * scaler))  # Set up the font
        text = font.render(self.letter.upper(), True, (0, 0, 0))    # Write the letter
        rect = text.get_rect(center=(self.x * scaler + x_offset, self.y * scaler + y_offset))
        dest = (round(rect.topleft[0]), round(rect.topleft[1]))     # Calculate its destination
        surface.blit(text, dest)                                    # Draw it ontop of the hexagon

        if self.animation_step > 0:  # Update animation if running
            self.animation_step -= 1
            self.size = HEXAGON_RADIUS * (1 + 0.003 * self.animation_step * (self.animation_step - 15))

        return surface

    def check(self, window_size: tuple[int, int], mouse_position: tuple[int, int]) -> str:
        mouse_x, mouse_y = mouse_position
        window_x, window_y = window_size

        scaler = min(window_x, window_y) * 0.01              # Calculate how large the tile is
        x_offset, y_offset = window_x * 0.5, window_y * 0.6  # Calculate its position on the screen

        hexagon_corners = [(int((self.x + self.size * x) * scaler + x_offset),
                            int((self.y + self.size * y) * scaler + y_offset))
                           for x, y in self.points]  # Calculate all six points of the hexagon

        if (hexagon_corners[0][0] > mouse_x > hexagon_corners[3][0] and
                hexagon_corners[1][1] > mouse_y > hexagon_corners[4][1]):
            self.animation_step = 16
            return self.letter

        return '-'


class Score:
    def __init__(self):
        self.score = 0
        self.animation_step = 0

    def __add__(self, other):
        self.animation_step = other * 10
        return self

    def draw(self, window_size: tuple[int, int]) -> pygame.Surface:
        surface = pygame.Surface(window_size, pygame.SRCALPHA)           # Create an empty surface

        scaler = min(window_size[0], window_size[1]) * 0.01              # Calculate how large it should be
        x_offset, y_offset = window_size[0] * 0.5, window_size[1] * 0.1  # Calculate its position on the screen

        font = pygame.font.Font('aptos-bold.ttf', int(4 * scaler))
        text = font.render(str(self.score), True, (0, 0, 0))
        rect = text.get_rect(center=(x_offset, y_offset))
        dest = (round(rect.topleft[0]), round(rect.topleft[1]))
        surface.blit(text, dest)

        if self.animation_step > 0:  # Update animation if running
            self.animation_step -= 1
            if self.animation_step % 10 == 0:
                self.score += 1

        return surface


def create_tiles(letters: list[str]) -> dict[str, Tile]:  # Create a tile for all seven letters
    return {letters[i]: Tile(letters[i], start_positions[i]) for i in range(7)}
