import sys

import pygame
from sys import exit
import random
import time

import maze as mz

pygame.init()
clock = pygame.time.Clock()

screen_width = 551
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

sky_image = pygame.image.load("assets1/background.png")
ground_image = pygame.image.load("assets1/ground.png")
bird_images = [pygame.image.load("assets1/bird_down.png"),
               pygame.image.load("assets1/bird_mid.png"),
               pygame.image.load("assets1/bird_up.png")]
top_obstacle_image = pygame.image.load("assets1/pipe_top.png")
bottom_obstacle_image = pygame.image.load("assets1/pipe_bottom.png")
game_over_image = pygame.image.load("assets1/bad_end.png")
good_over_image = pygame.image.load("assets1/good_over.png")
start_image = pygame.image.load("assets1/start.png")
agent_image = pygame.image.load("assets1/agent.png")
coin_image = pygame.image.load("assets1/coin.png")

MAZE_START_SIZE = 10
MAZE_SIZE_INCREMENT = 2
MAZE_TIME_LIMIT = 20
freq_diff_x, freq_diff_y = 2, 6
coins_needed=3

scroll_speed = 2
bird_start_pos = (100, 250)
score = 0
font = pygame.font.SysFont('Segoe', 25)
game_stopped = True
timer = 0
appearing_frequency = random.randint(freq_diff_x, freq_diff_y)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_pos
        self.image_index = 0
        self.vel = 0
        self.jump = False
        self.alive = True

    def update(self, user_input):
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.jump = False

        if user_input[pygame.K_SPACE] and not self.jump and self.rect.y > 0 and self.alive:
            self.jump = True
            self.vel = -7


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image, obstacle_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.obstacle_type = obstacle_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen_width:
            self.kill()

        global score
        if self.obstacle_type == 'bottom':
            if bird_start_pos[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_pos[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen_width:
            self.kill()


class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = agent_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -screen_width:
            self.kill()


def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    global score
    global timer
    global appearing_frequency
    last_score=-1

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    obstacle_timer = 0
    obstacles = pygame.sprite.Group()

    x_ground, y_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_ground, y_ground))

    agent = pygame.sprite.Group()

    god_mode = False
    args = sys.argv
    if len(args) > 1:
        god_mode = args[1] == 'walczuk'

    maze_launched = 0
    maze_solved = 0

    after_maze = False
    after_good_end=False

    run = True
    while run:
        if god_mode:
            bird.sprite.alive = True

        exit_game()

        screen.fill((0, 0, 0))

        user_input = pygame.key.get_pressed()

        screen.blit(sky_image, (0, 0))

        if len(ground) <= 2:
            ground.add(Ground(screen_width, y_ground))

        obstacles.draw(screen)
        ground.draw(screen)
        bird.draw(screen)
        agent.draw(screen)

        screen.blit(coin_image,(0,5))
        maze_solved_text = font.render('x' + str(maze_solved), True, pygame.Color(255, 255, 255))
        screen.blit(maze_solved_text, (35, 13))

        if after_maze:
            pygame.display.update()
            after_maze = False
            while True:
                user_input = pygame.key.get_pressed()
                exit_game()
                if user_input[pygame.K_SPACE]:
                    break

        if bird.sprite.alive:
            ground.update()
            obstacles.update()
            agent.update()
        bird.update(user_input)

        collision_obstacles = pygame.sprite.spritecollide(bird.sprites()[0], obstacles, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if (collision_obstacles or collision_ground) and score!=last_score and score!=last_score+1 and not after_good_end:
            if maze_solved>0:
                maze_solved-=1
                last_score=score 
                after_maze=True
                
            else:
                bird.sprite.alive = False
                if collision_ground:
                    screen.blit(game_over_image, (0,0))
                    if user_input[pygame.K_r]:
                        score = 0
                        break
        
        if maze_solved==coins_needed:
            bird.sprite.alive = False
            screen.blit(good_over_image, (0,0))
            after_good_end=True
            if user_input[pygame.K_r]:
                score = 0
                after_good_end=False
                break

        if bird.sprite.alive and obstacle_timer <= 0:
            timer += 1
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(100, 120) + bottom_obstacle_image.get_height()
            obstacles.add(Obstacle(x_top, y_top, top_obstacle_image, 'top'))
            obstacles.add(Obstacle(x_bottom, y_bottom, bottom_obstacle_image, 'bottom'))

            if timer == appearing_frequency:
                obstacle_timer = 242

                appearing_frequency = random.randint(freq_diff_x, freq_diff_y)
                timer = 0

                x_agent, y_agent = 790, 420
                agent.add(Agent(x_agent, y_agent))

            else:
                obstacle_timer = random.randint(90, 120)

        obstacle_timer -= 1

        collision_agent = pygame.sprite.spritecollide(bird.sprites()[0], agent, False)

        if collision_agent:
            maze = mz.MazeInator(screen, MAZE_START_SIZE + MAZE_SIZE_INCREMENT * maze_launched, MAZE_TIME_LIMIT)
            maze_launched += 1
            maze_status = maze.update()
            while maze_status == 0:
                exit_game()
                maze_status = maze.update()
                pygame.display.update()
            if maze_status == 1:
                maze_solved += 1
                bird.sprite.alive = True
            time.sleep(1)
            after_maze = True
            agent.sprites()[0].kill()

        clock.tick(60)
        pygame.display.update()


def menu():
    global game_stopped
    global MAZE_START_SIZE
    global MAZE_SIZE_INCREMENT
    global freq_diff_x
    global freq_diff_y
    global coins_needed

    while game_stopped:
        exit_game()

        screen.fill((0, 0, 0))
        screen.blit(start_image, (0, 0))

        user_input = pygame.key.get_pressed()
        
        if user_input[pygame.K_e]:
            MAZE_START_SIZE=3
            MAZE_SIZE_INCREMENT=1
            freq_diff_x, freq_diff_y=2,3
            coins_needed=1
            main()
        if user_input[pygame.K_m]:
            MAZE_START_SIZE=5
            MAZE_SIZE_INCREMENT=2
            freq_diff_x, freq_diff_y=3,5
            coins_needed=3
            main()
        if user_input[pygame.K_h]:
            MAZE_START_SIZE=10
            MAZE_SIZE_INCREMENT=2
            freq_diff_x, freq_diff_y=4,8
            coins_needed=5
            main()
        if user_input[pygame.K_x]:
            MAZE_START_SIZE=15
            MAZE_SIZE_INCREMENT=3
            freq_diff_x, freq_diff_y=10,15
            coins_needed=5
            main()

        pygame.display.update()


menu()
