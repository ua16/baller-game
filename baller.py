#!/usr/bin/env python3

import pygame , sys , random
import math
import font_parser

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption("baller")

WINDOW_SIZE = (1280,720)
DISPLAY_SIZE = (512,288)

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # The ac

display = pygame.Surface(DISPLAY_SIZE) # Where we blit our pixel art to

special = pygame.Surface(DISPLAY_SIZE) # For special effects


# Load Images

title_imgs = [
    pygame.image.load("data/img/title_img/0.png").convert()
]

for i in title_imgs:
    i.set_colorkey((0,0,0))


# Load fonts

big_text = font_parser.Font("large_font.png", "#FFFFFF")

# Load sounds
blip_sound = pygame.mixer.Sound('data/sfx/blip.wav')
score_sound = pygame.mixer.Sound('data/sfx/score.wav')
lose_sound = pygame.mixer.Sound('data/sfx/lose.wav')

# Our circle class
# A circle has a centre positiong and a radius

class Circle:
    def __init__(self, radius, x, y, velocity):
        self.radius = radius
        self.x = x
        self.y = y
        self.velocity = velocity # A tuple with x , y velocity

# Splash class
# For effects
class Splash:
    def __init__(self,x,y):
        self.radius = 1
        self.x = x
        self.y = y

# Collision Functions

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )

def is_circle_colliding(radius1, x1, y1, radius2, x2, y2):
    if (radius1 + radius2) > distance_between_points(x1, y1, x2, y2):
        return True
    return False


# Play Areas

def main_menu():
    running = True

    click = False

    mx, my = 0,0


    # Main Loop
    while running:
        # Display stuff
        display.fill("#101018")

        display.blit(title_imgs[0], (0,0))


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == KEYDOWN:
                game()

        
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

