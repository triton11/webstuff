import socket               # Import socket module
import pygame
import random

clients = []
num_players = 1000
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 10000                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
connected = False
s.listen(5)
c = None
while connected == False:
   c, addr = s.accept()     # Establish connection with client.

   print('Got connection from', addr)

   c.send(b'Thank you for connecting')
   c.send(str(num_players).encode())
   num_players += 1
   connected = True


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
        self.it = True

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0

# Initialize Pygame
player_id = 1001
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
tagged = pygame.sprite.Group()

player = None
player_2 = None
# Create a RED player block

player = Block(RED, 15, 15)
player.rect.x = 0
player.rect.y = 0

player_2 = Block(GREEN, 15, 15)
player_2.rect.x = 685
player_2.rect.y = 385

power = Block(BLACK, 10, 10)
power.rect.x = 335
power.rect.y = 185

block_list.add(power)
all_sprites_list.add(power)
all_sprites_list.add(player)
all_sprites_list.add(player_2)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

it = 0

c.send(b'start')
c.recv(1024)
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and player_id == 1001:
                player_2.y_speed = -5
                player_2.x_speed = 0
            elif event.key == pygame.K_s and player_id == 1001:
                player_2.y_speed = 5
                player_2.x_speed = 0
            elif event.key == pygame.K_a and player_id == 1001:
                player_2.x_speed = -5
                player_2.y_speed = 0
            elif event.key == pygame.K_d and player_id == 1001:
                player_2.x_speed = 5
                player_2.y_speed = 0

    # Clear the screen
    screen.fill(WHITE)

    c.send(str(player_2.rect.x).encode())
    player.rect.x = int(c.recv(1024))

    c.send(str(player_2.rect.y).encode())
    player.rect.y = int(c.recv(1024))
    
    c.send(str(it).encode())
    check = c.recv(1024)

    c.send(str(power.rect.x).encode())
    check = c.recv(1024)

    c.send(str(power.rect.y).encode())
    check = c.recv(1024)

    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)

    # Check the list of collisions.
    for block in blocks_hit_list:
        save_x = player.rect.x
        save_y = player.rect.y
        save_2x = player_2.rect.x
        save_2y = player_2.rect.y
        save_vx = player_2.x_speed
        save_yx = player_2.y_speed

        player = Block(BLACK, 15, 15)
        player.rect.x = save_x
        player.rect.y = save_y
	
        player_2 = Block(GREEN, 15, 15)
        player_2.rect.x = save_2x
        player_2.rect.y = save_2y
        player_2.x_speed = save_vx
        player_2.y_speed = save_yx

        it = 1
        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(player)
        all_sprites_list.add(player_2)
        all_sprites_list.add(power)
        power.rect.x = random.randrange(0,690)
        power.rect.y = random.randrange(0,390)
      
        	
    blocks_hit_list = pygame.sprite.spritecollide(player_2, block_list, False)

    # Check the list of collisions.
    for block in blocks_hit_list:
        save_x = player.rect.x
        save_y = player.rect.y
        save_2x = player_2.rect.x
        save_2y = player_2.rect.y
        save_vx = player_2.x_speed
        save_yx = player_2.y_speed

        player_2 = Block(BLACK, 15, 15)
        player.rect.x = save_x
        player.rect.y = save_y

        player = Block(RED, 15, 15)
        player_2.rect.x = save_2x
        player_2.rect.y = save_2y
        player_2.x_speed = save_vx
        player_2.y_speed = save_yx

        it = 2
        all_sprites_list = pygame.sprite.Group()
 
        all_sprites_list.add(player)
        all_sprites_list.add(player_2)
        all_sprites_list.add(power)
        power.rect.x = random.randrange(0,690)
        power.rect.y = random.randrange(0,390)
    

    if it == 1:
        tagged = pygame.sprite.Group()
        tagged.add(player_2)
    
    if it == 2:
        tagged = pygame.sprite.Group()
        tagged.add(player)

    if it == 1:
        tagged_list = pygame.sprite.spritecollide(player, tagged, False)
        for i in tagged_list:
            print("player 1 wins")
            done = True
    if it == 2:
        tagged_list = pygame.sprite.spritecollide(player_2, tagged, False)
        for i in tagged_list:
            print("player 2 wins")
            done = True
    
    if player.rect.x < 0 or player.rect.x > 685 or player.rect.y < 0 or player.rect.y > 385:
        print("player 2 wins")
        done = True

    if player_2.rect.x < 0 or player_2.rect.x > 685 or player_2.rect.y < 0 or player_2.rect.y > 385:
        print("player 1 wins")
        done = True
    
    # Draw all the spites
    all_sprites_list.draw(screen)
   
    player_2.rect.y += player_2.y_speed
    player_2.rect.x += player_2.x_speed

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()



c.close()
