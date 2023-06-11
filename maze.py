import pygame
from subprocess import Popen, PIPE
import time

import fps_monitor
import draw_text

DEFAULT_DIFFICULTY = 10
MAZE_GENERATOR_PATH = "maze_gen.exe"
MAZE_WALL_COLOUR = (0, 0, 0)
MAZE_BACKGROUND_COLOUR = (255, 255, 255)
WALL_WIDTH = 2

MIN_OFFSET = 10

MAZE_RUNNER_SIZE = 10
MAZE_RUNNER_COLOUR = (255, 0, 0)
MAZE_RUNNER_SPEED = 5

GOAL_COLOUR = (0, 255, 0)

FONT = "comicsansms"

UP_CONTROLS = [pygame.K_UP, pygame.K_w]
LEFT_CONTROLS = [pygame.K_LEFT, pygame.K_a]
DOWN_CONTROLS = [pygame.K_DOWN, pygame.K_s]
RIGHT_CONTROLS = [pygame.K_RIGHT, pygame.K_d]

MAX_FRAME_RATE = 60


class MAZE_TILE:
    WALL = 0
    PATH = 1



def key_from_set_pressed(keys, valid_keys_set):
    for key in valid_keys_set:
        if keys[key]:
            return True
    return False

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
                self.walls[1] = False
            elif pos[0] == self.x - 1:
                self.walls[3] = False


class MazeWall:
    def __init__(self, start: (int, int), end: (int, int)):
        self.start = start
        self.end = end

    def draw(self, screen):
        return pygame.draw.line(screen, MAZE_WALL_COLOUR, self.start, self.end, WALL_WIDTH)


