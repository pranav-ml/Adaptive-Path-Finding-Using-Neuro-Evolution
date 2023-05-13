import pygame
import random
import neat
import os
import math
import pickle
from algorithms import *
import copy
import os


max_score = 0


class grid():
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, win):
        for width in range(0, 502, 20):
            pygame.draw.line(win, (255, 255, 255), (self.x + width, self.y), (self.x + width, self.y + 500))
            pygame.draw.line(win, (255, 255, 255), (self.x, self.y + width), (self.x + 500, self.y + width))
            pygame.draw.rect(win, (255, 255, 255), (0,0,280,20))
            pygame.draw.rect(win, (255, 255, 255), (0, 0, 20, 280))
            pygame.draw.rect(win, (255, 255, 255), (0, 260, 280, 20))
            pygame.draw.rect(win, (255, 255, 255), (260, 0, 20, 280))

def neat_full_vision(row, col, *args):
    def prim_maze_generator(grid_rows, grid_columns, start_row, start_col):

        directions = dict()
        vertices = grid_rows * grid_columns

        # Creates keys for the directions dictionary
        # Note that the maze has half the width and length of the grid for the hamiltonian cycle
        for i in range(grid_rows):
            for j in range(grid_columns):
                directions[j, i] = []

        # The initial cell for maze generation is chosen randomly
        x = randint(0, grid_columns - 1)
        y = randint(0, grid_rows - 1)
        initial_cell = (x, y)

        current_cell = initial_cell

        # Stores all cells that have been visited
        visited = [initial_cell]

        # Contains all neighbouring cells to cells that have been visited
        adjacent_cells = set()

        # Generates walls in grid randomly to create a randomized maze
        while len(visited) != vertices:

            # Stores the position of the current cell in the grid
            x_position = current_cell[0]
            y_position = current_cell[1]

            # Finds adjacent cells when the current cell does not lie on the edge of the grid
            if x_position != 0 and y_position != 0 and x_position != grid_columns - 1 and y_position != grid_rows - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the left top corner of the grid
            elif x_position == 0 and y_position == 0:
                adjacent_cells.add((x_position + 1, y_position))
                adjacent_cells.add((x_position, y_position + 1))

            # Finds adjacent cells when the current cell lies in the bottom left corner of the grid
            elif x_position == 0 and y_position == grid_rows - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the left column of the grid
            elif x_position == 0:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the top right corner of the grid
            elif x_position == grid_columns - 1 and y_position == 0:
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))

            # Finds adjacent cells when the current cell lies in the bottom right corner of the grid
            elif x_position == grid_columns - 1 and y_position == grid_rows - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position - 1, y_position))

            # Finds adjacent cells when the current cell lies in the right column of the grid
            elif x_position == grid_columns - 1:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))

            # Finds adjacent cells when the current cell lies in the top row of the grid
            elif y_position == 0:
                adjacent_cells.add((x_position, y_position + 1))
                adjacent_cells.add((x_position - 1, y_position))
                adjacent_cells.add((x_position + 1, y_position))

            # Finds adjacent cells when the current cell lies in the bottom row of the grid
            else:
                adjacent_cells.add((x_position, y_position - 1))
                adjacent_cells.add((x_position + 1, y_position))
                adjacent_cells.add((x_position - 1, y_position))

            # Generates a wall between two cells in the grid
            while current_cell:

                current_cell = (adjacent_cells.pop())

                # The neighbouring cell is disregarded if it is already a wall in the maze
                if current_cell not in visited:

                    # The neighbouring cell is now classified as having been visited
                    visited.append(current_cell)
                    x = current_cell[0]
                    y = current_cell[1]

                    # To generate a wall, a cell adjacent to the current cell must already have been visited
                    # The direction of the wall between cells is stored
                    # The process is simplified by only considering a wall to be to the right or down
                    if (x + 1, y) in visited:
                        directions[x, y] += ['right']
                    elif (x - 1, y) in visited:
                        directions[x - 1, y] += ['right']
                    elif (x, y + 1) in visited:
                        directions[x, y] += ['down']
                    elif (x, y - 1) in visited:
                        directions[x, y - 1] += ['down']

                    break

        # Provides the hamiltonian cycle generating algorithm with the direction of the walls to avoid
        return hamiltonian_cycle(grid_rows, grid_columns, directions, start_row, start_col)

    def hamiltonian_cycle(grid_rows, grid_columns, orientation, start_row, start_col):

        # The path for the snake is stored in a dictionary
        # The keys are the (x, y) positions in the grid
        # The values are the adjacent (x, y) positions that the snake can travel towards
        hamiltonian_graph = dict()

        # Uses the coordinates of the walls to generate available adjacent cells for each cell
        # Simplified by only considering the right and down directions
        for i in range(grid_rows):
            for j in range(grid_columns):

                # Finds available adjacent cells if current cell does not lie on an edge of the grid
                if j != grid_columns - 1 and i != grid_rows - 1 and j != 0 and i != 0:
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                        if (j * 2 + 1, i * 2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' not in orientation[j, i - 1]:
                        hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    if 'right' not in orientation[j - 1, i]:
                        if (j * 2, i * 2) in hamiltonian_graph:
                            hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                        else:
                            hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

                # Finds available adjacent cells if current cell is in the bottom right corner
                elif j == grid_columns - 1 and i == grid_rows - 1:
                    hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' not in orientation[j, i - 1]:
                        hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    elif 'right' not in orientation[j - 1, i]:
                        hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

                # Finds available adjacent cells if current cell is in the top right corner
                elif j == grid_columns - 1 and i == 0:
                    hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'right' not in orientation[j - 1, i]:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]

                # Finds available adjacent cells if current cell is in the right column
                elif j == grid_columns - 1:
                    hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' not in orientation[j, i - 1]:
                        hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    if 'right' not in orientation[j - 1, i]:
                        if (j * 2, i * 2) in hamiltonian_graph:
                            hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                        else:
                            hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

                # Finds available adjacent cells if current cell is in the top left corner
                elif j == 0 and i == 0:
                    hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                        if (j * 2 + 1, i * 2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]

                # Finds available adjacent cells if current cell is in the bottom left corner
                elif j == 0 and i == grid_rows - 1:
                    hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]
                    hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' not in orientation[j, i - 1]:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2 + 1, i * 2)]

                # Finds available adjacent cells if current cell is in the left corner
                elif j == 0:
                    hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                        if (j * 2 + 1, i * 2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' not in orientation[j, i - 1]:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2 + 1, i * 2)]

                # Finds available adjacent cells if current cell is in the top row
                elif i == 0:
                    hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' in orientation[j, i]:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2, i * 2 + 2)]
                        if (j * 2 + 1, i * 2 + 1) in hamiltonian_graph:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] += [(j * 2 + 1, i * 2 + 2)]
                        else:
                            hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 1, i * 2 + 2)]
                    else:
                        hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'right' not in orientation[j - 1, i]:
                        hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]

                # Finds available adjacent cells if current cell is in the bottom row
                else:
                    hamiltonian_graph[j * 2, i * 2 + 1] = [(j * 2 + 1, i * 2 + 1)]
                    if 'right' in orientation[j, i]:
                        hamiltonian_graph[j * 2 + 1, i * 2 + 1] = [(j * 2 + 2, i * 2 + 1)]
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 2, i * 2)]
                    else:
                        hamiltonian_graph[j * 2 + 1, i * 2] = [(j * 2 + 1, i * 2 + 1)]
                    if 'down' not in orientation[j, i - 1]:
                        hamiltonian_graph[j * 2, i * 2] = [(j * 2 + 1, i * 2)]
                    if 'right' not in orientation[j - 1, i]:
                        if (j * 2, i * 2) in hamiltonian_graph:
                            hamiltonian_graph[j * 2, i * 2] += [(j * 2, i * 2 + 1)]
                        else:
                            hamiltonian_graph[j * 2, i * 2] = [(j * 2, i * 2 + 1)]

        # Provides the coordinates of available adjacent cells to generate directions for the snake's movement
        return path_generator(hamiltonian_graph, grid_rows * grid_columns * 4, start_row, start_col)

    def path_generator(graph, cells, start_row, start_col):

        # The starting position for the path is at cell (0, 0)
        path = [(start_row, start_col)]

        previous_cell = path[0]
        previous_direction = None

        # Generates a path that is a hamiltonian cycle by following a set of general laws
        # 1. If the right cell is available, travel to the right
        # 2. If the cell underneath is available, travel down
        # 3. If the left cell is available, travel left
        # 4. If the cell above is available, travel up
        # 5. The current direction cannot oppose the previous direction (e.g. left --> right)
        while len(path) != cells:

            if previous_cell in graph and (previous_cell[0] + 1, previous_cell[1]) in graph[previous_cell] \
                    and previous_direction != 'left':
                path.append((previous_cell[0] + 1, previous_cell[1]))
                previous_cell = (previous_cell[0] + 1, previous_cell[1])
                previous_direction = 'right'
            elif previous_cell in graph and (previous_cell[0], previous_cell[1] + 1) in graph[previous_cell] \
                    and previous_direction != 'up':
                path.append((previous_cell[0], previous_cell[1] + 1))
                previous_cell = (previous_cell[0], previous_cell[1] + 1)
                previous_direction = 'down'
            elif (previous_cell[0] - 1, previous_cell[1]) in graph \
                    and previous_cell in graph[
                previous_cell[0] - 1, previous_cell[1]] and previous_direction != 'right':
                path.append((previous_cell[0] - 1, previous_cell[1]))
                previous_cell = (previous_cell[0] - 1, previous_cell[1])
                previous_direction = 'left'
            else:
                path.append((previous_cell[0], previous_cell[1] - 1))
                previous_cell = (previous_cell[0], previous_cell[1] - 1)
                previous_direction = 'up'

        # Returns the coordinates of the hamiltonian cycle path
        return path

    if args[-1] == "winner_full_vision.pkl":
        ans = prim_maze_generator(6,6, row-1, col-1)
        path = []
        for r,c in reversed(ans):
            path.append((r+1, c+1))
        path.pop()
        return path
    else:
        distance_from_food = [i for i in range(96)]
        vision = [i for i in range(100)]
        net = pickle.load(open("winner_full_vision.pkl", 'rb'))
        output = net.activate((*distance_from_food, *vision))


