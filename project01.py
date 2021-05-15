#Eduardo Vasquez
#Num de Estudiante:75470
#vasquez_75470_proyect01 Flappy

from graphics import*
import random
import math

#Define Constants
UPDATE_RATE = 30
WIN_WIDTH = 500
WIN_HEIGHT = 500
WIN_TITLE = 'Flappy'

#Define Global Variables
exit_game = False
game_lost = False
bird_collided = False

#Define Bird Variables
birdXPosition = WIN_WIDTH / 8
birdYPosition = WIN_HEIGHT / 2
birdRadious = 6
birdDirection = 1
birdSpeed = 6
birdColor = color_rgb(0,102,0)
bird = Circle(Point(birdXPosition, birdYPosition), birdRadious)

#Define Enemy Circles
enemyList = []
enemyRadious = 12
enemySpeed = 6
enemyColor = 'black'
enemyTotalPerScreen = 16

def handle_input(win):
    key = win.checkKey()
    if key == "space":
        change_direction()
    elif key == "Escape":
        global exit_game
        exit_game = True

def draw_bird(win):
    global bird
    bird.setFill(birdColor)
    bird.setOutline(birdColor)
    bird.draw(win)

def draw_enemy(win):
    xPos = random.randint(enemyRadious, WIN_WIDTH - enemyRadious)
    yPos = random.randint(enemyRadious, WIN_HEIGHT - enemyRadious)

    enemy = Circle(Point(xPos + WIN_WIDTH, yPos), enemyRadious)
    enemy.setFill(enemyColor)
    enemy.setOutline(enemyColor)
    enemy.draw(win)

    global enemyList
    enemyList.append(enemy)
    
def move_enemy():
    global enemyList
    for e in enemyList:
        e.move(-enemySpeed, 0)

def move_bird():
    global bird
    bird.move(0, birdDirection * birdSpeed)

def change_direction():
    global birdDirection
    birdDirection *= -1

def bird_boundories():
    if bird.getCenter().getY() + birdRadious < 0 or bird.getCenter().getY() - birdRadious > WIN_HEIGHT:
        global game_lost
        game_lost = True

def remove_enemies():
    global enemyList
    for e in enemyList:
        if e.getCenter().getX() < -enemyRadious:
            enemyList.remove(e)
            e.undraw()

def remove_all():
    global enemyList
    for e in enemyList:
        enemyList.remove(e)
        e.undraw()
    global bird
    bird.undraw()
    
def create_enemies(win):
    enemiesOnRight = False
    
    for e in enemyList:
        if e.getCenter().getX() + enemyRadious > WIN_WIDTH:
            enemiesOnRight = True
            break
    if enemiesOnRight == False:
        for i in range(enemyTotalPerScreen):
            draw_enemy(win)

def bird_check_collision():
    for e in enemyList:
        dx = bird.getCenter().getX() - e.getCenter().getX()
        dy = bird.getCenter().getY() - e.getCenter().getY()
        length = math.sqrt(abs((dx*dx) + (dy*dy)))
        if length < birdRadious + enemyRadious:
            global bird_collided
            bird_collided = True
            break

def main():
    win = GraphWin(WIN_TITLE, WIN_WIDTH, WIN_HEIGHT)
    draw_bird(win)

    global game_lost
    global bird
    
    while(1):
        handle_input(win)
        create_enemies(win)
        move_bird()
        move_enemy()
        remove_enemies()
        bird_boundories()
        bird_check_collision()
        update(UPDATE_RATE)

        if exit_game or game_lost or bird_collided:
            break
        
    if bird_collided:
        bird.setFill('red')
        bird.setOutline('red')
        game_lost = True
        time.sleep(3)
        

    if game_lost:
        while win.checkKey() != "Escape":
            remove_all()
            message = Text(Point(WIN_WIDTH / 2, WIN_HEIGHT * 2/5), 'G A M E   O V E R')
            message.setSize(32)
            message.setFace('helvetica')
            message.draw(win)
    win.close()

main()
