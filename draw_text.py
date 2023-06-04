import pygame


class CORNERS:
    TOP_LEFT = (0, 0)
    TOP_RIGHT = (1, 0)
    BOTTOM_LEFT = (0, 1)
    BOTTOM_RIGHT = (1, 1)


def fullscreen(screen: pygame.surface.Surface, text: str, text_colour: (int, int, int), bg_colour: (int, int, int),
               font: str, font_size: int = 72):
    screen.fill(bg_colour)
    font = pygame.font.SysFont(font, font_size)
    text = font.render(text, True, text_colour)
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    screen.blit(text, text_rect)


def draw_in_corner(screen: pygame.surface.Surface, text: str, pos, text_colour: (int, int, int), font: str,
                   font_size: int = 20, offset=50):
    font = pygame.font.SysFont(font, 20)
    text = font.render(text, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() - offset if pos[0] else offset,
                        screen.get_height() - offset if pos[1] else offset)
    screen.blit(text, text_rect)
