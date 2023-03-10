import queue
import pickle
import math
import random
import heapq

class astar:
    def __init__(self, mat):
        self.mat = mat
        self.moves = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        self.cost = {}
        self.path = []

    def print_path(self, parent, end):
        if parent[end] is None:
            self.path.append(end)
            return
        self.print_path(parent, parent[end])
        self.path.append(end)

    def heuristic(self, curr, end):
        return math.sqrt(((curr[0] - end[0]) ** 2) + ((curr[1] - end[1]) ** 2))

    def algo(self, start, end, algorithm='a'):
        cost = {}
        parent = {}
        visited = set()
        pq = [(0, self.mat[start[0]][start[1]], start)]
        cost[start] = self.mat[start[0]][start[1]]
        parent[start] = None
        while len(pq) > 0:
            node = heapq.heappop(pq)
            # if cost.get(node[2]):
            #     if node[1]>cost.get(node[2]):
            #         continue
            if node[2] == end:
                self.print_path(parent, end)
                return self.path
            if node[2] in visited:
                continue
            visited.add(node[2])

            for move in self.moves:
                curr = (node[2][0] + move[0], node[2][1] + move[1])
                if curr[0] < 0 or curr[1] < 0 or curr[0] > 24 or curr[1] > 24 or curr in visited:
                    continue
                cost_to_curr = cost[node[2]] + self.mat[curr[0]][curr[1]]
                curr_cost = cost.get(curr)
                if not curr_cost or curr_cost > cost_to_curr:
                    cost[curr] = cost_to_curr
                    parent[curr] = node[2]
                    curr_priority = self.heuristic(curr, end) + cost_to_curr if algorithm == 'a' else self.heuristic(
                        curr, end)
                    heapq.heappush(pq, (curr_priority, cost_to_curr, curr))


def dfs(matrix, row, col):
    path = []
    visited = set()
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    matrix[row][col] = 99

    def helper(row, col, search_for=100):
        if (row, col) in visited or matrix[row][col] == -100:
            return False

        if matrix[row][col] == search_for:
            path.append((row, col))
            return True
        visited.add((row, col))
        path.append((row, col))

        for r, c in directions:
            if helper(row + r, col + c, search_for):
                return True
        # visited.remove((row, col))
        path.pop()
        return False

    helper(row, col)
    if len(path) == 0:
        visited = set()
        helper(row, col, 0)
    return path[1:][::-1]


def bfs(matrix, row, col, to_search=100):
    # for row in matrix:
    #     print(*row)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    path = []
    q = queue.Queue()
    parent = {}
    visited = set()
    q.put((row, col))
    ro, co = None, None
    while not q.empty():
        ro, co = q.get()
        curr = (ro, co)
        # print(curr)
        if curr in visited or matrix[ro][co] == -100:
            continue
        if matrix[ro][co] == to_search:
            break
        visited.add(curr)
        for r, c in directions:
            to_visit = (ro + r, co + c)
            if to_visit in visited or matrix[to_visit[0]][to_visit[1]] == -100: continue
            q.put(to_visit)
            parent[to_visit] = curr
            if matrix[ro + r][co + c] == to_search:
                break
    else:
        if to_search == 100:
            return bfs(matrix, row, col, 0)
        else: return []
    while (ro, co) != (row, col):
        # print(ro,co)
        path.append((ro, co))
        ro, co = parent[(ro, co)]
    # if len(path) == 0 and to_search == 100:

    return path


