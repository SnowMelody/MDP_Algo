import json
import pickle
import socket
import numpy as np
from multiprocessing.connection import Client
from fastestpath import search

ROWS = 20
COLUMNS = 15

right_wall_hug = True
col_to_turn = -1


class Cell:  # contains cell data for each cell on the grid.
    def __init__(self, row_, column_, explored):
        self.obstacle = 0
        self.virtual_wall = 0
        self.explored = explored
        self.row = row_
        self.column = column_


class Robot:  # Contains definition of robot pos and direction.
    def __init__(self):
        self.row = 18
        self.column = 1
        self.direction = "E"


class Connection:
    def __init__(self):
        self.socket = 0
        self.host = '192.168.22.1'
        self.port = 9999

    def connect_to_rpi(self):
        self.socket = socket.create_connection((self.host, self.port))
        if socket is not 0:
            print("connected successfully")

    def send_to_rpi(self, message):
        try:
            self.socket.sendall(message)
        except Exception as e:
            print(e)

    def close_connection(self):
        self.socket.close()

    def get_socket_instance(self):
        return self.socket


def parse_sensor_data(sensor_data):  # Takes raw sensor data string and turns it into a python dict.
    sensor_data_list = sensor_data.split(", ")
    sensor_values = {}
    for value in sensor_data_list:
        single_sensor_value = value.split(":")
        if single_sensor_value[0] == 'LL':
            if single_sensor_value[1][0:2] == ' 0':
                sensor_values[single_sensor_value[0]] = 0
            if single_sensor_value[1][0:2] == ' 1':
                sensor_values[single_sensor_value[0]] = 1
            if single_sensor_value[1][0:2] == ' 2':
                sensor_values[single_sensor_value[0]] = 2
        else:
            if single_sensor_value[1][0:2] == ' 0':
                sensor_values[single_sensor_value[0]] = False
            else:
                sensor_values[single_sensor_value[0]] = True

    return sensor_values


def create_maze_grid(rows, columns):  # creates grid and updates it with cell objects. Returns grid list.
    grid_temp = []
    for row in range(rows):
        grid_temp.append([])
        for column in range(columns):
            cell = Cell(row, column, 0)
            if row > 16 and column < 3:
                cell.explored = 1
            if row < 1 or row > 18 or column < 1 or column > 13:
                cell.virtual_wall = 1
            grid_temp[row].append(cell)

    return grid_temp


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


def update_robot_position(robot_):
    if robot_.direction == 'N':
        robot_.row -= 1
    elif robot_.direction == 'S':
        robot_.row += 1
    elif robot_.direction == 'E':
        robot_.column += 1
    elif robot_.direction == 'W':
        robot_.column -= 1
    else:
        pass

    return robot_


