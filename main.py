import pygame
from sys import exit
import random

pygame.init()
clock=pygame.time.Clock()

screen_width=551
screen_height=720
screen=pygame.display.set_mode((screen_width, screen_height))

sky_image=pygame.image.load("assets1/background.png")
ground_image=pygame.image.load("assets1/ground.png")
bird_images=[pygame.image.load("assets1/bird_down.png"),
             pygame.image.load("assets1/bird_mid.png"),
             pygame.image.load("assets1/bird_up.png")]
top_obstacle_image=pygame.image.load("assets1/pipe_top.png")
bottom_obstacle_image=pygame.image.load("assets1/pipe_bottom.png")

scroll_speed=1

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image=ground_image
        self.rect=self.image.get_rect()
        self.rect.x, self.rect.y=x, y
    
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.x<=-screen_width:
            self.kill()

def exit_game():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

bird_start_pos=(100,250)
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=bird_images[0]
        self.rect=self.image.get_rect()
        self.rect.center=bird_start_pos
        self.image_index=0
        self.vel=0
        self.jump=False
    
    def update(self, user_input):
        self.image_index+=1
        if self.image_index>=30:
            self.image_index=0
        self.image=bird_images[self.image_index//10]

        self.vel+=0.5
        if self.vel>7:
            self.vel=7
        if self.rect.y<500:
            self.rect.y+=int(self.vel)
        if self.vel==0:
            self.jump=False

        if user_input[pygame.K_SPACE] and not self.jump and self.rect.y>0:
            self.jump=True
            self.vel=-7

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x, self.rect.y=x, y

    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.x<=-screen_width:
            self.kill()

def exit_game():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

def main():

    x_ground, y_ground=0,520
    ground=pygame.sprite.Group()
    ground.add(Ground(x_ground, y_ground))

    bird=pygame.sprite.GroupSingle()
    bird.add(Bird())

    obstacle_timer=0
    obstacles=pygame.sprite.Group()

    run=True
    while run:
        
        exit_game()

        screen.fill((0,0,0))

        screen.blit(sky_image, (0,0))

        if len(ground)<=2:
            ground.add(Ground(screen_width, y_ground))

        user_input=pygame.key.get_pressed()

        if obstacle_timer<=0:
            x_top, x_bottom=550, 550
            y_top=random.randint(-600, -480)
            y_bottom=y_top+random.randint(90,130)+bottom_obstacle_image.get_height()
            obstacles.add(Obstacle(x_top, y_top, top_obstacle_image))
            obstacles.add(Obstacle(x_bottom, y_bottom, bottom_obstacle_image))
            obstacle_timer=random.randint(225,260)
        obstacle_timer-=1
        
        ground.draw(screen)
        bird.draw(screen)
        obstacles.draw(screen)

        ground.update()
        bird.update(user_input)
        obstacles.update()


        clock.tick(60)
        pygame.display.update()
main()   