class Maze:
    def parse_layout_grid(self):
        for edge in self.graph_data:
            if edge == "" or edge == "\n":
                continue
            a, b = edge.split(" ")
            a = a.split(",")
            b = b.split(",")
            a = (int(a[0]), int(a[1]))
            b = (int(b[0]), int(b[1]))
            self.cells[a[0]][a[1]].add_neighbour(b)
            self.cells[b[0]][b[1]].add_neighbour(a)

    def __init__(self, graph_data, size, canvas_width, canvas_height, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

        self.size = size
        self.graph_data = graph_data
        self.start = None
        self.end = None

        self.cells = [[MazeCell(i, j) for j in range(self.size)] for i in range(self.size)]

        self.walls = []
        self.wall_colliders = []

        self.walls_width = 0
        self.px_size = None

        if canvas_width < canvas_height:
            self.x_offset = MIN_OFFSET
            self.cell_size = (canvas_width - self.walls_width - MIN_OFFSET) // self.size - 1
            self.px_size = self.cell_size * self.size + self.walls_width
            self.y_offset = (canvas_height - self.px_size) // 2 + MIN_OFFSET
        else:
            self.y_offset = MIN_OFFSET
            self.cell_size = (canvas_height - self.walls_width - MIN_OFFSET) // self.size - 1
            self.px_size = self.cell_size * self.size + self.walls_width
            self.x_offset = (canvas_width - self.px_size) // 2 + MIN_OFFSET

        self.parse_layout_grid()
        # self.add_outer_walls()
        self.add_inner_walls()

        self.goal_collider = None

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
        self.wall_colliders = []
        for wall in self.walls:
            wall_rect = wall.draw(screen)
            self.wall_colliders.append(wall_rect)
        self.draw_goal(screen)

    def get_px_position(self, pos: (int, int)):
        x = self.x_offset + pos[0] * self.cell_size
        y = self.y_offset + pos[1] * self.cell_size
        return x, y

    def draw_goal(self, screen):
        x, y = self.get_px_position(self.end_pos)
        self.goal_collider = pygame.draw.circle(screen, GOAL_COLOUR, (x + self.cell_size // 2, y + self.cell_size // 2),
                                                self.cell_size // 4)


class MazeRunner:
    def __init__(self, start_pos: (int, int)):
        self.start_pos = start_pos
        self.rect = pygame.Rect(start_pos[0], start_pos[1], MAZE_RUNNER_SIZE, MAZE_RUNNER_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, MAZE_RUNNER_COLOUR, self.rect)

    def move(self, dx, dy, wall_colliders):
        old_pos = self.rect
        self.rect = self.rect.move(dx, dy)
        if self.rect.collidelist(wall_colliders) != -1:
            self.rect = old_pos
            return False


    def update(self, screen, keys, wall_colliders):
        if key_from_set_pressed(keys, UP_CONTROLS):
            self.move(0, -MAZE_RUNNER_SPEED, wall_colliders)
        if key_from_set_pressed(keys, LEFT_CONTROLS):
            self.move(-MAZE_RUNNER_SPEED, 0, wall_colliders)
        if key_from_set_pressed(keys, DOWN_CONTROLS):
            self.move(0, MAZE_RUNNER_SPEED, wall_colliders)
        if key_from_set_pressed(keys, RIGHT_CONTROLS):
            self.move(MAZE_RUNNER_SPEED, 0, wall_colliders)

        self.draw(screen)


class MazeInator:
    """
    Class that handles the maze minigame
    """

    def generate_maze(self):
        maze_gen = Popen([f"./{MAZE_GENERATOR_PATH}", str(self.difficulty)], stdout=PIPE)
        time.sleep(0.1)
        maze_gen_output = open("maze.maze", "r").read()
        size = maze_gen_output.split("\n")[0]
        size = int(size)
        start_pos = maze_gen_output.split("\n")[1]
        start_pos = start_pos.split(",")
        start_pos = (int(start_pos[0]), int(start_pos[1]))
        goal = maze_gen_output.split("\n")[2]
        goal = goal.split(",")
        goal = (int(goal[0]), int(goal[1]))
        maze = maze_gen_output.split("\n")[3:]
        self.maze = Maze(maze, size, self.screen_width, self.screen_height, start_pos, goal)

    def __init__(self, screen: pygame.surface.Surface, difficulty, time_limit=15):
        """
        :param screen: The PyGame screen to draw to
        :param difficulty: The difficulty of the maze (the dimensions of the maze)
        :param time_limit: Time that the player has to solve the maze, in seconds
        """

        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.maze: Maze = None
        self.difficulty = difficulty

        self.time_started = time.time()
        self.time_limit = time_limit
        self.game_running = True
        self.won = False

        self.clock = pygame.time.Clock()

        self.generate_maze()

        px_position = self.maze.get_px_position(self.maze.start_pos)
        x = px_position[0] + self.maze.cell_size // 2 - MAZE_RUNNER_SIZE // 2
        y = px_position[1] + self.maze.cell_size // 2 - MAZE_RUNNER_SIZE // 2
        self.runner = MazeRunner((x, y))

    def draw_message(self, message: str, colour: (int, int, int)):
        draw_text.fullscreen(self.screen, message, colour, MAZE_BACKGROUND_COLOUR, FONT)

    def draw_timer(self):
        seconds_elapsed = time.time() - self.time_started
        time_left = self.time_limit - seconds_elapsed
        timer = float(time_left)
        timer = round(timer, 2)
        timer = str(timer)
        draw_text.draw_in_corner(self.screen, timer, draw_text.CORNERS.TOP_RIGHT, (255, 255, 255), FONT)

    def draw(self):
        self.screen.fill(MAZE_BACKGROUND_COLOUR)
        self.maze.draw(self.screen)
        self.draw_timer()

    def update(self) -> int:
        """
        Function that should be called each frame to update the maze minigame
        :return: Returns 0 if game is running, 1 if maze has been solved, and -1 if the player has run out of time
        """
        current_time = time.time()
        seconds_elapsed = current_time - self.time_started
        if seconds_elapsed > self.time_limit and not self.won:
            self.game_running = False
            self.won = False
        if self.game_running:
            self.draw()
            self.runner.update(self.screen, pygame.key.get_pressed(), self.maze.wall_colliders)
            if self.runner.rect.colliderect(self.maze.goal_collider):
                self.game_running = False
                self.won = True

            self.clock.tick(MAX_FRAME_RATE)
            return 0
        else:
            if self.won:
                self.draw_message("You won!", (0, 128, 0))
                return 1
            else:
                self.draw_message("Time's up!", (255, 0, 0))
                return -1


def main():
    # Demo usage of MazeInator class. Should be used in a similar way
    # the following code snippet will be commented to demonstrate how to use the MazeInator class

    # Here is the usual PyGame initialization
    pygame.init()
    screen = pygame.display.set_mode((1400, 1000))
    pygame.display.set_caption("Maze")

    maze = MazeInator(screen, DEFAULT_DIFFICULTY, 20)  # Creating the MazeInator object.
    # Documented via docstring
    fps = fps_monitor.FPSMonitor(screen)  # Creating the FPS monitor

    while True:
        # Usual PyGame quit handling. Game logic other than the maze minigame would also be in this section
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


        maze.update()  # Calling the update method. This is the only method that needs to be called. Returns
        # game state (0 - running, 1 - won, -1 - lost).
        fps.update()  # Updating the FPS monitor
        pygame.display.flip()  # Usual PyGame stuff


if __name__ == '__main__':
    main()
