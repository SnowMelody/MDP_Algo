import numpy as np
import json

class Node:
    """
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None, direction='N'):
        self.parent = parent
        self.position = position
        self.direction = direction

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

#This function return the path of the search
def return_path(current_node,maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    # here we create the initialized result maze with -1 in every position
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append([current.position, current.direction])
        prev = current
        current = current.parent
        if current is not None:
            if prev.direction != current.direction:
                path.append([current.position, prev.direction])
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    return path

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


def search(maze, cost, start, end):

    # Create start and end node with initized values for g, h and f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yet_to_visit_list = []  
    # in this list we will put all node those already explored so that we don't explore it again
    visited_list = [] 
    
    # Add the start node
    yet_to_visit_list.append(start_node)
    
    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # what squares do we search . serarch movement is left-right-top-bottom 
    #(4 movements) from every positon

    move  =  [[-1, 0, 'N'], # go up
              [0, -1, 'W'], # go left
              [1, 0, 'S'], # go down
              [0, 1, 'E']] # go right

    #find maze has got how many rows and columns 
    no_rows, no_columns = np.shape(maze)
    
    # Loop until you find the end
    
    while len(yet_to_visit_list) > 0:
        
        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1    

        
        # Get the current node
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print ("giving up on pathfinding too many iterations")
            return return_path(current_node,maze)

        # Pop current node out off yet_to_visit list, add to visited list
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            return return_path(current_node,maze)

        # Generate children from all adjacent squares
        children = []

        for new_position in move: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range (check if within maze boundary)
            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position, new_position[2])

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            turn = 0
            if current_node.direction == 'N':
                if child.direction == 'S':
                    turn = 2
                elif child.direction == 'E' or child.direction == 'W':
                    turn = 1
            elif current_node.direction == 'S':
                if child.direction == 'N':
                    turn = 2
                elif child.direction == 'E' or child.direction == 'W':
                    turn = 1
            elif current_node.direction == 'E':
                if child.direction == 'W':
                    turn = 2
                elif child.direction == 'N' or child.direction == 'S':
                    turn = 1
            elif current_node.direction == 'W':
                if child.direction == 'E':
                    turn = 2
                elif child.direction == 'N' or child.direction == 'S':
                    turn = 1

            # Child is on the visited list (search entire visited list)
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost + 2 * turn * cost
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            if (child.position[0] - end_node.position[0] != 0) or (child.position[1] - end_node.position[1] != 0):
                child.h += 2 * cost

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and g cost is already lower
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # Add the child to the yet_to_visit list
            yet_to_visit_list.append(child)


if __name__ == '__main__':

    maze = [[2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2],
            [2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 2, 1, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 2, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 1],
            [2, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2],
            [2, 1, 2, 0, 0, 2, 1, 1, 2, 0, 0, 0, 0, 0, 2],
            [2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 2],
            [2, 0, 2, 1, 1, 1, 2, 0, 0, 0, 2, 1, 2, 0, 2],
            [2, 0, 2, 2, 2, 1, 2, 0, 0, 0, 2, 1, 2, 0, 2],
            [2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 1, 2, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
    
    start = [18, 1] # starting position
    end = [1,13] # ending position
    cost = 1 # cost per movement

    connection_rpi = Connection()
    connection_rpi.connect_to_rpi()

    path = search(maze, cost, start, end)
    print(path)
    movement = []
    for i in range(len(path)):
        if i == 0:
            count = 0
        elif path[i-1][1] == path[i][1]:
            count += 1
        else:
            movement.append([count, path[i-1][1]])
            count = 0
    movement.append([count, path[-1][1]])

    for i in movement:
        movement_json = {'map': {'steps': i[0],
                        'direction': i[1]}}
        movement_json = json.dumps(movement_json)
        movement_json = 'a|' + movement_json
        connection_rpi.send_to_rpi((movement_json.encode('UTF-8')))