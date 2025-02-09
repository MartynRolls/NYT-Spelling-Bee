from math import sin, cos, radians
import pygame

HEXAGON_RADIUS = 10
HEXAGON_SEPERATION = 1.5

hexagon_distance = HEXAGON_SEPERATION + HEXAGON_RADIUS * 2 * cos(radians(30))

start_positions = [(0, 0)]  # Seven hexagon positions. One in the center, and six more surrounding it
start_positions += [(round(hexagon_distance * sin(radians(60 * i)), 2),
                     round(hexagon_distance * cos(radians(60 * i)), 2))
                    for i in range(6)]


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
                           for x, y in self.points]  # Calculate all six points of the hexagon

        pygame.draw.polygon(surface, self.colour, hexagon_corners)        # Draw the hexagon onto the surface

        if self.animation_step > 0:
            self.size = HEXAGON_RADIUS * (1 + 0.003 * self.animation_step * (self.animation_step - 15))
            self.animation_step += 1
            if self.animation_step == 16:
                self.animation_step = 0

        # TODO: write letter on tile

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
            self.animation_step = 1
            return self.letter

        return '-'


def create_tiles(letters: list[str]) -> dict[str, Tile]:  # Create a tile for all seven letters
    return {letters[i]: Tile(letters[i], start_positions[i]) for i in range(7)}
