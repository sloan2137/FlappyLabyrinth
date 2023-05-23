import pygame
from subprocess import Popen, PIPE
import time

DEFAULT_DIFFICULTY = 100
MAZE_GENERATOR_PATH = "maze_gen.exe"
MAZE_WALL_COLOUR = (0, 0, 0)
MAZE_BACKGROUND_COLOUR = (255, 255, 255)
WALL_WIDTH = 2

MIN_OFFSET = 10


class MAZE_TILE:
    WALL = 0
    PATH = 1


class MazeCell:
    def __init__(self, x, y, is_start=False, is_end=False):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]
        self.is_start = is_start
        self.is_end = is_start

    def top_wall(self):
        return self.walls[0]

    def right_wall(self):
        return self.walls[1]

    def bottom_wall(self):
        return self.walls[2]

    def left_wall(self):
        return self.walls[3]

    def set_start(self):
        self.is_start = True

    def set_end(self):
        self.is_end = True

    def add_neighbour(self, pos: (int, int)):
        if pos[0] == self.x:
            if pos[1] == self.y + 1:
                self.walls[2] = False
            elif pos[1] == self.y - 1:
                self.walls[0] = False
        elif pos[1] == self.y:
            if pos[0] == self.x + 1:
                print("here")
                self.walls[1] = False
            elif pos[0] == self.x - 1:
                self.walls[3] = False


class MazeWall:
    def __init__(self, start: (int, int), end: (int, int)):
        self.start = start
        self.end = end

    def draw(self, screen):
        pygame.draw.line(screen, MAZE_WALL_COLOUR, self.start, self.end, WALL_WIDTH)


class Maze:
    def parse_layout_grid(self):
        for edge in self.graph_data:
            a, b = edge.split(" ")
            a = a.split(",")
            b = b.split(",")
            a = (int(a[0]), int(a[1]))
            b = (int(b[0]), int(b[1]))
            self.cells[a[0]][a[1]].add_neighbour(b)
            self.cells[b[0]][b[1]].add_neighbour(a)

    def __init__(self, graph_data, size, canvas_width, canvas_height):
        self.size = size
        self.graph_data = graph_data
        self.start = None
        self.end = None

        self.cells = [[MazeCell(i, j) for j in range(self.size)] for i in range(self.size)]

        self.walls = []

        self.walls_width = 0
        self.px_size = None

        if canvas_width < canvas_height:
            self.x_offset = MIN_OFFSET
            self.cell_size = (canvas_width - self.walls_width - MIN_OFFSET) // self.size
            self.px_size = self.cell_size * self.size + self.walls_width
            self.y_offset = (canvas_height - self.px_size) // 2 + MIN_OFFSET
        else:
            self.y_offset = MIN_OFFSET
            self.cell_size = (canvas_height - self.walls_width - MIN_OFFSET) // self.size
            self.px_size = self.cell_size * self.size + self.walls_width
            self.x_offset = (canvas_width - self.px_size) // 2 + MIN_OFFSET

        self.parse_layout_grid()
        # self.add_outer_walls()
        self.add_inner_walls()

    def add_outer_walls(self):
        corner1 = (self.x_offset - WALL_WIDTH, self.y_offset - WALL_WIDTH)
        corner2 = (self.x_offset + self.px_size + WALL_WIDTH, self.y_offset - WALL_WIDTH)
        corner3 = (self.x_offset - WALL_WIDTH, self.y_offset + self.px_size + WALL_WIDTH)
        corner4 = (self.x_offset + self.px_size + WALL_WIDTH, self.y_offset +
                   self.px_size + WALL_WIDTH)

        self.walls.append(MazeWall(corner1, corner2))
        self.walls.append(MazeWall(corner1, corner3))
        self.walls.append(MazeWall(corner2, corner4))
        self.walls.append(MazeWall(corner3, corner4))

    def add_cell_walls(self, cell: MazeCell):
        x = self.x_offset + cell.x * self.cell_size
        y = self.y_offset + cell.y * self.cell_size
        if cell.top_wall():
            self.walls.append(MazeWall((x, y), (x + self.cell_size, y)))
        if cell.right_wall():
            print(cell.x, cell.y)
            self.walls.append(MazeWall((x + self.cell_size, y), (x + self.cell_size, y + self.cell_size)))
        if cell.bottom_wall():
            self.walls.append(MazeWall((x, y + self.cell_size), (x + self.cell_size, y + self.cell_size)))
        if cell.left_wall():
            self.walls.append(MazeWall((x, y), (x, y + self.cell_size)))

    def add_inner_walls(self):
        for row in self.cells:
            for cell in row:
                self.add_cell_walls(cell)

    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen)


class MazeInator:

    def generate_maze(self):
        maze_gen = Popen([f"./{MAZE_GENERATOR_PATH}", str(self.difficulty)], stdout=PIPE)
        time.sleep(0.1)
        maze_gen_output = open("maze.maze", "r").read()
        size = maze_gen_output.split("\n")[0]
        size = int(size)
        maze = maze_gen_output.split("\n")[1:]
        self.maze = Maze(maze, size, self.screen_width, self.screen_height)

    def __init__(self, screen: pygame.surface.Surface, difficulty, time_limit=15):

        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.maze: Maze = None
        self.difficulty = difficulty

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
        else:
            self.draw()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1400, 1000))
    pygame.display.set_caption("Maze")
    maze = MazeInator(screen, DEFAULT_DIFFICULTY)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        maze.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
