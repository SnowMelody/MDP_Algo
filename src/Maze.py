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


def col_to_make_turn(grid_):
    explored_grid = np.empty([20, 15], dtype=int)
    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid_[i][j].explored == 1:
                explored_grid[i][j] = 1
            else:
                explored_grid[i][j] = 0
    non_zero_array = np.count_nonzero(explored_grid, axis=0)

    # Returns last index instead of first
    # idx = np.where(non_zero_array == non_zero_array.min())[0]
    # return idx[-1]
    return np.argmin(non_zero_array)


def update_explored_cells(robot_, grid_):
    row_ = robot_.row
    column_ = robot_.column

    # Mark 3x3 grid occupied by robot as explored
    for i in range(row_ - 1, row_ + 2):
        for j in range(column_ - 1, column_ + 2):
            grid_[i][j].explored = 1

    # Also mark 3 grids directly in front of robot's facing direction as explored (3 front sensors) And 1 front right
    # + 1 back right sensor? Wrt robot's facing direction (Not sure, I just simulate there, we can change accordingly)
    # Assuming the left sensor's reading is accurate up to 2 cells. can be increased to reduce exploration time.
    if robot_.direction == "N":
        if row_ != 1:
            grid_[row_ - 2][column_ - 1].explored = 1
            grid_[row_ - 2][column_].explored = 1
            grid_[row_ - 2][column_ + 1].explored = 1
        if column_ <= COLUMNS - 3:
            grid_[row_ - 1][column_ + 2].explored = 1
            grid_[row_ + 1][column_ + 2].explored = 1
        if column_ - 3 >= 0:
            grid_[row_][column_ - 2].explored = 1
            if grid_[row_][column_ - 2].obstacle != 1:
                grid_[row_][column_ - 3].explored = 1

    elif robot_.direction == "S":
        if row_ != ROWS - 2:
            grid_[row_ + 2][column_ - 1].explored = 1
            grid_[row_ + 2][column_].explored = 1
            grid_[row_ + 2][column_ + 1].explored = 1
        if column_ >= 2:
            grid_[row_ - 1][column_ - 2].explored = 1
            grid_[row_ + 1][column_ - 2].explored = 1
        if column_ + 3 < COLUMNS:
            grid_[row_][column_ + 2].explored = 1
            if grid_[row_][column_ + 2].obstacle != 1:
                grid_[row_][column_ + 3].explored = 1

    elif robot_.direction == "E":
        if column_ != COLUMNS - 2:
            grid_[row_ - 1][column_ + 2].explored = 1
            grid_[row_][column_ + 2].explored = 1
            grid_[row_ + 1][column_ + 2].explored = 1
        if row_ <= ROWS - 3:
            grid_[row_ + 2][column_ - 1].explored = 1
            grid_[row_ + 2][column_ + 1].explored = 1
        if row_ - 3 >= 0:
            grid_[row_ - 2][column_].explored = 1
            if grid_[row_ - 2][column_].obstacle != 1:
                grid_[row_ - 3][column_].explored = 1

    elif robot_.direction == "W":
        if column_ != 1:
            grid_[row_ - 1][column_ - 2].explored = 1
            grid_[row_][column_ - 2].explored = 1
            grid_[row_ + 1][column_ - 2].explored = 1
        if row_ >= 2:
            grid_[row_ - 2][column_ - 1].explored = 1
            grid_[row_ - 2][column_ + 1].explored = 1
        if row_ + 3 < ROWS:
            grid_[row_ + 2][column_].explored = 1
            if grid_[row_ + 2][column_].obstacle != 1:
                grid_[row_ + 3][column_].explored = 1


def check_exploration_status(grid_):
    total_exp_grids = [cell.explored for item in grid_ for cell in item].count(1)
    print('Explored cells:', total_exp_grids)

    # For checking purposes (to be removed once verified code works properly)
    if total_exp_grids >= 280:
        for i in range(ROWS):
            for j in range(COLUMNS):
                if grid_[i][j].explored == 0:
                    print(i, j)

    if total_exp_grids == ROWS * COLUMNS:
        return True

    return False


def update_prev_and_curr_total(grid_, prev_total, curr_total):
    total_exp_grids = [cell.explored for item in grid_ for cell in item].count(1)
    prev_total = curr_total
    curr_total = total_exp_grids

    return prev_total, curr_total


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
        # 180 turn (2 right turns)
        if robot_.direction == "E":
            robot_.direction = "S"
            update_explored_cells(robot_, grid)
            robot_.direction = "W"

        elif robot_.direction == "N":
            robot_.direction = "E"
            update_explored_cells(robot_, grid)
            robot_.direction = "S"

        elif robot_.direction == "W":
            robot_.direction = "N"
            update_explored_cells(robot_, grid)
            robot_.direction = "E"

        elif robot_.direction == "S":
            robot_.direction = "W"
            update_explored_cells(robot_, grid)
            robot_.direction = "N"


