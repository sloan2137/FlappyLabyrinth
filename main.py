import pygame
from sys import exit
import random

pygame.init()
clock=pygame.time.Clock()

screen_width=551
screen_height=720
screen=pygame.display.set_mode((screen_width, screen_height))

sky_image=pygame.image.load("assets1/background.png")

def exit_game():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

def main():
    
    run=True
    while run:
        
        exit_game()

        screen.fill((0,0,0))

        screen.blit(sky_image, (0,0))

        clock.tick(60)
        pygame.display.update()
main()   