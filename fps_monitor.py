import pygame
import time

import draw_text

UPDATE_EVERY_SECONDS = 1


class FPSMonitor:
    def __init__(self, screen: pygame.surface.Surface):
        self.screen = screen
        self.last_update_time = time.time()
        self.frames_since_last_update = 0
        self.fps: int = 0

    def draw_fps(self):
        draw_text.draw_in_corner(self.screen, f"FPS: {self.fps}", draw_text.CORNERS.TOP_LEFT, (255, 255, 255),
                                 "Arial", 12)

    def update(self):
        self.frames_since_last_update += 1
        if time.time() - self.last_update_time >= UPDATE_EVERY_SECONDS:
            self.fps = self.frames_since_last_update // UPDATE_EVERY_SECONDS
            self.frames_since_last_update = 0
            self.last_update_time = time.time()
        self.draw_fps()