class cube():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up = False
        self.left = False
        self.right = False
        self.down = True
        self.x_vel = 0
        self.y_vel = 1
        self.path = []

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 255), (self.x, self.y, 19, 19))


class head():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 19, 19))


class food():
    def __init__(self):
        self.x = random.randrange(21, 242, 20)
        self.y = random.randrange(21, 242, 20)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, 19, 19))

class game():
    def __init__(self, algorithm, file = "winner.pkl"):
        # self.genome = genome
        self.file = file
        self.gr = grid()
        self.run = True
        self.cube = cube(201,201)
        self.body = [head(self.cube.x,self.cube.y-20)]
        self.food = food()
        self.score = 0
        self.gamedecider = 0
        self.win = pygame.display.set_mode((800, 501))
        self.sfont = pygame.font.SysFont("comicsans", 30, True)
        self.moves = ["forward", "right", "left"]
        self.moves_left = 200
        # self.genome_to_display = genome_to_display
        self.board = [[0] * 25 for _ in range(25)]
        self.algorithm = algorithm
        self.update_board(False)

    def update_board(self, toprint):
        # print(cube.y//20, cube.x//20)
        for y, row in enumerate(self.board):
            for x in range(25):
                row[x] = -100 if y == 0 or x == 0 or y == 13 or x == 13 else 0

        # self.board[self.cube.y // 20][self.cube.x // 20] = 100
        self.board[self.food.y // 20][self.food.x // 20] = 100
        for sq in self.body:
            self.board[sq.y // 20][sq.x // 20] = -100
        self.board[self.cube.y//20][self.cube.x//20] = 1000 if self.board[self.cube.y//20][self.cube.x//20] != -100 else -100
        if toprint:
            os.system('cls')
            for row in self.board:
                print(*row)

    def xpos(self, x):
        return self.body[x].x

    def ypos(self, y):
        return self.body[y].y

    def distance_from_walls(self):
        left = (self.cube.x)
        up = (self.cube.y)
        right = (482 // 2 - self.cube.x) - 19
        down = (482 // 2 - self.cube.y) - 19
        return min(up, left, down, right)

    def vision(self):
        current_row = self.cube.y//20
        current_col = self.cube.x//20
        xvel = self.cube.x_vel
        yvel = self.cube.y_vel
        if xvel != 0:
            return self.board[current_row-1*xvel][current_col], self.board[current_row][current_col+1*xvel], self.board[current_row+1*xvel][current_col]
        else:
            return self.board[current_row][current_col+1*yvel], self.board[current_row+1*yvel][current_col], self.board[current_row][current_col-1*yvel]

    def long_vision(self):
        def rotate(matrix, n):
            for _ in range(n):
                matrix = list(zip(*matrix[::-1]))
            return matrix

        duplicate = copy.deepcopy(self.board)
        n = 0
        if self.cube.x_vel == -1:
            n = 1
        elif self.cube.y_vel == 1:
            n = 2
        elif self.cube.x_vel == 1:
            n = 3
        duplicate = rotate(duplicate, n)
        for r, row in enumerate(duplicate):
            for c in range(25):
                if row[c] == 1000:
                    ro = r
                    co = c
                    break
        current_row = ro
        current_col = co
        left = 0
        while duplicate[current_row][current_col] != -100:
            left += 1
            current_col -= 1
        current_row = ro
        current_col = co
        forward = 0
        while duplicate[current_row][current_col] != -100:
            forward += 1
            current_row -= 1
        current_row = ro
        current_col = co
        right = 0
        while duplicate[current_row][current_col] != -100:
            right += 1
            current_col += 1
        current_row = ro
        current_col = co
        left_diagonal = 0
        while duplicate[current_row][current_col] != -100:
            left_diagonal += 1
            current_col -= 1
            current_row -= 1
        current_row = ro
        current_col = co
        right_diagonal = 0
        while duplicate[current_row][current_col] != -100:
            right_diagonal += 1
            current_col += 1
            current_row -=1
        return left - 1, forward - 1, right - 1, left_diagonal - 1, right_diagonal - 1

    def full_vision(self):
        vision = []
        for i in range(0, 14):
            for j in range(0, 14):
                vision.append(self.board[i][j])
        return vision





    def distance_from_food(self):
        # left-negative
        # right-positive
        # up-negative
        # down-positive
        if self.cube.y_vel == -1:
            return (self.food.x - self.cube.x), (self.food.y + 19 - self.cube.y)
        elif self.cube.y_vel == 1:
            return -(self.food.x - self.cube.x), -(self.food.y - self.cube.y - 19)
        elif self.cube.x_vel == 1:
            return (self.food.y - self.cube.y), (self.food.x - self.cube.x - 19)
        elif self.cube.x_vel == -1:
            return -(self.food.y - self.cube.y), -(self.food.x + 19 - self.cube.x)

    def redrawWindow(self):
        global max_score
        self.win.fill((0, 0, 0))
        self.gr.draw(self.win)
        self.cube.draw(self.win)
        for cb in self.body:
            cb.draw(self.win)
        self.food.draw(self.win)
        text = self.sfont.render("Score:" + str(self.score), True, (255, 255, 255))
        self.win.blit(text, (520, 100))
        max_score_text = self.sfont.render("Max_Score:" + str(max_score), True, (255, 0, 0))
        self.win.blit(max_score_text, (520, 200))
        pygame.display.update()

    def main(self):
        global max_score
        while self.run:
            # print(self.score)
            if self.gamedecider == 0:
                # reward = 100-(self.distance_from_food()/7)
                # self.genome.fitness += 1
                self.moves_left -= 1
                if self.moves_left <= 0:
                    # self.genome.fitness -= 50
                    break
                # if self.genome.key == self.genome_to_display or self.score>200:
                pygame.time.delay(5)
                if len(self.cube.path) == 0:
                    if self.algorithm == "neat_shortvision":
                        self.cube.path = neat_shortvision(self.vision(), self.distance_from_food(), self.cube.y, self.cube.x, self.cube)
                    elif self.algorithm == "bfs":
                        self.cube.path = bfs(self.board, self.cube.y//20, self.cube.x//20)
                    elif self.algorithm == "dfs":
                        self.cube.path = dfs(self.board, self.cube.y//20, self.cube.x//20)
                    elif self.algorithm == "a_star":
                        self.cube.path = a_star(self.board, self.cube.y//20, self.cube.x//20, self.food.y//20, self.food.x//20)
                        print(self.cube.path)
                    elif self.algorithm == "neat_long_vision":
                        prev = self.long_vision()
                        self.cube.path = neat_long_vision(prev, self.distance_from_food(), self.cube.y, self.cube.x, self.cube, self.file,self.board, self.food.y//20, self.food.x//20)
                    elif self.algorithm == "neat_full_vision":
                        prev = self.full_vision()
                        self.cube.path = neat_full_vision(self.cube.y//20, self.cube.x//20, prev, self.distance_from_food(), self.cube.y, self.cube.x, self.cube, "winner_full_vision.pkl")
                    elif self.algorithm == "longest_path":
                        self.cube.path = longest_path(self.board, self.cube.y//20, self.cube.x//20, self.food.y//20, self.food.x//20)
                        # print(self.cube.path)
                    # print(self.cube.path)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                # keys = pygame.key.get_pressed()

                for index, heads in reversed(list(enumerate(self.body))):

                    if index == 0:
                        heads.x = self.cube.x
                        heads.y = self.cube.y
                    else:
                        heads.x = self.xpos(index - 1)
                        heads.y = self.ypos(index - 1)
                try:
                    # if len(self.cube.path)==1:
                    #     pygame.time.delay(1000)
                    output = self.cube.path.pop()
                except:
                    # pygame.time.delay(5000)
                    pass
                if self.algorithm == "neat_full_vision":
                    self.cube.path.insert(0,(self.cube.y//20, self.cube.x//20))
                # print("inputs: ",*self.distance_from_food())
                # print("direction: ", direction)


                self.cube.x = output[1]*20+1
                self.cube.y = output[0]*20+1
                self.update_board(False)
                # print(self.cube.y // 20, self.cube.x // 20)
                if self.board[self.cube.y // 20][self.cube.x // 20] == -100:
                    pygame.time.delay(10000)
                    # self.genome.fitness -= 100
                    return prev
                if self.cube.x == self.food.x and self.cube.y == self.food.y:
                    self.food.x = random.randrange(21, 242, 20)
                    self.food.y = random.randrange(21, 242, 20)
                    # self.genome.fitness += 10
                    self.moves_left = 200
                    while self.board[self.food.y//20][self.food.x//20] != 0:
                        # print(self.board[self.food.y//20][self.food.x//20])
                        self.food.x = random.randrange(21, 242, 20)
                        self.food.y = random.randrange(21, 242, 20)
                    # print(self.food.y // 20, self.food.x // 20)

                    self.body.append(head(self.body[-1].x, self.body[-1].y))
                    # self.body.append(head(self.cube.x, self.cube.y))
                    self.score += 1
                    # if self.score>max_score:
                    #     pickle.dump(self.net, open('winner.pkl', 'wb'))
                    max_score = max(self.score, max_score)
                    self.update_board(False)
                # if self.genome.key == self.genome_to_display or self.score>200:
                    # print(self.distance_from_walls())
                    # print(self.vision(), self.cube.y_vel)
                self.redrawWindow()
                    # print(self.cube.x, self.cube.y, self.food.x, self.food.y, self.distance_from_walls(), self.cube.x_vel, self.cube.y_vel)
            else:
                break

        # pygame.quit()

def selu_activation(z):
    lam = 1.0507009873554804934193349852946
    alpha = 1.6732632423543772848170429916717
    return lam * z if z > 0.0 else lam * alpha * (math.exp(z) - 1)

if __name__ == "__main__":
    pygame.init()
    config_file = 'config-feedforward.txt'
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    config.genome_config.add_activation('selu', selu_activation)



    # interface = game("dfs")
    # interface = game("bfs")
    # interface = game("a_star")
    # interface = game("longest_path")
    # interface = game("neat_shortvision")
    # interface = game("neat_long_vision")
    interface = game("neat_full_vision")

    last_vision = interface.main()
        # for i in range(3):
        #     if last_vision[i] > 0:
        #         break
        # else:
        #     print(file)

