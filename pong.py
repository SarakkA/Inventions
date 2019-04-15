import pygame as py
import random

py.init()

# Global constants
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
WIN_WIDTH  = 600
WIN_HEIGHT = 600

# Clock object
clock = py.time.Clock()

# Opens a window and name it
wn = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
py.display.set_caption('Pong game')

# Fonts
font = py.font.SysFont('comicsansms', 30)
little_font = py.font.SysFont('comicsansms', 20)


class Player:
    def __init__(self, x, y, up, down):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 80
        self.vel = 8
        self.up = up
        self.down = down

    def draw(self):
        py.draw.rect(wn, WHITE, (self.x, self.y, self.width, self.height))

    def move(self):
        keys = py.key.get_pressed()

        if keys[self.up] and self.y > 0:
            self.y -= self.vel
        if keys[self.down] and self.y + self.height < WIN_HEIGHT:
            self.y += self.vel

    # collision with ball
    def collision(self):
        if self.y < ball.y < self.y + self.height:
            if abs(self.x + self.width // 2 - ball.x) < self.width // 2 + ball.radius:
                ball.vel_x *= -1


class Ball:
    def __init__(self):
        self.x = WIN_WIDTH // 2
        self.y = WIN_HEIGHT // 2
        self.vel_x = 8
        self.vel_y = 6
        self.radius = 10
        self.score1 = 0
        self.score2 = 0

    def draw(self):
        py.draw.circle(wn, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # collision with walls
        if self.y < 0 or self.y > WIN_HEIGHT:
            self.vel_y *= -1
        # score and reset the ball
        if self.x < 0:
            self.x = WIN_WIDTH // 2
            self.y = random.randint(100, 500)
            self.score2 += 1
        if self.x > WIN_WIDTH:
            self.x = WIN_WIDTH // 2
            self.y = random.randint(100, 500)
            self.score1 += 1


# defines an interactive button object
def button(msg, x, y, w, h, c1, c2, action):

    mouse = py.mouse.get_pos()
    click = py.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1:
            if action == 'play':
                main()
            if action == 'quit':
                py.quit()
                quit()
        py.draw.rect(wn, c1, (x, y, w, h))
    else:
        py.draw.rect(wn, c2, (x, y, w, h))

    wn.blit(font.render(msg, True, BLACK), (x + 20, y))


# Initialize the ball and the players
player1 = Player(50, 250, py.K_UP, py.K_DOWN)
player2 = Player(WIN_WIDTH - 60, 250, py.K_w, py.K_s)
ball = Ball()


def main():

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()

        # 30 FPS
        clock.tick(30)

        wn.fill(BLACK)

        player1.draw()
        player1.move()
        player1.collision()

        player2.draw()
        player2.move()
        player2.collision()

        ball.draw()
        ball.move()

        score_1 = font.render(str(ball.score1), True, WHITE)
        score_2 = font.render(str(ball.score2), True, WHITE)
        wn.blit(score_1, (250, 300))
        wn.blit(score_2, (350, 300))

        py.display.update()


# Intro scene
def intro():
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()

        wn.fill(BLACK)

        button('play', 250, 200, 100, 50, WHITE, (200, 200, 200), 'play')
        button('quit', 250, 300, 100, 50, WHITE, (200, 200, 200), 'quit')

        py.display.update()


if __name__ == '__main__':
    intro()
