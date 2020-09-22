# This script creates a grid with 20x15 cells.

import numpy as np
import pygame
from fastestpath import search

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 3

ROWS = 20
COLUMNS = 15

TARGET_ROBOT_POS_ROW = 18
TARGET_ROBOT_POS_COL = 1


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
        self.direction = "E"


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

grid[9][1].obstacle = 1

grid[14][3].obstacle = 1
grid[14][4].obstacle = 1
grid[14][5].obstacle = 1
grid[15][5].obstacle = 1

grid[3][4].obstacle = 1
grid[4][4].obstacle = 1
grid[5][4].obstacle = 1

grid[0][8].obstacle = 1

grid[9][6].obstacle = 1
grid[9][7].obstacle = 1

grid[5][9].obstacle = 1
grid[5][10].obstacle = 1
grid[5][11].obstacle = 1
grid[5][12].obstacle = 1
grid[5][13].obstacle = 1
grid[5][14].obstacle = 1

grid[14][11].obstacle = 1
grid[15][11].obstacle = 1
grid[16][11].obstacle = 1
grid[17][11].obstacle = 1

maze = [[0 for j in range(COLUMNS)] for i in range(ROWS)]

for row in range(ROWS):
    for column in range(COLUMNS):
        if grid[row][column].obstacle:
            for r in range(row - 1, row + 2):
                for c in range(column - 1, column + 2):
                    if r < 0 or r >= ROWS or c < 0 or c >= COLUMNS:
                        continue
                    
                    if grid[r][c].obstacle == 0:
                        grid[r][c].virtual_wall = 1

for i in range(ROWS):
    for j in range(COLUMNS):
        if grid[i][j].obstacle:
            maze[i][j] = 1
        if grid[i][j].virtual_wall:
            maze[i][j] = 2
        grid[i][j].explored = 1

path = search(maze, 1, [18, 1], [1, 13])

pygame.init()
WINDOW_SIZE = [500, 480]
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
font = pygame.font.SysFont("comicsansms", 24)
text = font.render("GO!", True, (0, 128, 0))
done = False
move = False
clock = pygame.time.Clock()
col_to_turn = -1
right_wall_hug = True
prev_total, curr_total = 0, 0

i = 0
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
        clock.tick(60)
        robot.row, robot.column = path[i][0]
        robot.direction = path[i][1]
        i += 1

    screen.fill(BLACK)

    for row in range(ROWS):
        for column in range(COLUMNS):
            
            if grid[row][column].explored:
                color = WHITE
                if grid[row][column].obstacle == 1:
                    color = RED                                
                elif grid[row][column].virtual_wall == 1:
                    color = GREY

            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH, HEIGHT])

    # start
    pygame.draw.rect(screen, GREEN,
                     [MARGIN, (MARGIN + HEIGHT) * 17 + MARGIN, WIDTH * 3 + MARGIN * 2, HEIGHT * 3 + MARGIN * 2])

    # goal
    pygame.draw.rect(screen, YELLOW,
                     [(MARGIN + WIDTH) * 12 + MARGIN, MARGIN, WIDTH * 3 + MARGIN * 2, HEIGHT * 3 + MARGIN * 2])

    # robot
    pygame.draw.rect(screen, BLUE,
                     [(MARGIN + WIDTH) * (robot.column - 1) + MARGIN,
                      (MARGIN + HEIGHT) * (robot.row - 1) + MARGIN,
                      WIDTH * 3 + MARGIN * 2, HEIGHT * 3 + MARGIN * 2])

    # button
    pygame.draw.rect(screen, WHITE, (380, 40, 80, 20))
    screen.blit(text, (405, 45))

    clock.tick(30)
    pygame.display.flip()

pygame.quit()
