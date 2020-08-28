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

# Grid is an array of cells of the maze.
grid = []


class Cell:
    def __init__(self, row_, column_, explored):
        self.obstacle = 0
        self.virtual_wall = 0
        self.explored = explored
        self.row = row_
        self.column = column_


class Robot:
    def __init__(self):
        self.row = 17
        self.column = 1
        self.direction = "E"


for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        cell = Cell(row, column, 0)
        if row < 1 or row > 18 or column < 1 or column > 13:
            cell.virtual_wall = 1
        grid[row].append(cell)  # Append a cell

robot = Robot()


def robot_movement(robot_):
    row_ = robot_.row
    column_ = robot_.column
    if robot_.direction == "N":
        if grid[row_ - 1][column_].virtual_wall != 1:
            # if grid[row_ - 2][column_ - 1].obstacle == 0 and grid[row_ - 2][column_].obstacle == 0 and grid[row_ -
            # 2][column_ + 1].obstacle == 0:
            robot_.row -= 1
    elif robot_.direction == "S":

        robot_.row += 1
    elif robot_.direction == "E":
        if grid[row_ + 1][column_ + 2].virtual_wall != 1:
            robot_.column += 1
    else:
        if grid[row_ + 1][column_ - 2].virtual_wall != 1:
            robot_.column -= 1


pygame.init()
WINDOW_SIZE = [500, 480]
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
font = pygame.font.SysFont("comicsansms", 24)
text = font.render("GO!", True, (0, 128, 0))
done = False
move = False
clock = pygame.time.Clock()
while not done:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            print(row, column)
            if (row < 17 or column > 2) and (row > 2 or column < 12):
                cell = grid[row][column]
                cell.obstacle = 1
                print("Click ", pos, "Grid coordinates: ", row, column)
            if 460 > pos[0] > 300 and 60 > pos[1] > 40:
                move = True

    if move:
        robot_movement(robot)

    screen.fill(BLACK)

    grid[5][2].obstacle = 1
    grid[6][2].obstacle = 1
    grid[7][2].obstacle = 1

    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column].obstacle == 1:
                color = RED
                for r in range(row - 1, row + 2):
                    for c in range(column - 1, column + 2):
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
    pygame.draw.rect(screen, GREEN,
                     [MARGIN, (MARGIN + HEIGHT) * 17 + MARGIN, WIDTH * 3 + MARGIN * 2, HEIGHT * 3 + MARGIN * 2])

    # goal
    pygame.draw.rect(screen, YELLOW,
                     [(MARGIN + WIDTH) * 12 + MARGIN, MARGIN, WIDTH * 3 + MARGIN * 2, HEIGHT * 3 + MARGIN * 2])

    # robot
    pygame.draw.rect(screen, BLUE,
                     [(MARGIN + WIDTH) * (robot.column - 1) + MARGIN,
                      (MARGIN + HEIGHT) * robot.row + MARGIN,
                      WIDTH * 3 + MARGIN * 2, HEIGHT * 3 + MARGIN * 2])

    # button
    pygame.draw.rect(screen, WHITE, (380, 40, 80, 20))
    screen.blit(text, ((380 + (50 / 2)), 45))
    clock.tick(6)
    pygame.display.flip()

pygame.quit()
