import pygame
from pygame.locals import *
import random

# shape parameters
size = width, height = (800, 800)
road_w = int(width / 1.6)
roadmark_w = int(width / 80)
middle_line_w = int(width / 200)  # Width of the middle yellow line
# location parameters
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
# animation parameters
speed = 1

# initialize the app
pygame.init()
running = True

# set window size
screen = pygame.display.set_mode(size)
# set window title
pygame.display.set_caption("Ngida's car game")
# set background color
screen.fill((0, 0, 0))
# apply changes
pygame.display.update()

# load player vehicle
car = pygame.image.load("car.png")
car_loc = car.get_rect()
car_loc.center = right_lane, height * 0.8

# load enemy vehicle
car2 = pygame.image.load("otherCar.png")
car2_loc = car2.get_rect()
car2_loc.center = left_lane, height * 0.2

# load tree image
tree = pygame.image.load("Forest.png")

player_speed = 0
road_pos = 0
car2_speed = speed
score = 0

# font for leaderboard display
font_name = pygame.font.match_font('arial')
font_size = 36
score_font = pygame.font.Font(font_name, font_size)

def draw_road_markings():
    # draw left road marking
    for y in range(-height, height + road_w, 100):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 - road_w / 2 + roadmark_w * 2, (y - road_pos) % height, roadmark_w, 80))

    # draw right road marking
    for y in range(-height, height + road_w, 100):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (width / 2 + road_w / 2 - roadmark_w * 3, (y - road_pos) % height, roadmark_w, 80))

    # draw middle line
    for y in range(-height, height + road_w, 100):
        pygame.draw.rect(
            screen,
            (255, 240, 60),
            (width / 2 - middle_line_w / 2, (y - road_pos) % height, middle_line_w, 20))

def draw_trees():
    # draw trees on the left side of the road
    for y in range(-height, height + road_w, 300):
        screen.blit(tree, (width / 2 - road_w / 2 - tree.get_width(), (y - road_pos) % height))

    # draw trees on the right side of the road
    for y in range(-height, height + road_w, 300):
        screen.blit(tree, (width / 2 + road_w / 2, (y - road_pos) % height))

# game loop
while running:
    # event listeners
    player_moved = False  # Flag to track if the player has moved left or right
    for event in pygame.event.get():
        if event.type == QUIT:
            # collapse the app
            running = False
        if event.type == KEYDOWN:
            # move user car to the left
            if event.key in [K_a, K_LEFT]:
                car_loc = car_loc.move([-int(road_w / 2), 0])
                player_moved = True
            # move user car to the right
            if event.key in [K_d, K_RIGHT]:
                car_loc = car_loc.move([int(road_w / 2), 0])
                player_moved = True
            # increase speed when the up arrow key is pressed
            if event.key == K_UP:
                player_speed += 0.15

    # animate enemy vehicle
    car2_loc[1] += car2_speed
    if car2_loc[1] > height:
        # randomly select lane
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200
        car2_speed = speed + player_speed

    # update road position
    road_pos += player_speed * speed

    # draw road, markings, and trees
    screen.fill((0, 0, 0))
    draw_road_markings()
    draw_trees()

    # place car images on the screen
    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)

    # update and draw leaderboard
    score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))  # White color
    score_rect = score_text.get_rect()
    score_rect.center = (width // 2, 50)
    screen.blit(score_text, score_rect)

    # increase score when the car is dodged
    if car2_loc.y <= 0 and player_moved and not car_loc.colliderect(car2_loc):
        score += 1

        # Display score increment message on the screen
        score_increment_text = score_font.render("Great!", True, (255, 255, 255))
        screen.blit(score_increment_text, (width // 2 - score_increment_text.get_width() // 2, 100))

    # apply changes
    pygame.display.update()

    # end game logic - check for collision
    if car_loc.colliderect(car2_loc):
        print("GAME OVER! YOU LOST!")
        break

# collapse application window
pygame.quit()
 

