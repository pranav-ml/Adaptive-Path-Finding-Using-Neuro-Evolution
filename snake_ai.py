import pygame
import random
import neat
import os
import math
import pickle
import copy

max_score = 0
max_score_complete = 0
complete = 0


class grid():
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, win):
        for width in range(0, 502, 20):
            pygame.draw.line(win, (255, 255, 255), (self.x + width, self.y), (self.x + width, self.y + 500))
            pygame.draw.line(win, (255, 255, 255), (self.x, self.y + width), (self.x + 500, self.y + width))
            pygame.draw.rect(win, (255, 255, 255), (0, 0, 260, 20))
            pygame.draw.rect(win, (255, 255, 255), (0, 0, 20, 260))
            pygame.draw.rect(win, (255, 255, 255), (0, 240, 260, 20))
            pygame.draw.rect(win, (255, 255, 255), (240, 0, 20, 260))


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
        self.x = random.randrange(21, 222, 20)
        self.y = random.randrange(21, 222, 20)

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, 19, 19))


class game():
    def __init__(self, net, genome, genome_to_display):
        self.net = net
        self.genome = genome
        self.gr = grid()
        self.run = True
        self.cube = cube(random.randrange(21, 222, 20), random.randrange(21, 222, 20))
        self.body = [head(self.cube.x, self.cube.y - 20)]
        self.food = food()
        self.score = 0
        self.gamedecider = 0
        self.win = pygame.display.set_mode((800, 501))
        self.sfont = pygame.font.SysFont("comicsans", 30, True)
        self.moves = ["forward", "right", "left"]
        self.moves_left = 200
        self.genome_to_display = genome_to_display
        self.board = [[0] * 25 for _ in range(25)]
        self.update_board(False)

    def update_board(self, toprint):
        # print(cube.y//20, cube.x//20)
        for y, row in enumerate(self.board):
            for x in range(25):
                row[x] = -100 if y == 0 or x == 0 or y == 12 or x == 12 else 0

        # self.board[self.cube.y // 20][self.cube.x // 20] = 100
        self.board[self.food.y // 20][self.food.x // 20] = 100
        self.board[self.cube.y // 20][self.cube.x // 20] = 1000 if self.board[self.cube.y // 20][
                                                                       self.cube.x // 20] != -100 else -100
        for sq in self.body:
            self.board[sq.y // 20][sq.x // 20] = -100
        # if toprint:
        #     os.system('cls')
        #     for row in self.board:
        #         print(*row)

    def xpos(self, x):
        return self.body[x].x

    def ypos(self, y):
        return self.body[y].y

    def distance_from_walls(self):
        left = self.cube.x
        up = self.cube.y
        right = (482 // 2 - self.cube.x) - 19
        down = (482 // 2 - self.cube.y) - 19
        return min(up, left, down, right)

    def vision(self):
        current_row = self.cube.y // 20
        current_col = self.cube.x // 20
        xvel = self.cube.x_vel
        yvel = self.cube.y_vel
        if xvel != 0:
            return self.board[current_row - 1 * xvel][current_col], self.board[current_row][current_col + 1 * xvel], \
                   self.board[current_row + 1 * xvel][current_col]
        else:
            return self.board[current_row][current_col + 1 * yvel], self.board[current_row + 1 * yvel][current_col], \
                   self.board[current_row][current_col - 1 * yvel]

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
            current_row -= 1
        return left - 1, forward - 1, right - 1, left_diagonal - 1, right_diagonal - 1

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
        global max_score_complete, complete
        while self.run:
            # print(self.score)
            if self.gamedecider == 0:
                # reward = 100-(self.distance_from_food()/7)
                self.genome.fitness += 1
                self.moves_left -= 1
                if self.moves_left <= 0:
                    self.genome.fitness = 0
                    break
                if self.genome.key == self.genome_to_display:
                    pygame.time.delay(10)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                # keys = pygame.key.get_pretssed()
                for index, heads in reversed(list(enumerate(self.body))):
                    if index == 0:
                        heads.x = self.cube.x
                        heads.y = self.cube.y
                    else:
                        heads.x = self.xpos(index - 1)
                        heads.y = self.ypos(index - 1)
                # output = self.net.activate(
                #     (*self.distance_from_food(), *self.vision()))
                # print(self.long_vision())
                vision = self.long_vision()
                output = self.net.activate(
                    (*self.distance_from_food(), *vision))
                direction = self.moves[output.index(max(output))]
                # print("inputs: ",*self.distance_from_food())
                # print("direction: ", direction)
                if direction == "right":
                    if self.cube.up:
                        self.cube.x_vel = 1
                        self.cube.y_vel = 0
                        self.cube.up = False
                        self.cube.left = False
                        self.cube.right = True
                        self.cube.down = False
                    elif self.cube.right:
                        self.cube.x_vel = 0
                        self.cube.y_vel = 1
                        self.cube.up = False
                        self.cube.left = False
                        self.cube.right = False
                        self.cube.down = True
                    elif self.cube.down:
                        self.cube.x_vel = -1
                        self.cube.y_vel = 0
                        self.cube.up = False
                        self.cube.left = True
                        self.cube.right = False
                        self.cube.down = False
                    elif self.cube.left:
                        self.cube.x_vel = 0
                        self.cube.y_vel = -1
                        self.cube.up = True
                        self.cube.left = False
                        self.cube.right = False
                        self.cube.down = False
                elif direction == "left":
                    if self.cube.down:
                        self.cube.x_vel = 1
                        self.cube.y_vel = 0
                        self.cube.up = False
                        self.cube.left = False
                        self.cube.right = True
                        self.cube.down = False
                    elif self.cube.left:
                        self.cube.x_vel = 0
                        self.cube.y_vel = 1
                        self.cube.up = False
                        self.cube.left = False
                        self.cube.right = False
                        self.cube.down = True
                    elif self.cube.up:
                        self.cube.x_vel = -1
                        self.cube.y_vel = 0
                        self.cube.up = False
                        self.cube.left = True
                        self.cube.right = False
                        self.cube.down = False
                    elif self.cube.right:
                        self.cube.x_vel = 0
                        self.cube.y_vel = -1
                        self.cube.up = True
                        self.cube.left = False
                        self.cube.right = False
                        self.cube.down = False

                if self.cube.up:
                    self.cube.y -= 20
                elif self.cube.down:
                    self.cube.y += 20
                elif self.cube.right:
                    self.cube.x += 20
                elif self.cube.left:
                    self.cube.x -= 20

                self.update_board(self.genome.key == self.genome_to_display)
                # print(self.cube.y // 20, self.cube.x // 20)
                if self.board[self.cube.y // 20][self.cube.x // 20] == -100:
                    for i in range(3):
                        if vision[i] > 0:
                            self.genome.fitness -= 99 * self.score
                            break
                    else:
                        if self.score > 15:
                            pickle.dump(self.net, open(str(complete) + str(self.score) + '.pkl', 'wb'))
                            complete += 1
                        if self.score > max_score_complete:
                            pickle.dump(self.net, open('winner.pkl', 'wb'))
                            max_score_complete = self.score

                        # self.genome.fitness -= 50 * self.score
                    break
                if self.cube.x == self.food.x and self.cube.y == self.food.y:
                    self.food.x = random.randrange(21, 222, 20)
                    self.food.y = random.randrange(21, 222, 20)
                    while self.board[self.food.y // 20][self.food.x // 20] != 0:
                        self.food.x = random.randrange(21, 222, 20)
                        self.food.y = random.randrange(21, 222, 20)
                    self.genome.fitness += 100
                    self.moves_left = 200

                    self.body.append(head(self.cube.x, self.cube.y))
                    # self.body.append(head(self.cube.x, self.cube.y))
                    self.score += 1
                    # if self.score >= max_score:
                    #     pickle.dump(self.net, open('winner.pkl', 'wb'))
                    max_score = max(self.score, max_score)
                if self.genome.key == self.genome_to_display:
                    # print(self.distance_from_walls())
                    # print(self.vision(), self.cube.y_vel)
                    self.redrawWindow()
                    pass
            else:
                break

        # pygame.quit()


pygame.init()
gen = 0
max_fitness_genome_id, max_fitness = 1, 0


def selu_activation(z):
    lam = 1.0507009873554804934193349852946
    alpha = 1.6732632423543772848170429916717
    return lam * z if z > 0.0 else lam * alpha * (math.exp(z) - 1)


def main(genomes, config):
    global gen, max_fitness, max_fitness_genome_id
    max_fit, max_id = 1, 0
    gen += 1
    for _, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        interface = game(net, g, max_fitness_genome_id)
        interface.main()
        max_id, max_fit = (g.key, g.fitness) if g.fitness >= max_fit else (max_id, max_fit)
    max_fitness_genome_id, max_fitness = max_id, max_fit
    print(max_score)
    # print(max_fitness_genome_id)


def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    config.genome_config.add_activation('selu', selu_activation)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 10 ** 8)


config_path = 'config-feedforward.txt'
run(config_path)