def update_robot_dir_left_wall(robot_):
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
        # 180 turn (2 left turns)
        if robot_.direction == "E":
            robot_.direction = "N"
            update_explored_cells(robot_, grid)
            robot_.direction = "W"

        elif robot_.direction == "N":
            robot_.direction = "W"
            update_explored_cells(robot_, grid)
            robot_.direction = "S"

        elif robot_.direction == "W":
            robot_.direction = "S"
            update_explored_cells(robot_, grid)
            robot_.direction = "E"

        elif robot_.direction == "S":
            robot_.direction = "E"
            update_explored_cells(robot_, grid)
            robot_.direction = "N"


def check_right(robot_):
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if column_ != COLUMNS - 2 and check_obs_east(row_, column_) and check_col_right_wall_hug(column_):
            return True

    elif robot_.direction == "S":
        if column_ != 1 and check_obs_west(row_, column_) and check_col_left_wall_hug(column_):
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
        if column_ != COLUMNS - 2 and check_obs_east(row_, column_) and check_col_right_wall_hug(column_):
            return True

    elif robot_.direction == "W":
        if column_ != 1 and check_obs_west(row_, column_) and check_col_left_wall_hug(column_):
            return True

    return False


def check_left(robot_):
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if column_ != 1 and check_obs_west(row_, column_) and check_col_left_wall_hug(column_):
            return True

    elif robot_.direction == "S":
        if column_ != COLUMNS - 2 and check_obs_east(row_, column_) and check_col_right_wall_hug(column_):
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


def check_col_right_wall_hug(column_):
    if col_to_turn == -1 or not right_wall_hug:
        return True

    else:
        if column_ != col_to_turn:
            return True

        return False


def check_col_left_wall_hug(column_):
    if col_to_turn == -1 or right_wall_hug:
        return True

    else:
        if column_ != col_to_turn:
            return True

        return False


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
                cell.explored = 1  # Assuming that this is done when implementation of the real run.
                print("Click ", pos, "Grid coordinates: ", row, column)

            if 460 > pos[0] > 300 and 60 > pos[1] > 40:
                move = True

    if move:
        clock.tick(60)
        update_explored_cells(robot, grid)

        if right_wall_hug:
            update_robot_dir_right_wall(robot)

        else:
            update_robot_dir_left_wall(robot)

        update_explored_cells(robot, grid)
        robot_movement(robot)

        # Each right wall hugging run involves robot returning to starting point
        # Each left wall hugging run involves robot returning to goal point
        # When all cells are explored and robot returns to starting point, end exploration
        if robot.row == TARGET_ROBOT_POS_ROW and robot.column == TARGET_ROBOT_POS_COL:
            col_to_turn = col_to_make_turn(grid)

            if check_exploration_status(grid):
                if TARGET_ROBOT_POS_ROW != 18 or TARGET_ROBOT_POS_COL != 1:
                    col_to_turn = -1
                    TARGET_ROBOT_POS_ROW = 18
                    TARGET_ROBOT_POS_COL = 1

                else:
                    print("Exploration complete.")
                    break

            prev_total, curr_total = update_prev_and_curr_total(grid, prev_total, curr_total)

            # When current run has no new explored cells, change hugging
            if prev_total == curr_total:
                if (TARGET_ROBOT_POS_ROW, TARGET_ROBOT_POS_COL) == (18, 1):
                    right_wall_hug = False
                    robot.direction = "N"
                    TARGET_ROBOT_POS_ROW = 1
                    TARGET_ROBOT_POS_COL = 13
                    print("Switched to left wall hugging.")

                else:
                    right_wall_hug = True
                    robot.direction = "N"
                    TARGET_ROBOT_POS_ROW = 18
                    TARGET_ROBOT_POS_COL = 1
                    print("Switched to right wall hugging.")

            print("Reached target point", TARGET_ROBOT_POS_ROW, TARGET_ROBOT_POS_COL)

    screen.fill(BLACK)

    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE

            if grid[row][column].obstacle == 1:
                color = RED

                for r in range(row - 1, row + 2):
                    for c in range(column - 1, column + 2):
                        if r < 0 or r >= ROWS or c < 0 or c >= COLUMNS:
                            continue

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

    clock.tick(30)
    pygame.display.flip()

pygame.quit()
