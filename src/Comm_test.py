import json
import socket

ROWS = 20
COLUMNS = 15


class Cell:  # contains cell data for each cell on the grid.
    def __init__(self, row_, column_, explored):
        self.obstacle = 0
        self.virtual_wall = 0
        self.explored = explored
        self.row = row_
        self.column = column_


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


def main():
    grid = create_maze_grid(ROWS, COLUMNS)
    connection = Connection()
    connection.connect_to_rpi()
    s = connection.get_socket_instance()
    mdf_status_update = make_mdf_string(grid)
    connection.send_to_rpi(mdf_status_update.encode('UTF-8'))
    reply = s.recv(1024)
    print(reply)
    connection.close_connection()


def make_mdf_string(grid):
    mdf_exploration = '11'
    mdf_obstacle = ''
    for i in range(ROWS-1, -1, -1):
        for j in range(COLUMNS):
            mdf_exploration = mdf_exploration + str(grid[i][j].explored)
            if grid[i][j].explored == 1:
                mdf_obstacle = mdf_obstacle + str(grid[i][j].obstacle)

    if len(mdf_obstacle) % 8 is not 0:
        dummy = '0'*(8 - (len(mdf_obstacle) % 8))
        mdf_obstacle = dummy + mdf_obstacle

    mdf_exploration = mdf_exploration + '11'
    mdf_exploration_hex = hex(int(mdf_exploration, 2))[2:]
    mdf_obstacle_hex = hex(int(mdf_obstacle, 2))[2:]
    no_of_digits_obs = int(len(mdf_obstacle) / 4)
    mdf_obstacle_hex = "0" * (no_of_digits_obs - len(mdf_obstacle_hex)) + mdf_obstacle_hex
    mdf_json = {'map': {'exploration': mdf_exploration_hex,
                        'obstacle': mdf_obstacle_hex}}
    mdf_json = json.dumps(mdf_json)
    mdf_json = 'a|' + mdf_json

    return mdf_json


if __name__ == "__main__":
    main()
