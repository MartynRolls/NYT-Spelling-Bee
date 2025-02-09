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

word = game.Word()
score = 0

tiles: dict = graphics.create_tiles(word.generate_letters())
for _, tile in tiles.items():
    tile.check((500, 500), (0, 0))

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                score += word.score()
            if event.key == pygame.K_BACKSPACE:
                word -= '_'
            for key, tile in tiles.items():
                if event.key == getattr(pygame, f'K_{key}'):
                    word += key
                    tile.animation_step = 1

        # For checking if a mouse button has been pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                for _, tile in tiles.items():
                    word += tile.check(window_size, mouse_position)

    screen.fill((255, 255, 255))   # Clear the screen
    for _, tile in tiles.items():  # Draw all letter tiles
        screen.blit(tile.draw(window_size), (0, 0))
    screen.blit(graphics.write_word(window_size, word.word), (0, 0))  # Write the word

    print(score, word)  # Print the word and score for debug

    pygame.display.flip()
    clock.tick(60)
