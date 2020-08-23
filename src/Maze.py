# This script creates a grid with 20x15 cells.


import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

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
        self.explored = explored
        self.row = row_
        self.column = column_


# Grid is an array of cells of the maze.
grid = []

for row in range(ROWS):
    grid.append([])
    for column in range(COLUMNS):
        cell = Cell(row, column, 0)

        grid[row].append(cell)  # Append a cell

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
            cell = grid[row][column]
            cell.obstacle = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    screen.fill(BLACK)

    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE
            if grid[row][column].obstacle == 1:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