def neat_shortvision(vision, distance_from_food, row, col, cube):
    net = pickle.load(open(r"C:\Users\Admin\Desktop\Misc\snake winners\winner1.pkl", 'rb'))
    output = net.activate(
        (*distance_from_food, *vision))
    moves = ["forward", "right", "left"]
    direction = moves[output.index(max(output))]
    if direction == "right":
        if cube.up:
            cube.x_vel = 1
            cube.y_vel = 0
            cube.up = False
            cube.left = False
            cube.right = True
            cube.down = False
        elif cube.right:
            cube.x_vel = 0
            cube.y_vel = 1
            cube.up = False
            cube.left = False
            cube.right = False
            cube.down = True
        elif cube.down:
            cube.x_vel = -1
            cube.y_vel = 0
            cube.up = False
            cube.left = True
            cube.right = False
            cube.down = False
        elif cube.left:
            cube.x_vel = 0
            cube.y_vel = -1
            cube.up = True
            cube.left = False
            cube.right = False
            cube.down = False
    elif direction == "left":
        if cube.down:
            cube.x_vel = 1
            cube.y_vel = 0
            cube.up = False
            cube.left = False
            cube.right = True
            cube.down = False
        elif cube.left:
            cube.x_vel = 0
            cube.y_vel = 1
            cube.up = False
            cube.left = False
            cube.right = False
            cube.down = True
        elif cube.up:
            cube.x_vel = -1
            cube.y_vel = 0
            cube.up = False
            cube.left = True
            cube.right = False
            cube.down = False
        elif cube.right:
            cube.x_vel = 0
            cube.y_vel = -1
            cube.up = True
            cube.left = False
            cube.right = False
            cube.down = False

    if cube.x_vel != 0:
        col += cube.x_vel * 20
    else:
        row += cube.y_vel * 20
    return [(row//20, col//20)]

def neat_long_vision(vision, distance_from_food, row, col, cube, file):
    net = pickle.load(open(file, 'rb'))
    output = net.activate(
        (*distance_from_food, *vision))
    moves = ["forward", "right", "left"]
    direction = moves[output.index(max(output))]
    # print(direction)
    if direction == "right":
        if cube.up:
            cube.x_vel = 1
            cube.y_vel = 0
            cube.up = False
            cube.left = False
            cube.right = True
            cube.down = False
        elif cube.right:
            cube.x_vel = 0
            cube.y_vel = 1
            cube.up = False
            cube.left = False
            cube.right = False
            cube.down = True
        elif cube.down:
            cube.x_vel = -1
            cube.y_vel = 0
            cube.up = False
            cube.left = True
            cube.right = False
            cube.down = False
        elif cube.left:
            cube.x_vel = 0
            cube.y_vel = -1
            cube.up = True
            cube.left = False
            cube.right = False
            cube.down = False
    elif direction == "left":
        if cube.down:
            cube.x_vel = 1
            cube.y_vel = 0
            cube.up = False
            cube.left = False
            cube.right = True
            cube.down = False
        elif cube.left:
            cube.x_vel = 0
            cube.y_vel = 1
            cube.up = False
            cube.left = False
            cube.right = False
            cube.down = True
        elif cube.up:
            cube.x_vel = -1
            cube.y_vel = 0
            cube.up = False
            cube.left = True
            cube.right = False
            cube.down = False
        elif cube.right:
            cube.x_vel = 0
            cube.y_vel = -1
            cube.up = True
            cube.left = False
            cube.right = False
            cube.down = False

    if cube.x_vel != 0:
        col += cube.x_vel * 20
    else:
        row += cube.y_vel * 20
    return [(row//20, col//20)]


def a_star(matrix, row, col, foodrow, foodcol):
    new_matrix = [[0] * 25 for i in range(25)]
    for i in range(25):
        for j in range(25):
            new_matrix[i][j] = float('inf') if matrix[i][j] == -100 else 0
    algorithm = astar(new_matrix)
    ans = algorithm.algo((row, col), (foodrow, foodcol))[::-1]
    if len(ans) > 0:
        ans.pop()
    if len(ans) == 0:
        return bfs(matrix, row, col, 0)
    for r,c in ans:
        if matrix[r][c] == -100:
            return bfs(matrix, row, col, 0)
    return ans


if __name__ == "__main__":
    matrix = [[0] * 25 for i in range(25)]
    for i in range(13):
        for j in range(13):
            if i == 0 or i == 12 or j == 0 or j == 12:
                matrix[i][j] = -100
    # for i in range(12):
    #     matrix[4][i] = -100
    # matrix[3][1] = 100