def update_explored_cells(robot_, grid_, sensor_data):  # updates the map grid according to sensor data.
    row_ = robot_.row
    column_ = robot_.column
    # Mark 3x3 grid occupied by robot as explored
    for i in range(row_ - 1, row_ + 2):
        for j in range(column_ - 1, column_ + 2):
            grid_[i][j].explored = 1

        # Mark 3 grids directly in front of robot's facing direction as explored (3 front sensors)
        # And 1 front right + 1 back right sensor
        # And 1 long range left sensor
    # Mark 3 grids directly in front of robot's facing direction as explored (3 front sensors)
    # And 1 front right + 1 back right sensor
    # And 1 long range left sensor
    if robot_.direction == "N":
        if row_ != 1:
            if sensor_data['FL']:
                grid_[row_ - 2][column_ - 1].obstacle = 1
            else:
                grid_[row_ - 2][column_ - 1].obstacle = 0
            if sensor_data['FC']:
                grid_[row_ - 2][column_].obstacle = 1
            else:
                grid_[row_ - 2][column_].obstacle = 0
            if sensor_data['FR']:
                grid_[row_ - 2][column_ + 1].obstacle = 1
            else:
                grid_[row_ - 2][column_ + 1].obstacle = 0
            grid_[row_ - 2][column_ - 1].explored = 1
            grid_[row_ - 2][column_].explored = 1
            grid_[row_ - 2][column_ + 1].explored = 1
        if column_ <= COLUMNS - 3:
            if sensor_data['RF']:
                grid_[row_ - 1][column_ + 2].obstacle = 1
            else:
                grid_[row_ - 1][column_ + 2].obstacle = 0
            if sensor_data['RB']:
                grid_[row_ + 1][column_ + 2].obstacle = 1
            else:
                grid_[row_ + 1][column_ + 2].obstacle = 0
            grid_[row_ - 1][column_ + 2].explored = 1
            grid_[row_ + 1][column_ + 2].explored = 1
        if column_ - 3 >= 0:  # adjust this part again based on data format.
            if sensor_data['LL'] == 0:
                grid_[row_ - 1][column_ - 3].explored = 1
                grid_[row_ - 1][column_ - 3].obstacle = 0
                grid_[row_ - 1][column_ - 2].obstacle = 0
            if sensor_data['LL'] == 1:
                grid_[row_ - 1][column_ - 2].obstacle = 1
            elif sensor_data['LL'] == 2:
                grid_[row_ - 1][column_ - 2].obstacle = 1
                grid_[row_ - 1][column_ - 3].explored = 1
            grid_[row_ - 1][column_ - 2].explored = 1
            # if grid_[row_][column_ - 2].obstacle != 1:
            # grid_[row_][column_ - 3].explored = 1
    elif robot_.direction == "S":
        if row_ != ROWS - 2:
            if sensor_data['FL']:
                grid_[row_ + 2][column_ - 1].obstacle = 1
            else:
                grid_[row_ + 2][column_ - 1].obstacle = 0
            if sensor_data['FC']:
                grid_[row_ + 2][column_].obstacle = 1
            else:
                grid_[row_ + 2][column_].obstacle = 0
            if sensor_data['FR']:
                grid_[row_ + 2][column_ + 1].obstacle = 1
            else:
                grid_[row_ + 2][column_ + 1].obstacle = 0
            grid_[row_ + 2][column_ - 1].explored = 1
            grid_[row_ + 2][column_].explored = 1
            grid_[row_ + 2][column_ + 1].explored = 1
        if column_ >= 2:
            if sensor_data['RF']:
                grid_[row_ + 1][column_ - 2].obstacle = 1
            else:
                grid_[row_ + 1][column_ - 2].obstacle = 0
            if sensor_data['RB']:
                grid_[row_ - 1][column_ - 2].obstacle = 1
            else:
                grid_[row_ - 1][column_ - 2].obstacle = 0
            grid_[row_ - 1][column_ - 2].explored = 1
            grid_[row_ + 1][column_ - 2].explored = 1
        if column_ + 3 < COLUMNS:
            if sensor_data['LL'] == 0:
                grid_[row_ + 1][column_ + 3].explored = 1
                grid_[row_ + 1][column_ + 3].obstacle = 0
                grid_[row_ + 1][column_ + 2].obstacle = 0
            if sensor_data['LL'] == 1:
                grid_[row_ + 1][column_ + 2].obstacle = 1
            elif sensor_data['LL'] == 2:
                grid_[row_ + 1][column_ + 3].obstacle = 1
                grid_[row_ + 1][column_ + 3].explored = 1
            grid_[row_ + 1][column_ + 2].explored = 1
            # if grid_[row_][column_ + 2].obstacle != 1:
            #    grid_[row_][column_ + 3].explored = 1
    elif robot_.direction == "E":
        if column_ != COLUMNS - 2:
            if sensor_data['FL']:
                grid_[row_ - 1][column_ + 2].obstacle = 1
            else:
                grid_[row_ - 1][column_ + 2].obstacle = 0
            if sensor_data['FC']:
                grid_[row_][column_ + 2].obstacle = 1
            else:
                grid_[row_][column_ + 2].obstacle = 0
            if sensor_data['FR']:
                grid_[row_ + 1][column_ + 2].obstacle = 1
            else:
                grid_[row_ + 1][column_ + 2].obstacle = 0
            grid_[row_ - 1][column_ + 2].explored = 1
            grid_[row_][column_ + 2].explored = 1
            grid_[row_ + 1][column_ + 2].explored = 1
        if row_ <= ROWS - 3:
            if sensor_data['RF']:
                grid_[row_ + 2][column_ + 1].obstacle = 1
            else:
                grid_[row_ + 2][column_ + 1].obstacle = 0
            if sensor_data['RB']:
                grid_[row_ + 2][column_ - 1].obstacle = 1
            else:
                grid_[row_ + 2][column_ - 1].obstacle = 0
            grid_[row_ + 2][column_ - 1].explored = 1
            grid_[row_ + 2][column_ + 1].explored = 1
        if row_ - 3 >= 0:
            if sensor_data['LL'] == 0:
                grid_[row_ - 3][column_ + 1].explored = 1
                grid_[row_ - 3][column_ + 1].obstacle = 0
                grid_[row_ - 2][column_ + 1].obstacle = 0
            if sensor_data['LL'] == 1:
                grid_[row_ - 2][column_ + 1].obstacle = 1
            elif sensor_data['LL'] == 2:
                grid_[row_ - 3][column_ + 1].obstacle = 1
                grid_[row_ - 3][column_ + 1].explored = 1
            grid_[row_ - 2][column_ + 1].explored = 1

    elif robot_.direction == "W":
        if column_ != 1:
            if sensor_data['FL']:
                grid_[row_ + 1][column_ - 2].obstacle = 1
            else:
                grid_[row_ + 1][column_ - 2].obstacle = 0
            if sensor_data['FC']:
                grid_[row_][column_ - 2].obstacle = 1
            else:
                grid_[row_][column_ - 2].obstacle = 0
            if sensor_data['FR']:
                grid_[row_ - 1][column_ - 2].obstacle = 1
            else:
                grid_[row_ - 1][column_ - 2].obstacle = 0
            grid_[row_ - 1][column_ - 2].explored = 1
            grid_[row_][column_ - 2].explored = 1
            grid_[row_ + 1][column_ - 2].explored = 1
        if row_ >= 2:
            if sensor_data['RF']:
                grid_[row_ - 2][column_ - 1].obstacle = 1
            else:
                grid_[row_ - 2][column_ - 1].obstacle = 0
            if sensor_data['RB']:
                grid_[row_ - 2][column_ + 1].obstacle = 1
            else:
                grid_[row_ - 2][column_ + 1].obstacle = 0
            grid_[row_ - 2][column_ - 1].explored = 1
            grid_[row_ - 2][column_ + 1].explored = 1
        if row_ + 3 < ROWS:
            if sensor_data['LL'] == 0:
                grid_[row_ + 3][column_ - 1].explored = 1
                grid_[row_ + 3][column_ - 1].obstacle = 0
                grid_[row_ + 2][column_ - 1].obstacle = 0
            if sensor_data['LL'] == 1:
                grid_[row_ + 2][column_ - 1].obstacle = 1
            elif sensor_data['LL'] == 2:
                grid_[row_ + 3][column_ - 1].obstacle = 1
                grid_[row_ + 3][column_ - 1].explored = 1
            grid_[row_ + 2][column_ - 1].explored = 1
        #    if grid_[row_ + 2][column_].obstacle != 1:
        #       grid_[row_ + 3][column_].explored = 1
    return grid_


