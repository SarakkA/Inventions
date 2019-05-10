import pygame as py
import math
import random

py.init()

WIN_HEIGHT = 600
WIN_WIDTH = 450

# Make the window object
wn = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
py.display.set_caption('Arkanoid')

clock = py.time.Clock()

# Fonts and texts
font = py.font.SysFont('comicsansms', 30)
text = font.render("ARKANOID", True, (255, 255, 0))
play_button = font.render("PLAY!", True, (255, 255, 255))
quit_button = font.render("QUIT!", True, (255, 255, 255))


# Main loop
def game_loop():
    run = True
    while run:
        # Set FPS
        clock.tick(30)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()
        # Player movements
        keys = py.key.get_pressed()

        if keys[py.K_RIGHT] and arka.x < WIN_WIDTH - arka.width:
            arka.x += arka.vel
        if keys[py.K_LEFT] and arka.x > 0:
            arka.x -= arka.vel

        arka.draw()
        palla.draw()
        palla.update()

        # Check for collision, if True, remove the box hit
        for b in boxes:
            b.draw()

            if dist(b.center_x, palla.x) < b.width // 2 + 15 and dist(b.center_y, palla.y) < b.height // 2 + 15:
                boxes.remove(b)
                palla.vel_y *= -1

        # Restart the game
        if palla.y > WIN_HEIGHT:
            palla.y = 280
            boxes.clear()
            create_boxes()

        if len(boxes) == 0:
            palla.y = 280
            palla.x = 30
            create_boxes()

        py.display.update()
        wn.fill((0, 0, 0))


# Button function
def button(msg, x, y, w, h, c1, c2, action):
    mouse = py.mouse.get_pos()
    click = py.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        py.draw.rect(wn, c1, (x, y, w, h))
        if click[0] == 1:
            if action == 'play':
                game_loop()
            elif action == 'quit':
                py.quit()
                quit()
    else:
        py.draw.rect(wn, c2, (x, y, w, h))

    wn.blit(font.render(msg, True, (255, 255, 255)), (x + 8, y))


# Intro screen
def game_intro():
    intro = True

    while intro:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()

        wn.blit(text, (150, 100))

        button('PLAY!', 100, 350, 100, 50, (0, 255, 0), (0, 150, 0), 'play')

        button('QUIT!', 250, 350, 100, 50, (255, 0, 0), (150, 0, 0), 'quit')

        py.display.update()
        clock.tick(15)


# 2 dimensional distance
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# 1 dimensional distance
def dist(x1, x2):
    return abs(x1 - x2)


# Player class
class Player:
    def __init__(self):
        self.width = 84
        self.height = 15
        self.x = WIN_WIDTH // 2 - self.width // 2
        self.y = WIN_HEIGHT - 100
        self.vel = 8

    def draw(self):
        py.draw.rect(wn, (255, 255, 255), (self.x, self.y, self.width, self.height))


# Ball class
class Ball:
    def __init__(self):
        self.x = 10
        self.y = 280
        self.radius = 12
        self.vel_x = 8
        self.vel_y = 8
        self.space = arka.width // 6

    def draw(self):
        py.draw.circle(wn, (250, 250, 0), (self.x, self.y), self.radius)

    def update(self):

        # Check the bounce with walls
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x < self.radius or self.x > WIN_WIDTH - self.radius:
            self.vel_x *= -1
        if self.y < self.radius:
            self.vel_y *= -1

        ''' 
                Check for collision with player and change its velocity direction,
                velocity magnitude is kept
        '''

        if arka.y + self.radius > self.y > arka.y - self.radius:
            if arka.x < self.x <= arka.x + self.space:
                self.vel_x = -9
                self.vel_y = -4
            if arka.x + self.space < self.x < arka.x + self.space * 2:
                self.vel_x = - 7
                self.vel_y = - 7
            if arka.x + self.space * 2 < self.x < arka.x + self.space * 3:
                self.vel_x = - 4
                self.vel_y = - 9
            if arka.x + self.space * 3 < self.x < arka.x + self.space * 4:
                self.vel_x = 4
                self.vel_y = -9
            if arka.x + self.space * 4 < self.x < arka.x + self.space * 5:
                self.vel_x = 7
                self.vel_y = -7
            if arka.x + self.space * 5 < self.x < arka.x + arka.width:
                self.vel_x = 9
                self.vel_y = - 4


# Boxes class
class Boxes:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 22
        self.center_x = self.x + self.width // 2
        self.center_y = self.y + self.height // 2
        self.color = color

    def draw(self):
        py.draw.rect(wn, self.color, (self.x, self.y, self.width, self.height))


arka = Player()
palla = Ball()

# Create the Boxes list
boxes = []


def create_boxes():
    a = random.randint(0, 2)
    if a == 0:
        for j in range(2, 10):
            for i in range(j):
                b = Boxes(i * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)
    if a == 1:
        for j in range(2, 5):
            for i in range(10):
                b = Boxes(i * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)

    if a == 2:
        for j in range(2, 10):
            for i in range(10 - j + 1):
                b = Boxes(i * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)

    if a == 3:
        for j in range(2, 10):
            if j == 2 or j == 9:
                for i in range(1, 9):
                    b = Boxes(i * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                    boxes.append(b)
            else:

                b = Boxes(1 * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)

                b = Boxes(8 * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)
    if a == 4:
        b = Boxes(5 * 45 - 20, 6 * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
        boxes.append(b)
        for j in range(2, 11):
            for i in range(j - 1, 10 - j + 1):
                b = Boxes(i * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)
            for i in range(10 - j + 1, j - 1):
                b = Boxes(i * 45 + 1, j * 23 + 1, (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255)))
                boxes.append(b)


create_boxes()


if __name__ == '__main__':
    game_intro()
