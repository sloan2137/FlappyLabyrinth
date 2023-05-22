import pygame
from subprocess import Popen, PIPE
import time

DEFAULT_DIFFICULTY = 20
MAZE_GENERATOR_PATH = "maze_gen.cpp"
MAZE_WALL_COLOUR = (0, 0, 0)
MAZE_BACKGROUND_COLOUR = (255, 255, 255)
class MAZE_TILE:
    WALL = 0
    PATH = 1

class MazeTile:
    def __init__(self, row, col, size, x_offset, y_offset):
        self.row = row
        self.col = col
        self.size = size
        self.x = self.col * self.size + x_offset
        self.y = self.row * self.size + y_offset
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        pygame.draw.rect(screen, MAZE_WALL_COLOUR, self.rect)


class Maze:
    def parse_layout_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.layout_grid[row][col] == "1":
                    self.grid[row][col] = MAZE_TILE.WALL
                elif self.layout_grid[row][col] == "0":
                    self.grid[row][col] = MAZE_TILE.PATH
                elif self.layout_grid[row][col] == "*":
                    self.start = (row, col)
                elif self.layout_grid[row][col] == ".":
                    self.end = (row, col)


    def __init__(self, layout_grid, rows, cols):
        self.rows = rows
        self.cols = cols
        self.layout_grid = layout_grid
        self.grid = None
        self.start = None
        self.end = None
        self.parse_layout_grid()

    def populate_tiles(self, tile_size, x_offset, y_offset):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == MAZE_TILE.FREE:
                    continue
                self.tiles[row][col] = MazeTile(row, col, tile_size, x_offset, y_offset)

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw(screen)

class MazeInator:

    def generate_maze(self):
        maze_gen = Popen([f"./{MAZE_GENERATOR_PATH}", str(self.difficulty)], stdout=PIPE)
        maze_gen_output = maze_gen.stdout.read().decode("utf-8")
        rows, cols = maze_gen_output.split("\n")[0].split(" ")
        maze = maze_gen_output.split("\n")[1:]
        self.maze = Maze(maze, int(rows), int(cols))


    def __init__(self, screen: pygame.surface.Surface, difficulty, time_limit=15):

        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.maze = None
        self.difficulty = difficulty

        tile_size: int = min(self.screen_width, self.screen_height) // self.difficulty
        x_offset = (self.screen_width - (tile_size * self.difficulty)) // 2 if self.screen_width > self.screen_height\
            else 0
        y_offset = (self.screen_height - (tile_size * self.difficulty)) // 2 if self.screen_height > self.screen_width\
            else 0

        self.time_started = time.time()
        self.time_limit = time_limit
        self.game_over = False

        self.generate_maze()

    def draw(self):
        self.screen.fill(MAZE_BACKGROUND_COLOUR)
        self.maze.draw(self.screen)

    def update(self):
        current_time = time.time()
        seconds_elapsed = current_time - self.time_started
        if seconds_elapsed >= self.time_limit:
            self.game_over = True
        if self.game_over:
            self.draw_game_over()
        else:
            self.draw()




def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Maze")
    maze = MazeInator(screen, DEFAULT_DIFFICULTY)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        maze.update()

        screen.fill((255, 255, 255))
        pygame.display.flip()


if __name__ == '__main__':
    main()
