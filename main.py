import pygame
import game
import graphics

# Initialising game
pygame.init()

# Defining Variables
window_size = 500, 500
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption('NYT Spelling Bee')

tiles = graphics.create_tiles(game.generate_letters())

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.WINDOWRESIZED:
            window_size = screen.get_size()

        # For checking if a key has been pressed
        # if event.type == pygame.KEYDOWN:
        #     if keys[pygame.K_{key}]:

        # For checking if a mouse button has been pressed
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     mouse_x, mouse_y = pygame.mouse.get_pos()
        #     if pygame.mouse.get_pressed()[{0 = left, 1 = middle, 2 = right}]:

    # For checking if a key is being held down
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_{key}]:

    screen.fill((255, 255, 255))  # Clear the screen
    for tile in tiles:            # Draw all letter tiles
        screen.blit(tile.draw(window_size), (0, 0))

    pygame.display.flip()
    clock.tick(60)
