def dfs(g, stack, a):
    visited = [False]*(r*c)
    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)] # D, L, U, R (highest priority)
    
    while stack:
        V, cx, cy = stack.pop()

        # add edges of current node explored
        # show order which nodes are visited
        if not visited[V]:
            addEdge(g, V, a)
            print(V)
            
        visited[V] = True

        for dx, dy in dirs:
            for i in g[V]:
                if not visited[i] and cx+dx == i%c and cy+dy == i//c:
                    stack.append((i, cx+dx, cy+dy))

        #print(stack)

    return 


def addEdge(g, V, a):
    u = V

    if V + c < n and a[V+c] != 'x' and (V + c) not in g[u]:
        g[u].append(V+c)
        g[V+c].append(u)

    if V - c >= 0 and a[V-c] != 'x' and (V - c) not in g[u]:
        g[u].append(V-c)
        g[V-c].append(u)

    if (V+1)%c != 0 and a[V+1] != 'x' and (V + 1) not in g[u]:
        g[u].append(V+1)
        g[V+1].append(u)

    if (V-1)%c != c-1 and a[V-1] != 'x' and (V - 1) not in g[u]:
        g[u].append(V-1)
        g[V-1].append(u)
    
    return


# Test 1
r, c = 3, 3
n = 9
g = [[] for i in range(n)]


# array (world detected by sensors) -> nodes 4 and 6 are walls
a = ['o', 'o', 'o', 'o', 'x', 'o', 'x', 'o', 'o']

# stack -> push starting pos (node, x, y)
stack = [(0, 0, 0)]
dfs(g, stack, a)
print(g)


# Test 2
'''
r, c = 5, 5
n = 25
g = [[] for i in range(n)]
a = ['o', 'o', 'o', 'x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x', 'x', 'o', 'x', 'x', 'o', 'o', 'o', 'o', 'o', 'o', 'x', 'x', 'o']

stack = [(0, 0, 0)]
dfs(g, stack, a)
print(g)
'''


"""
-- Test 1 explanation -- 

Node order:
6|7|8
3|4|5
0|1|2

Coordinates order:
(0,2)|(1,2)|(2,2)
(0,1)|(1,1)|(2,1)
(0,0)|(1,0)|(2,0)

World: (x = wall, o = path)
x|o|o
o|x|o
o|o|o


-- Test 2 explanation --

Node order:
20|21|22|23|24
15|16|17|18|19
10|11|12|13|14
5 |6 |7 |8 |9
0 |1 |2 |3 |4

Coordinates order:
(0,4)|(1,4)|(2,4)|(3,4)|(4,4)
(0,3)|(1,3)|(2,3)|(3,3)|(4,3)
(0,2)|(1,2)|(2,2)|(3,2)|(4,2)
(0,1)|(1,1)|(2,1)|(3,1)|(4,1)
(0,0)|(1,0)|(2,0)|(3,0)|(4,0)

World: (x = wall, o = path)
o|o|x|x|o
x|o|o|o|o
o|x|x|o|x
o|o|o|o|o
o|o|o|x|o

To modify, change values of r (rows), c (columns), n (num of nodes), a (world)
All nodes are connected to adjacent nodes by edges
Adjacent nodes added to stack in order of priority (can be changed): Right, Up, Left, Down

Assumptions:
Edges are added dynamically -> edges are only known when on current node
Sensors have perfect detection -> when on current node, all edges in hor/ver dirs of that node are added (taking into account walls)

TODO:
- Extend robot occupancy grid to 3x3
- visited[V] to string seq of 0 and 1
- Store backtracking steps of dfs -> currently only node order visited shown
- Implement UI -> Map dfs w/ backtracking steps to animated simulation
"""