def check_obs_north(grid, row_, column_):
    if (
            grid[row_ - 2][column_].obstacle, grid[row_ - 2][column_ + 1].obstacle,
            grid[row_ - 2][column_ - 1].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_obs_south(grid, row_, column_):
    if (
            grid[row_ + 2][column_].obstacle, grid[row_ + 2][column_ + 1].obstacle,
            grid[row_ + 2][column_ - 1].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_obs_east(grid, row_, column_):  # Checks for obstacles on right of the robot.
    if (
            grid[row_][column_ + 2].obstacle, grid[row_ + 1][column_ + 2].obstacle,
            grid[row_ - 1][column_ + 2].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_obs_west(grid, row_, column_):
    if (
            grid[row_][column_ - 2].obstacle, grid[row_ + 1][column_ - 2].obstacle,
            grid[row_ - 1][column_ - 2].obstacle) == (
            0, 0, 0):
        return True

    return False


def check_col_right_wall_hug(column_):  # responsible for switching from left to right
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


def check_right(grid, robot_):  # Checks if the robot is able to make a right turn.
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if column_ != COLUMNS - 2 and check_obs_east(grid, row_, column_) and check_col_right_wall_hug(column_):
            return True
    elif robot_.direction == "S":
        if column_ != 1 and check_obs_west(grid, row_, column_) and check_col_left_wall_hug(column_):
            return True

    elif robot_.direction == "E":
        if row_ != ROWS - 2 and check_obs_south(grid, row_, column_):
            return True

    elif robot_.direction == "W":
        if row_ != 1 and check_obs_north(grid, row_, column_):
            return True

    return False


def check_forward(grid, robot_):  # Checks if the robot is able to go forward.
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if row_ != 1 and check_obs_north(grid, row_, column_):
            return True

    elif robot_.direction == "S":
        if row_ != ROWS - 2 and check_obs_south(grid, row_, column_):
            return True

    elif robot_.direction == "E":
        if column_ != COLUMNS - 2 and check_obs_east(grid, row_, column_) and check_col_right_wall_hug(column_):
            return True

    elif robot_.direction == "W":
        if column_ != 1 and check_obs_west(grid, row_, column_) and check_col_left_wall_hug(column_):
            return True

    return False


def check_left(grid, robot_):
    row_ = robot_.row
    column_ = robot_.column

    if robot_.direction == "N":
        if column_ != 1 and check_obs_west(grid, row_, column_) and check_col_left_wall_hug(column_):
            return True

    elif robot_.direction == "S":
        if column_ != COLUMNS - 2 and check_obs_east(grid, row_, column_) and check_col_right_wall_hug(column_):
            return True

    elif robot_.direction == "E":
        if row_ != 1 and check_obs_north(grid, row_, column_):
            return True

    elif robot_.direction == "W":
        if row_ != ROWS - 2 and check_obs_south(grid, row_, column_):
            return True

    return False


def update_robot_dir_right_wall(grid, robot_):  # Updates the direction of the robot during right wall hugging.
    robot_status_update_ad_temp = ''
    if check_right(grid, robot_):
        if robot_.direction == "E":
            robot_.direction = "S"
            robot_status_update_ad_temp = 'S'
        elif robot_.direction == "N":
            robot_.direction = "E"
            robot_status_update_ad_temp = 'E'
        elif robot_.direction == "W":
            robot_.direction = "N"
            robot_status_update_ad_temp = 'N'
        elif robot_.direction == "S":
            robot_.direction = "W"
            robot_status_update_ad_temp = 'W'
    elif check_forward(grid, robot_):
        robot_status_update_ad_temp = robot_.direction
    elif check_left(grid, robot_):
        if robot_.direction == "E":
            robot_.direction = "N"
            robot_status_update_ad_temp = "N"

        elif robot_.direction == "N":
            robot_.direction = "W"
            robot_status_update_ad_temp = "W"

        elif robot_.direction == "W":
            robot_.direction = "S"
            robot_status_update_ad_temp = "S"

        elif robot_.direction == "S":
            robot_.direction = "E"
            robot_status_update_ad_temp = "E"
    else:
        if robot_.direction == "E":
            robot_.direction = "W"
            robot_status_update_ad_temp = "W"
        elif robot_.direction == "N":
            robot_.direction = "S"
            robot_status_update_ad_temp = "S"
        elif robot_.direction == "S":
            robot_.direction = "N"
            robot_status_update_ad_temp = "N"
        else:
            robot_.direction = "E"
            robot_status_update_ad_temp = "E"

    return robot_, robot_status_update_ad_temp


def update_robot_dir_left_wall(grid, robot_):
    robot_status_update_ad_temp = ''
    if check_left(grid, robot_):
        if robot_.direction == "E":
            robot_.direction = "N"
            robot_status_update_ad_temp = 'N'

        elif robot_.direction == "N":
            robot_.direction = "W"
            robot_status_update_ad_temp = 'W'

        elif robot_.direction == "W":
            robot_.direction = "S"
            robot_status_update_ad_temp = 'S'

        elif robot_.direction == "S":
            robot_.direction = "E"
            robot_status_update_ad_temp = 'E'
    elif check_forward(grid, robot_):
        robot_status_update_ad_temp = robot_.direction

    elif check_right(grid, robot_):
        if robot_.direction == "E":
            robot_.direction = "S"
            robot_status_update_ad_temp = 'S'

        elif robot_.direction == "N":
            robot_.direction = "E"
            robot_status_update_ad_temp = 'E'

        elif robot_.direction == "W":
            robot_.direction = "N"
            robot_status_update_ad_temp = 'N'

        elif robot_.direction == "S":
            robot_.direction = "W"
            robot_status_update_ad_temp = 'W'

    else:
        # 180 turn (2 left turns)
        if robot_.direction == "E":
            robot_.direction = "W"
            robot_status_update_ad_temp = 'W'

        elif robot_.direction == "N":
            robot_.direction = "S"
            robot_status_update_ad_temp = 'S'

        elif robot_.direction == "W":
            robot_.direction = "E"
            robot_status_update_ad_temp = 'E'

        elif robot_.direction == "S":
            robot_.direction = "N"
            robot_status_update_ad_temp = 'N'

    return robot_, robot_status_update_ad_temp


def send_data_simulator(grid, robot_):
    db = {'robot': robot_, 'grid': grid}
    dbfile = open('grid_file', 'wb')
    # source, destination
    pickle.dump(db, dbfile)
    dbfile.close()


def make_mdf_string(grid, robot):
    mdf_exploration = '11'
    mdf_obstacle = ''
    temp_debug = []
    for i in range(ROWS - 1, -1, -1):
        temp_debug.append([])
        for j in range(COLUMNS):
            mdf_exploration = mdf_exploration + str(grid[i][j].explored)
            if grid[i][j].explored == 1:
                temp_debug[ROWS - i - 1].append(1)
                mdf_obstacle = mdf_obstacle + str(grid[i][j].obstacle)

    if len(mdf_obstacle) % 8 is not 0:
        dummy = '0' * (8 - (len(mdf_obstacle) % 8))
        mdf_obstacle = mdf_obstacle + dummy

    mdf_exploration = mdf_exploration + '11'
    mdf_exploration_hex = hex(int(mdf_exploration, 2))[2:].rstrip('L')
    mdf_obstacle_hex = hex(int(mdf_obstacle, 2))[2:].rstrip('L')
    no_of_digits_obs = int(len(mdf_obstacle) / 4)
    mdf_obstacle_hex = "0" * (no_of_digits_obs - len(mdf_obstacle_hex)) + mdf_obstacle_hex
    mdf_json = {'map': {'exploration': mdf_exploration_hex,
                        'obstacle': mdf_obstacle_hex,
                        'robotPos': [robot.column, robot.row, robot.direction]}}
    mdf_json = json.dumps(mdf_json)
    mdf_json = 'a|' + mdf_json

    return mdf_json


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


def update_prev_and_curr_total(grid_, curr_total):
    total_exp_grids = [cell.explored for item in grid_ for cell in item].count(1)
    prev_total = curr_total
    curr_total = total_exp_grids

    return prev_total, curr_total


def fastest_path(grid_, waypoint):
    maze = [[0 for j in range(COLUMNS)] for i in range(ROWS)]

    for row in range(ROWS):
        for column in range(COLUMNS):
            if grid_[row][column].obstacle:
                for r in range(row - 1, row + 2):
                    for c in range(column - 1, column + 2):
                        if r < 0 or r >= ROWS or c < 0 or c >= COLUMNS:
                            continue

                        if grid_[r][c].obstacle == 0:
                            grid_[r][c].virtual_wall = 1

    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid_[i][j].obstacle:
                maze[i][j] = 1
            if grid_[i][j].virtual_wall:
                maze[i][j] = 2
            grid_[i][j].explored = 1

    path = search(maze, 1, [18, 1], waypoint)
    path += search(maze, 1, waypoint, [1, 13])[1:]

    movement = ''
    for i in range(len(path)):
        if i == 0:
            count = 0
        elif path[i-1][1] == path[i][1]:
            count += 1
        else:
            movement += str(count) + path[i-1][1]
            count = 0
    movement += str(count) + path[i-1][1]

    return movement


def main():
    target_robot_pos_row = 18
    target_robot_pos_col = 1
    exploration_done = False
    fastest_eligible = False
    # conn = Client(('localhost', 6000), authkey=b'secret password')
    global col_to_turn, right_wall_hug
    prev_explored_total, curr_explored_total = 0, 0
    connection_rpi = Connection()
    connection_rpi.connect_to_rpi()
    robot = Robot()
    grid = create_maze_grid(ROWS, COLUMNS)

    while exploration_done is not True:
        sensor_readings_ad = connection_rpi.get_socket_instance().recv(1024)
        sensor_readings_ad = sensor_readings_ad.decode('UTF-8')
        print(sensor_readings_ad)
        if sensor_readings_ad == "begin fastest" and fastest_eligible is True:
            fast_path = fastest_path(grid)
           # TODO: send the fastest path to rpi
        else:
            sensor_data = parse_sensor_data(sensor_readings_ad)
            grid = update_explored_cells(robot, grid, sensor_data)
        if right_wall_hug:
            robot, robot_status_update = update_robot_dir_right_wall(grid, robot)
        else:
            robot, robot_status_update = update_robot_dir_left_wall(grid, robot)

        robot = update_robot_position(robot)

        # Each right wall hugging run involves robot returning to starting point
        # Each left wall hugging run involves robot returning to goal point
        # When all cells are explored and robot returns to starting point, end exploration
        if robot.row == target_robot_pos_row and robot.column == target_robot_pos_col:
            col_to_turn = col_to_make_turn(grid)
            if check_exploration_status(grid):
                if target_robot_pos_row != 18 or target_robot_pos_col != 1:
                    col_to_turn = -1
                    target_robot_pos_row = 18
                    target_robot_pos_col = 1

                else:
                    exploration_done = True
                    print("Exploration complete.")
                    fastest_eligible = True

            prev_explored_total, curr_explored_total = update_prev_and_curr_total(grid, curr_explored_total)
            if prev_explored_total == curr_explored_total:
                if (target_robot_pos_row, target_robot_pos_col) == (18, 1):
                    right_wall_hug = False
                    robot.direction = "N"
                    robot_status_update = 'N'
                    target_robot_pos_row = 1
                    target_robot_pos_col = 13
                    print("Switched to left wall hugging.")
                    robot = update_robot_position(robot)

                else:
                    right_wall_hug = True
                    robot.direction = "N"
                    robot_status_update = 'N'
                    target_robot_pos_row = 18
                    target_robot_pos_col = 1
                    print("Switched to right wall hugging.")
                    robot = update_robot_position(robot)

        robot_status_update_formatted = 'h|' + robot_status_update + '|a|' + robot_status_update
        mdf_status_update = make_mdf_string(grid, robot)

        print(robot.row, robot.column)

        #  conn.send([grid, robot])
        send_data_simulator(grid, robot)
        connection_rpi.send_to_rpi(robot_status_update_formatted.encode('UTF-8'))
        connection_rpi.send_to_rpi((mdf_status_update.encode('UTF-8')))


if __name__ == '__main__':
    main()