#Eduardo Vasquez
#Num de Estudiante:75470
#vasquez_75470_proyect01_C Flappy
# with class

from graphics import*
import random
import math

#Define Constants
UPDATE_RATE = 30
WIN_WIDTH = 500
WIN_HEIGHT = 500
WIN_TITLE = 'Flappy'

#Define Bird Variables
birdColor = color_rgb(0,102,0)

#Define Enemy Circles
enemyColor = 'black'

class Bird():
    def __init__(self, max_birds):
        self.max_birds = max_birds
        self.birds = []
        
    def add_bird(self, bird):
        if len(self.birds) < self.max_birds:
            self.birds.append(bird)

    def set_dead_color(self):
        self.birds[0].circle.setFill('red')
        self.birds[0].circle.setOutline('red')
    
    def remove_bird(self):
        self.birds[0].remove_cBall()
        
    def boundories(self):
        bird = self.birds[0]
        if bird.circle.getCenter().getY() + bird.radious < 0 or bird.circle.getCenter().getY() - bird.radious > WIN_HEIGHT:
            global game_lost
            game_lost = True

    def check_collision(self, enemies):
        birdCircle = self.birds[0].circle
        for enemy in enemies:
            dx = birdCircle.getCenter().getX() - enemy.circle.getCenter().getX()
            dy = birdCircle.getCenter().getY() - enemy.circle.getCenter().getY()
            length = math.sqrt(abs((dx*dx) + (dy*dy)))
            if length < self.birds[0].radious + enemy.radious:
                global bird_collided
                bird_collided = True
                break
    
    def handle_input(self):
        key = self.birds[0].win.checkKey()
        if key == "space":
            self.birds[0].invert_direction()
        elif key == "Escape":
            global exit_game
            exit_game = True

    def update(self, enemies):
        self.handle_input()
        self.birds[0].move_cBall()
        self.boundories()
        self.check_collision(enemies)

class EnemyGroup():
    def __init__(self, max_enemies):
        self.max_enemies = max_enemies
        self.enemies = []

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def remove_enemies(self):
        for enemy in self.enemies:
            enemy.remove_cBall()

    def boundories(self):
        for enemy in self.enemies:
            if enemy.circle.getCenter().getX() + enemy.radious < 0:
                enemy.remove_cBall()
                self.enemies.remove(enemy)

    def can_create_new_enemies(self, win):
        for enemy in self.enemies:
            if enemy.circle.getCenter().getX() + enemy.radious > WIN_WIDTH:
                return
        for i in range(self.max_enemies):
            self.add_enemy(create_enemy(win))
            
    def update(self, win):
        for enemy in self.enemies:
            enemy.move_cBall()
        self.boundories()
        self.can_create_new_enemies(win)
        
class cBall():
    def __init__(self, xPos, yPos, radious, direction, x_speed, y_speed, color, win):
        self.xPos = xPos
        self.yPos = yPos
        self.radious = radious
        self.direction = direction
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color = color
        self.win = win
        self.circle = self.create_cBall()

    def create_cBall(self):
        circle = Circle(Point(self.xPos, self.yPos), self.radious)
        circle.setFill(self.color)
        circle.setOutline(self.color)
        circle.draw(self.win)
        return circle

    def move_cBall(self):
        self.xPos += self.x_speed * self.direction
        self.yPos += self.y_speed * self.direction
        self.circle.move(self.x_speed * self.direction, self.y_speed * self.direction)

    def invert_direction(self):
        self.direction = -self.direction

    def remove_cBall(self):
        self.circle.undraw()


def create_enemy(win):
    xPos = random.randint(12, WIN_WIDTH - 12)
    yPos = random.randint(12, WIN_HEIGHT - 12)
    circle = cBall(xPos + WIN_WIDTH, yPos, 12, -1, 6, 0, enemyColor, win)
    return circle

def main():
    win = GraphWin(WIN_TITLE, WIN_WIDTH, WIN_HEIGHT)
    bird = Bird(1)
    bird.add_bird(cBall(WIN_WIDTH / 8, WIN_HEIGHT / 2, 6, 1, 0, 6, birdColor, win))
    enemyGroup = EnemyGroup(16)

    global game_lost
    
    while(1):
        bird.update(enemyGroup.enemies)
        enemyGroup.update(win)
        update(UPDATE_RATE)

        if exit_game or game_lost or bird_collided:
            break
        
    if bird_collided:
        bird.set_dead_color()
        game_lost = True
        time.sleep(1)
        
    if game_lost:

        while win.checkKey() != "Escape":
            enemyGroup.remove_enemies()
            bird.remove_bird()
            message = Text(Point(WIN_WIDTH / 2, WIN_HEIGHT * 2/5), 'G A M E   O V E R')
            message.setSize(32)
            message.setFace('helvetica')
            message.draw(win)
    win.close()

main()
