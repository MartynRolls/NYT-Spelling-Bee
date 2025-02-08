import pygame

# Initialising game
pygame.init()

# Defining Variables
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Window Title')

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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

    pygame.display.flip()
    clock.tick(60)
