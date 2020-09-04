# This script creates a grid with 20x15 cells.

import numpy as np
import pygame

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

INITIAL_ROBOT_POS_ROW = 18
INITIAL_ROBOT_POS_COL = 1


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


def col_to_make_turn(grid_):
    explored_grid = np.empty([20, 15], dtype=int)
    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid_[i][j].explored == 1:
                explored_grid[i, j] = 1
            else:
                explored_grid[i, j] = 0
    non_zero_array = np.count_nonzero(explored_grid, axis=0)

    return np.argmin(non_zero_array)


def turn_left(robot_):
    if check_left(robot_):
        if robot_.direction == "E":
            robot_.direction = "N"

        elif robot_.direction == "N":
            robot_.direction = "W"

        elif robot_.direction == "W":
            robot_.direction = "S"

        elif robot_.direction == "S":
            robot_.direction = "E"

    elif check_forward(robot_):
        pass

    elif check_right(robot_):
        if robot_.direction == "E":
            robot_.direction = "S"

        elif robot_.direction == "N":
            robot_.direction = "E"

        elif robot_.direction == "W":
            robot_.direction = "N"

        elif robot_.direction == "S":
            robot_.direction = "W"

    else:
        if robot_.direction == "E":
            robot_.direction = "W"

        elif robot_.direction == "N":
            robot_.direction = "S"

        elif robot_.direction == "W":
            robot_.direction = "E"

        elif robot_.direction == "S":
            robot_.direction = "N"


def check_for_wall(robot_):
    if robot_.direction == 'N':
        if grid[robot.row - 2][robot.column].virtual_wall == 1:
            return True
        else:
            return False
    elif robot_.direction == 'S':
        if grid[robot.row + 2][robot.column].virtual_wall == 1:
            return True
        else:
            return False
    elif robot_.direction == 'E':
        if grid[robot.row][robot.column + 2].virtual_wall == 1:
            return True
        else:
            return False
    else:
        if grid[robot.row][robot.column - 2].virtual_wall == 1:
            return True
        else:
            return False


def update_explored_cells(robot_, grid_):
    row_ = robot_.row
    column_ = robot_.column

    for i in range(row_ - 1, row_ + 2):
        for j in range(column_ - 1, column_ + 2):
            grid_[i][j].explored = 1


def robot_movement(robot_):
    if robot_.direction == "N":
        robot_.row -= 1

    elif robot_.direction == "S":
        robot_.row += 1

    elif robot_.direction == "E":
        robot_.column += 1

    elif robot_.direction == "W":
        robot_.column -= 1

    else:
        pass


def update_robot_dir_right_wall(robot_):
    if check_right(robot_):
        if robot_.direction == "E":
            robot_.direction = "S"

        elif robot_.direction == "N":
            robot_.direction = "E"

        elif robot_.direction == "W":
            robot_.direction = "N"

        elif robot_.direction == "S":
            robot_.direction = "W"

    elif check_forward(robot_):
        pass

    elif check_left(robot_):
        if robot_.direction == "E":
            robot_.direction = "N"

        elif robot_.direction == "N":
            robot_.direction = "W"

        elif robot_.direction == "W":
            robot_.direction = "S"

        elif robot_.direction == "S":
            robot_.direction = "E"

    else:
        if robot_.direction == "E":
            robot_.direction = "W"

        elif robot_.direction == "N":
            robot_.direction = "S"

        elif robot_.direction == "W":
            robot_.direction = "E"

        elif robot_.direction == "S":
            robot_.direction = "N"


def check_right(robot_):
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if column_ != COLUMNS - 2 and check_obs_east(row_, column_):
            return True

    elif robot_.direction == "S":
        if column_ != 1 and check_obs_west(row_, column_):
            return True

    elif robot_.direction == "E":
        if row_ != ROWS - 2 and check_obs_south(row_, column_):
            return True

    elif robot_.direction == "W":
        if row_ != 1 and check_obs_north(row_, column_):
            return True

    return False


def check_forward(robot_):
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if row_ != 1 and check_obs_north(row_, column_):
            return True

    elif robot_.direction == "S":
        if row_ != ROWS - 2 and check_obs_south(row_, column_):
            return True

    elif robot_.direction == "E":
        if column_ != COLUMNS - 2 and check_obs_east(row_, column_):
            return True

    elif robot_.direction == "W":
        if column_ != 1 and check_obs_west(row_, column_):
            return True

    return False


def check_left(robot_):
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if column_ != 1 and check_obs_west(row_, column_):
            return True

    elif robot_.direction == "S":
        if column_ != COLUMNS - 2 and check_obs_east(row_, column_):
            return True

    elif robot_.direction == "E":
        if row_ != 1 and check_obs_north(row_, column_):
            return True

    elif robot_.direction == "W":
        if row_ != ROWS - 2 and check_obs_south(row_, column_):
            return True

    return False


def check_obs_north(row_, column_):
    if (
            grid[row_ - 2][column_].obstacle, grid[row_ - 2][column_ + 1].obstacle,
            grid[row_ - 2][column_ - 1].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_obs_south(row_, column_):
    if (
            grid[row_ + 2][column_].obstacle, grid[row_ + 2][column_ + 1].obstacle,
            grid[row_ + 2][column_ - 1].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_obs_east(row_, column_):
    if (
            grid[row_][column_ + 2].obstacle, grid[row_ + 1][column_ + 2].obstacle,
            grid[row_ - 1][column_ + 2].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_obs_west(row_, column_):
    if (
            grid[row_][column_ - 2].obstacle, grid[row_ + 1][column_ - 2].obstacle,
            grid[row_ - 1][column_ - 2].obstacle) == (
            0, 0, 0):
        return True

    return False


pygame.init()
WINDOW_SIZE = [500, 480]
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
font = pygame.font.SysFont("comicsansms", 24)
text = font.render("GO!", True, (0, 128, 0))
done = False
move = False
col_to_turn = -1
clock = pygame.time.Clock()
flag = True
initial_run = 0

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
        clock.tick(12)
        update_explored_cells(robot, grid)
        if flag:
            update_robot_dir_right_wall(robot)
        else:
            if check_for_wall(robot):
                update_robot_dir_right_wall(robot)

        robot_movement(robot)
        if (robot.row == INITIAL_ROBOT_POS_ROW or robot.row == INITIAL_ROBOT_POS_ROW-1) and (robot.column == INITIAL_ROBOT_POS_COL or robot.column == INITIAL_ROBOT_POS_COL+1):
            if initial_run == 1:
                print("Reached initial state.")
                col_to_turn = col_to_make_turn(grid)
            else:
                initial_run = 1

        if robot.column == col_to_turn and initial_run == 1:
            flag = not flag
            turn_left(robot)
            initial_run = 0


    screen.fill(BLACK)

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
            else:
                if grid[row][column].explored == 1:
                    color = ORANGE

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

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
