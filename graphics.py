from math import sin, cos, radians
import pygame
from pygame import gfxdraw

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

        draw_positions = [(int((self.x + self.size * x) * scaler + x_offset),
                           int((self.y + self.size * y) * scaler + y_offset))
                          for x, y in self.points]                       # Calculate all six points of the hexagon

        pygame.draw.polygon(surface, self.colour, draw_positions)        # Draw the hexagon onto the surface

        # TODO: write letter on tile

        return surface


def create_tiles(letters: list[str]) -> list[Tile]:  # Create a tile for all seven letters
    return [Tile(letters[i], start_positions[i]) for i in range(7)]
