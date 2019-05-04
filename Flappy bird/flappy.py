import pygame as py
import random
import math

py.init()

# Global constants
WIN_WIDTH = 600
WIN_HEIGHT = 600

EVENT_NEWPIPE = py.USEREVENT + 1
EVENT_NEWCOIN = py.USEREVENT + 2

# Create the window
wn = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
py.display.set_caption("Flappy bird")

# Images
bg = py.image.load('bgbg.png').convert_alpha()
bir = py.image.load('big_flappy.png').convert_alpha()
img = py.image.load('flappy_d_buono.png').convert_alpha()
img2 = py.image.load('top_pipe.png').convert_alpha()
img3 = py.image.load('coin.png').convert_alpha()
img4 = py.image.load('fly_flap.png').convert_alpha()

wn.blit(bg, (0, 0))

# Create a clock object
clock = py.time.Clock()

# Fonts
font2 = py.font.SysFont("comicsansmc", 30)

coin_score = 0
score = 0


# Player class
class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 0
        self.gravity = 1
        self.lift = -1

    def draw(self):
        # py.draw.circle(wn, (255, 255, 255), (self.x, self.y), self.radius)
        if keys[py.K_SPACE]:
            wn.blit(img4, (self.x - 17, self.y - 16))
        else:
            wn.blit(bir, (self.x - 17, self.y - 16))

    # Gravity function
    def update(self):
        self.vel += self.gravity
        self.y += self.vel

        if self.y < 0:
            self.y = 0
        if self.y > WIN_HEIGHT - 10:
            self.y = WIN_HEIGHT - 10
            self.vel = 0

    # Jump function
    def up(self):
        self.vel = self.lift*10


# Coin class
class Coin:
    def __init__(self):
        self.x = WIN_WIDTH
        self.y = random.randint(50, WIN_HEIGHT - 50)
        self.vel = 5

    def draw(self):
        py.draw.circle(wn, (255, 255, 0), (self.x, self.y), 10)
        wn.blit(img3, (self.x - 11, self.y - 11))

    def update(self):
        self.x -= self.vel

    # Check if the player collide with the coin
    def collision(self):
        if distance(bird.x, bird.y, self.x, self.y) < 20:
            return True
        else:
            return False


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Pipe class
class Pipe:
    def __init__(self):
        self.opening = random.randint(130, 210)
        self.top = random.randint(0, WIN_HEIGHT - self.opening - 10)
        self.bottom = random.randint(0, WIN_HEIGHT // 2)
        self.x = WIN_WIDTH
        self.speed = 5
        self.score = 0

    def draw(self):

        # py.draw.rect(wn, (255, 255, 255), (self.x, 0, 20, self.top))
        # py.draw.rect(wn, (255, 255, 255), (self.x, self.top + self.opening, 20, win_height - self.top - self.opening))
        wn.blit(img, (self.x - 3, self.top + self.opening - 3))
        wn.blit(img2, (self.x - 3, self.top - 504))

    def update(self):
        self.x -= self.speed

    # Check if the player collide with the pipe
    def collision(self):
        if bird.x - 12 < self.x + 20 and bird.x + 12 > self.x and (
                bird.y + 10 > self.top + self.opening or bird.y - 12 < self.top):
            return True
        else:
            return False


# Initialize player
bird = Player(100, 0, 15)

list_pipes = []
list_coin = []

# Create an event every x millisecond
py.time.set_timer(EVENT_NEWPIPE, 2500)
py.time.set_timer(EVENT_NEWCOIN, 2347)

run = True
while run:
    clock.tick(30)

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False

        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                bird.up()
        # Create a new pipe
        if event.type == EVENT_NEWPIPE:
            pp = Pipe()
            list_pipes.append(pp)
        # Create a new coin
        if event.type == EVENT_NEWCOIN:
            cc = Coin()
            list_coin.append(cc)

    wn.blit(bg, (0, 0))

    keys = py.key.get_pressed()

    bird.draw()
    bird.update()

    for p in list_pipes:
        p.draw()
        p.update()

        # Update the score when the player does not collide with the pipe
        if p.x == 90:
            score += 1
        if p.collision():
            # Restart the game
            list_pipes.clear()
            score = 0
            list_coin.clear()
            coin_score = 0

    for c in list_coin:
        c.draw()
        c.update()
        if c.collision():
            list_coin.remove(c)
            coin_score += 1

    # Create text with score and coin score
    text = font2.render("score: " + str(score), True, (0, 0, 0))
    coin_text = font2.render('coins: ' + str(coin_score), True, (0, 0, 0))

    # Display texts
    wn.blit(text, (40, 40))
    wn.blit(coin_text, (450, 40))

    py.display.update()
    wn.fill((0, 0, 0))
py.quit()
