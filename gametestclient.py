import pygame
import random

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 10000               # Reserve a port for your service.

s.connect((host, port))
print (s.recv(1024))
player_id = int(s.recv(1024))
print(player_id)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Block(pygame.sprite.Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """

    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()


player = None
player_2 = None
# Create a RED player block

player = Block(RED, 20, 15)
player.rect.x = 0
player.rect.y = 0
player_2 = Block(GREEN, 20, 15)
player_2.rect.x = 650
player_2.rect.y = 350



all_sprites_list.add(player)
all_sprites_list.add(player_2)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
print(str(s.recv(1024)))
s.send(b'ok')

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_id == 1000:
                player.y_speed_speed = -5
                player.x_speed = 0
            elif event.key == pygame.K_DOWN and player_id == 1000:
                player.y_speed = 5
                player.x_speed = 0
            elif event.key == pygame.K_LEFT and player_id == 1000:
                player.x_speed = 5
                player.y_speed = 0
            elif event.key == pygame.K_RIGHT and player_id == 1000:
                player.x_speed = -5
                player.y_speed = 0

            if event.key == pygame.K_w and player_id == 1001:
                player_2.y_speed_speed = -5
                player_2.x_speed = 0
            elif event.key == pygame.K_s and player_id == 1001:
                player_2.y_speed = 5
                player_2.x_speed = 0
            elif event.key == pygame.K_a and player_id == 1001:
                player_2.x_speed = 5
                player_2.y_speed = 0
            elif event.key == pygame.K_d and player_id == 1001:
                player_2.x_speed = -5
                player_2.y_speed = 0

    # Clear the screen
    screen.fill(WHITE)

    player_2.rect.x = int(s.recv(1024))
    s.send(str(player.rect.x).encode())

    player_2.rect.y = int(s.recv(1024))
    s.send(str(player.rect.y).encode())

    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)

    # Check the list of collisions.
    for block in blocks_hit_list:
        score += 1
        print(score)

    # Draw all the spites
    all_sprites_list.draw(screen)
    player.rect.x += player.x_speed
    player.rect.y += player.y_speed
    player_2.rect.y += player_2.y_speed
    player_2.rect.x += player_2.x_speed

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
s.close  # Close the socket when done