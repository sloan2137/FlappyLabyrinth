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

def main():

    x_ground, y_ground=0,520
    ground=pygame.sprite.Group()
    ground.add(Ground(x_ground, y_ground))

    run=True
    while run:
        
        exit_game()

        screen.fill((0,0,0))

        screen.blit(sky_image, (0,0))

        if len(ground)<=2:
            ground.add(Ground(screen_width, y_ground))
        
        ground.draw(screen)

        ground.update()

        clock.tick(60)
        pygame.display.update()
main()   