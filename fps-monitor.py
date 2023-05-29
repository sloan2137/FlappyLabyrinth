import pygame
import time

UPDATE_EVERY_SECONDS = 1


class FPSMonitor:
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.last_update_time = time.time()
        self.frames_since_last_update = 0
        self.fps = None

    def draw_fps(self):
        pass

    def update(self):
        self.frames_since_last_update += 1
        if time.time() - self.last_update_time >= UPDATE_EVERY_SECONDS:
            self.fps = self.frames_since_last_update / UPDATE_EVERY_SECONDS
        self.draw_fps()
