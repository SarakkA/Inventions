import pygame as py
import random

py.init()


WIN_WIDTH = 600
WIN_HEIGHT = 600

# width and height of each cell
w = 30

wn = py.display.set_mode((WIN_WIDTH, WIN_HEIGHT - w))
py.display.set_caption('Maze Generator')

# clock object
clock = py.time.Clock()

# Number of columns and rows
cols = WIN_WIDTH // w
rows = WIN_HEIGHT // w

# List of all cells
grid = []

# Stack to keep track of visited cells
stack = []


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # walls of each cell [ Top wall, right wall, bottom wall, left wall]
        self.walls = [True, True, True, True]
        self.visited = False

    def draw(self):
        if self.walls[0]:
            py.draw.line(wn, (255, 255, 255), (self.x, self.y), (self.x + w, self.y))
        if self.walls[1]:
            py.draw.line(wn, (255, 255, 255), (self.x + w, self.y), (self.x + w, self.y + w))
        if self.walls[2]:
            py.draw.line(wn, (255, 255, 255), (self.x + w, self.y + w), (self.x, self.y + w))
        if self.walls[3]:
            py.draw.line(wn, (255, 255, 255), (self.x, self.y + w), (self.x, self.y))

        if self.visited:
            # color the visited cells
            py.draw.rect(wn, (100, 100, 255), (self.x + 1, self.y + 1, w, w))

    def check_neighbours(self):

        # append the neighbors of the current cell (if available) to the neighbors list
        neighbours = []
        top = grid[index(self.x, self.y - w)]
        right = grid[index(self.x + w, self.y)]
        bottom = grid[index(self.x, self.y + w)]
        left = grid[index(self.x - w, self.y)]

        if self.y > 0 and not top.visited:
            neighbours.append(top)
        if self.x < WIN_WIDTH - w and not right.visited:
            neighbours.append(right)
        if self.y < WIN_WIDTH - 2 * w and not bottom.visited:
            neighbours.append(bottom)
        if self.x > 0 and not left.visited:
            neighbours.append(left)

        # if there is a neighbors available, return one of them randomly
        if len(neighbours) > 0:
            r = random.randint(0, len(neighbours) - 1)
            return neighbours[r]

    # highlights the current cell
    def highlight(self):
        py.draw.rect(wn, (0, 255, 0), (self.x + 1, self.y + 1, w, w))


# Enumerate all the cells and give them an index
def index(x, y):
    return x // w + y // w * cols


# When the current cell moves, remove the wall between the two cells
def remove_walls(a, b):
    diff_x = a.x - b.x
    if diff_x > 0:
        a.walls[3] = False
        b.walls[1] = False
    elif diff_x < 0:
        a.walls[1] = False
        b.walls[3] = False

    diff_y = a.y - b.y
    if diff_y > 0:
        a.walls[0] = False
        b.walls[2] = False
    elif diff_y < 0:
        a.walls[2] = False
        b.walls[0] = False


# Create the grid list
for j in range(cols):
    for i in range(rows):
        cc = Cell(i * w, j * w)
        grid.append(cc)

# Initialize the current cell
current = grid[55]


run = True
while run:
    clock.tick(30)
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            quit()

    for i in grid:
        i.draw()

    # Step 1 of the Recursive backtracker algorithm
    current.visited = True
    current.highlight()

    new = current.check_neighbours()

    if new is not None:
        new.visited = True

        # Step 2 of the algorithm
        stack.append(current)

        # Step 3 of the algorithm
        remove_walls(current, new)

        # Step 4 of the algorithm
        current = new

    elif len(stack) > 0:
        current = stack.pop()

    py.display.update()
    wn.fill((0, 0, 0))
