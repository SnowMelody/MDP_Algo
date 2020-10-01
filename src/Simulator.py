import pickle

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


def create_grid(rows, columns):
    grid = []
    for row_ in range(rows):
        grid.append([])
        for column_ in range(columns):
            cell = Cell(row_, column_, 0)
            if row_ < 1 or row_ > 18 or column_ < 1 or column_ > 13:
                cell.virtual_wall = 1
            grid[row_].append(cell)  # Append a cell

    return grid


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

    return robot_


def main():
    pygame.init()
    WINDOW_SIZE = [500, 480]
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    font = pygame.font.SysFont("comicsansms", 24)
    text = font.render("GO!", True, (0, 128, 0))
    done = False
    clock = pygame.time.Clock()
    move = False
    grid = create_grid(ROWS, COLUMNS)
    robot = Robot()

    while not done:

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
            clock.tick(60)  # change this value to modify robot's animation speed
            #   robot = robot_movement(robot)
            try:
                dbfile = open('examplePickle', 'rb')
                db = pickle.load(dbfile)
                grid = db['grid']
                robot = db['robot']
            except Exception as e:
                print(e)
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = ORANGE

                if grid[row][column].explored:
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


if __name__ == '__main__':
    main()
