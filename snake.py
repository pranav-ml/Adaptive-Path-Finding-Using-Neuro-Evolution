import pygame
import random
pygame.init()
def xpos(x):
    for i,c in enumerate(body):
        if x==i:
            return c.x
def ypos(y):
    for index,item in enumerate(body):
        if y==index:
            return item.y
class grid():
    def __init__(self):
        self.x=0
        self.y=0

    def drawgrid(self):
        for width in range(0,502,20):
            pygame.draw.line(win,(255,255,255),(self.x+width,self.y),(self.x+width,self.y+500))
            pygame.draw.line(win, (255, 255, 255), (self.x, self.y + width), (self.x + 500, self.y + width))
class cube():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.up = False
        self.left = False
        self.right = False
        self.down = False
    def draw(self):
        pygame.draw.rect(win,(0,0,255),(self.x,self.y,19,19))

class head():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def draw(self):

        pygame.draw.rect(win,(255,0,0),(self.x,self.y,19,19))

class food():
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def draw(self):
        pygame.draw.rect(win,(0,255,0),(self.x,self.y,19,19))

def redrawWindow():
    win.fill((0,0,0))
    gr.drawgrid()
    cube.draw()
    for test in body:
        test.draw()
    food.draw()
    text=sfont.render("Score:"+str(score),1,(255,255,255))
    win.blit(text,(520,100))
    pygame.display.update()

gr=grid()
win=pygame.display.set_mode((640,501))
run=True
cube=cube(81,81)
body=[]
food=food(41,301)
score=0
gamedecider=0
sfont=pygame.font.SysFont("comicsans",30,True)
while run:
    if gamedecider==0:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        for index,heads in reversed(list(enumerate(body))):
            if index==0:
                heads.x=cube.x
                heads.y=cube.y
            else:

                heads.x = xpos(index-1)
                heads.y = ypos(index-1)


        if len(body)>0:
            if keys[pygame.K_UP] and cube.down==False:
                cube.up=True
                cube.left = False
                cube.right = False
                cube.down = False
            elif keys[pygame.K_DOWN] and cube.up==False:
                cube.down=True
                cube.up = False
                cube.left = False
                cube.right = False

            elif keys[pygame.K_RIGHT] and cube.left==False:
                cube.right=True
                cube.up = False
                cube.left = False
                cube.down = False
            elif keys[pygame.K_LEFT] and cube.right==False:
                cube.left=True
                cube.up = False
                cube.right = False
                cube.down = False
        else:
            if keys[pygame.K_UP]:
                cube.up = True
                cube.left = False
                cube.right = False
                cube.down = False
            elif keys[pygame.K_DOWN]:
                cube.down = True
                cube.up = False
                cube.left = False
                cube.right = False

            elif keys[pygame.K_RIGHT]:
                cube.right = True
                cube.up = False
                cube.left = False
                cube.down = False
            elif keys[pygame.K_LEFT]:
                cube.left = True
                cube.up = False
                cube.right = False
                cube.down = False
        if cube.up:
            cube.y -= 20
        elif cube.down:
            cube.y += 20
        elif cube.right:
            cube.x += 20
        elif cube.left:
            cube.x -= 20
        for heads in body:
            if cube.x==heads.x and cube.y==heads.y:
                gamedecider=1
                for x in range(0,4):
                    win.fill((0, 0, 0))
                    gr.drawgrid()
                    food.draw()
                    text = sfont.render("Score:" + str(score), 1, (255, 255, 255))
                    win.blit(text, (520, 100))
                    pygame.display.update()
                    pygame.time.delay(500)
                    win.fill((0, 0, 0))
                    for test in body:
                        test.draw()
                    gr.drawgrid()
                    cube.draw()
                    food.draw()
                    text = sfont.render("Score:" + str(score), 1, (255, 255, 255))
                    win.blit(text, (520, 100))
                    pygame.display.update()
                    pygame.time.delay(500)
        if cube.x >= 501:
            cube.x = 1
        if cube.x <= -19:
            cube.x = 481
        if cube.y >= 501:
            cube.y = 1
        if cube.y <= -19:
            cube.y = 501

        if cube.x == food.x and cube.y == food.y:
            food.x=random.randrange(1,492,20)
            food.y=random.randrange(1,492,20)
            for square in body:
                if square.x==food.x and square.y==food.y:
                    food.x = random.randrange(1, 492, 20)
                    food.y = random.randrange(1, 492, 20)

            body.append(head(cube.x, cube.y))
            body.append(head(cube.x, cube.y))
            score+=1
        redrawWindow()
    else:
        win.fill((0, 0, 0))
        text2 = sfont.render("GAME OVER", 1, (255, 255, 255))
        text3 = sfont.render("YOUR SCORE:" + str(score), 1, (255, 255, 255))
        win.blit(text2, (240, 220))
        win.blit(text3, (225, 320))
        pygame.display.update()
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:

            body = []
            cube.x = 81
            cube.y=81
            cube.right =False
            cube.up = False
            cube.left = False
            cube.down = False
            food.x =41
            food.y=301
            score = 0
            gamedecider = 0
            sfont = pygame.font.SysFont("comicsans", 30, True)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

pygame.quit()
