# This script creates a grid with 20x15 cells.


import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 3

ROWS = 20
COLUMNS = 15


class Cell:
    def __init__(self, row_, column_, explored):
        self.obstacle = 0
        self.virtual_wall = 0
        self.explored = explored
        self.row = row_
        self.column = column_

class Robot:
    def __init__(self):
        self.row = 18
        self.column = 1
        self.direction = "N"

# Grid is an array of cells of the maze.
grid = []

for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        cell = Cell(row, column, 0)
        if row < 1 or row > 18 or column < 1 or column > 13:
            cell.virtual_wall = 1
        grid[row].append(cell)  # Append a cell

robot = Robot()

def move_forward(robot):
    r = robot.row
    c = robot.column
    if robot.direction == "N":
        if grid[r - 2][c - 1].obstacle == 0 and grid[r - 2][c].obstacle == 0 and grid[r - 2][c + 1].obstacle == 0:
            robot.row -= 1

pygame.init()
WINDOW_SIZE = [360, 480]
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0]//(WIDTH+MARGIN)
            row = pos[1]//(HEIGHT + MARGIN)
            if (row < 17 or column > 2) and (row > 2 or column < 12):
                cell = grid[row][column]
                cell.obstacle = 1
                print("Click ", pos, "Grid coordinates: ", row, column)

    screen.fill(BLACK)

    grid[5][2].obstacle = 1
    grid[6][2].obstacle = 1
    grid[7][2].obstacle = 1

    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column].obstacle == 1:
                color = RED
                for r in range(row-1, row+2):
                    for c in range(column-1, column+2):
                        if grid[r][c].obstacle == 0:
                            grid[r][c].virtual_wall = 1
            elif grid[row][column].virtual_wall == 1:
                color = GREY
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # start
    pygame.draw.rect(screen, GREEN, [MARGIN, (MARGIN + HEIGHT) * 17 + MARGIN, WIDTH * 3+ MARGIN * 2, HEIGHT * 3+ MARGIN * 2])

    # goal
    pygame.draw.rect(screen, YELLOW, [(MARGIN + WIDTH) * 12 + MARGIN, MARGIN, WIDTH * 3+ MARGIN * 2, HEIGHT * 3+ MARGIN * 2])

    # robot
    pygame.draw.rect(screen, BLUE, [(MARGIN + WIDTH) * (robot.column - 1) + MARGIN, (MARGIN + HEIGHT) * (robot.row - 1) + MARGIN, WIDTH * 3+ MARGIN * 2, HEIGHT * 3+ MARGIN * 2])
    move_forward(robot)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