def lose(score):
    running = True
    click = False

    frame_count = 0

    while running:
        big_text.render(display, str(score), (DISPLAY_SIZE[0]//2 - (len(str(score)) * big_text.space_width), DISPLAY_SIZE[1]//2 - 60 ))
        big_text.render(display, "Game Over", (DISPLAY_SIZE[0]//2 - 5*big_text.space_width , DISPLAY_SIZE[1]//2))
        big_text.render(display, "Press Any Key To Continue", (4, DISPLAY_SIZE[1] -18))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and frame_count > 30:
                running = False


        frame_count += 1


        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)

    return False

def game():
    running = True
    click = False

    frame_count = 0
    time_s = 0

    player_radius = 17
    player_cords = {"x": (DISPLAY_SIZE[0]//2), "y": (DISPLAY_SIZE[1]//2)}
    player_colour = "#F0CA28"
    player_velocity = [0,0]

    deceleration = 0.25
    acceleration = 0.5
    terminal_velocity = 1

    # Track Key Presses
    input_keys = {
        K_UP: False, K_DOWN : False, K_RIGHT : False, K_LEFT: False,
        K_w : False, K_s : False, K_d : False, K_a : False
                  }

    circles = [] # A list of circles

    max_circles = 0

    score = 0

    # Effects

    offset = 0
    offset_reverse = 1

    splashes = []
    
    while running:
        # Display stuff
        display.fill("#101018")

        # Put the game mechanic logic here

        max_circles = (1 + time_s)%20
        if time_s > 20:
            time_s = 0


        # Generate new random circles at the edges

        if len(circles) < max_circles:
            rand_radius = random.randint(3,18)
            rand_x = random.choice([0,DISPLAY_SIZE[0]])
            rand_y = random.choice([0,DISPLAY_SIZE[1]])
            rand_vel = [0,0]

            if rand_x == 0:
                rand_x += random.randint(8,32)
                rand_vel[0] = random.randint(1,3)
            else:
                rand_x -= random.randint(8,32)
                rand_vel[0] = random.randint(1,3) * -1

            if rand_y == 0:
                rand_y += random.randint(8,DISPLAY_SIZE[1]//2)
                rand_vel[1] = random.randint(1,3)
            else:
                rand_y -= random.randint(8,DISPLAY_SIZE[1]//2)
                rand_vel[1] = random.randint(1,3) * -1

            circles.append(Circle(rand_radius, rand_x, rand_y, (rand_vel[0], rand_vel[1])))
            blip_sound.play()

            # Add a splash as well
            splashes.append(Splash(rand_x, rand_y))

        # Remove the circles
        i = 0
        while i < len(circles):
            if circles[i].x > DISPLAY_SIZE[0] + 64 or circles[i].x < -64:
                del circles[i]
                score += 100
                score_sound.play()
            elif circles[i].y > DISPLAY_SIZE[1] + 64 or circles[i].y < -64:
                del circles[i]
                score += 100
                score_sound.play()
            else:
                i += 1


        # Remove the splashes
        i = 0
        while i < len(splashes):
            if splashes[i].radius > 74:
                del splashes[i]
            else:
                i += 1
                        

        # CPU Effects

        # Render Lines
        
        if offset < -60:
            offset_reverse = 1
        if offset > 60:
            offset_reverse = -1

        offset += 0.25 * offset_reverse
        
        for i in range(-11, 11):
            pygame.draw.line(
                display,
                "#434364",
                (0,DISPLAY_SIZE[1] + i *32 + offset),
                (DISPLAY_SIZE[0], i*32 + offset),
                width=4
            )

        # Render splashes

        for splash in splashes:
            splash.radius += 1
            splash_width = 8 - (splash.radius//10)
            pygame.draw.circle(display, "#FFFFFF", (splash.x, splash.y), splash.radius, width=8-(splash.radius//10))
        

        # Draw stuff Top layer

        pygame.draw.circle(display, player_colour, (player_cords["x"], player_cords["y"]), player_radius)

        for circle in circles:
            pygame.draw.circle(display, "#FD1e21",(circle.x, circle.y), circle.radius)

        # Score
        big_text.render(display, str(score), (3,4))


        # Collisions And Lose ------------------------- #

        for circle in circles:
            if is_circle_colliding(player_radius, player_cords["x"] , player_cords["y"], circle.radius, circle.x, circle.y):
                lose_sound.play()
                running = lose(score)# End the game or something This can wait till the end


        # Circle Movement

        for circle in circles:
            circle.x += circle.velocity[0]
            circle.y += circle.velocity[1]


        # Dealing with input from previous frame
        # Implement a smoother one later
        # Implemented much smoother movement
        if input_keys[K_UP] or input_keys[K_w]:
            player_velocity[1] -= acceleration

        if input_keys[K_DOWN] or input_keys[K_s]:
            player_velocity[1] += acceleration
            
        if input_keys[K_RIGHT] or input_keys[K_d]:
            player_velocity[0] += acceleration

        if input_keys[K_LEFT] or input_keys[K_a]:
            player_velocity[0] -= acceleration

        for velocity in player_velocity:
            if velocity > terminal_velocity:
                velocity = terminal_velocity
            if velocity < terminal_velocity * -1:
                velocity = terminal_velocity *-1

        player_cords['x'] += player_velocity[0]
        player_cords['y'] += player_velocity[1]
        
        # Deceleration
        if not (input_keys[K_UP] or input_keys[K_w] or input_keys[K_DOWN] or input_keys[K_s]):
            if player_velocity[0] != 0:
                if player_velocity[0] > 0:
                    player_velocity[0] -= deceleration
                if player_velocity[0] < 0:
                    player_velocity[0] += deceleration
        if not (input_keys[K_RIGHT] or input_keys[K_d] or input_keys[K_LEFT] or input_keys[K_a]):
            if player_velocity[1] != 0:
                if player_velocity[1] > 0:
                    player_velocity[1] -= deceleration
                if player_velocity[1] < 0:
                    player_velocity[1] += deceleration

        # Keep the player inside the view
        if player_cords['x'] < 0:
            player_cords['x'] = 0
        if player_cords['x'] > DISPLAY_SIZE[0]:
            player_cords['x'] = DISPLAY_SIZE[0]
        if player_cords['y'] < 0:
            player_cords['y'] = 0
        if player_cords['y'] > DISPLAY_SIZE[1]:
            player_cords['y'] = DISPLAY_SIZE[1]


        # Input
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Key Presses
            if event.type == KEYDOWN:
                input_keys[event.key] = True
            if event.type == KEYUP:
                input_keys[event.key] = False

        # Create a copy of the surface for special effects

        if frame_count%15 == 0:
            special = display.copy()

        
        frame_count += 1
        if frame_count%60 == 0:
            time_s += 1
        if frame_count > 720:
            frame_count = 0

        
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)


main_menu()
