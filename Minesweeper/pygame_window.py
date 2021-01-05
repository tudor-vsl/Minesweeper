import pygame, sys
from Minesweeper.Project.mine_board import *

pygame.init()

black = (100, 0, 100)
white = (200, 200, 200)

red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block1 = pygame.image.load("block1.png")
block2 = pygame.image.load("block2.png")
block3 = pygame.image.load("block3.png")
block4 = pygame.image.load("block4.png")
block5 = pygame.image.load("block5.png")
block6 = pygame.image.load("block6.png")
block7 = pygame.image.load("block7.png")
block8 = pygame.image.load("block8.png")
empty = pygame.image.load("blankblock1.png")
blank = pygame.image.load("blankblock.png")
bomb = pygame.image.load("bomb.png")

rows, cols, no_of_bombs = 9, 9, 30# setup_board() minim 23 pt max 24 x 34
matrix = np.zeros((rows + 1, cols + 1), dtype=int)
test = Board(rows, cols, no_of_bombs, matrix)

unveil_matrix = np.zeros((rows, cols), dtype=int)

test.place_bombs()
test.place_numbers()
test.print_matrix()

indent = 15

header = 15

height = header * 2 + test.cols * 16
width = indent * 2 + test.rows * 16

window = pygame.display.set_mode((height, width))
pygame.display.get_surface().fill((200, 200, 200))
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    window.blit(textSurf, textRect)


def setup_board():
    rows = int(input("Input rows:"))
    cols = int(input("Input cols:"))
    no_of_bombs = int(input("Input no_of_bombs:"))
    return rows, cols, no_of_bombs


def createSquare(x, y, color):
    pygame.draw.rect(window, color, [x, y, width, height])


def block(x, y, blockImg):
    window.blit(blockImg, (x, y))


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(white)
        largeText = pygame.font.SysFont("comicsansms", width // 10)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((width / 2), (height / 2))
        window.blit(TextSurf, TextRect)

        button("GO!", width // 2 - 30, height // 2 - 50, 50, 30, green, bright_green, main)
        # button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def block_assignment(val, x, y):
    if val == 1:
        block(x, y, block1)
    elif val == 2:
        block(x, y, block2)
    elif val == 3:
        block(x, y, block3)
    elif val == 4:
        block(x, y, block4)
    elif val == 5:
        block(x, y, block5)
    elif val == 6:
        block(x, y, block6)
    elif val == 7:
        block(x, y, block7)
    elif val == 8:
        block(x, y, block8)
    elif val == 0:
        block(x, y, empty)
    else:
        block(x, y, bomb)


def unveil(m_i, m_j):
    y = header  # we start at the top of the screen
    for i in range(0, test.rows):
        x = indent  # for every row we start at the left of the screen again
        for j in range(0, test.cols):
            if i == m_i and j == m_j:
                if unveil_matrix[m_i][m_j] == 0:
                    block_assignment(test.main_matrix[i][j], x, y)
                    unveil_matrix[m_i][m_j] = 1
            if unveil_matrix[i][j] == 1:
                block_assignment(test.main_matrix[i][j], x, y)

            x += 16  # for ever item/number in that row we move one "step" to the right
        y += 16  # for every new row we move one "step" downwards
    pygame.display.update()


def check_indexes(i, j):
    if i >= 0 and i <= rows and j >= 0 and j <= cols:
        return True
    return False


def unveil_neighbours(check_matrix, m_i, m_j):
    if test.main_matrix[m_i][m_j] == 0:
        if check_matrix[m_i - 1][m_j - 1] == 0 and  check_indexes(m_i - 1, m_j - 1) is True:
            check_matrix[m_i - 1][m_j - 1] = 1
            unveil_neighbours(check_matrix, m_i - 1, m_j - 1)

        if check_matrix[m_i - 1][m_j] == 0 and  check_indexes(m_i - 1, m_j) is True:
            check_matrix[m_i - 1][m_j - 1] = 1
            unveil_neighbours(check_matrix, m_i - 1, m_j)

        if check_matrix[m_i - 1][m_j + 1] == 0 and  check_indexes(m_i - 1, m_j + 1) is True:
            check_matrix[m_i - 1][m_j + 1] = 1
            unveil_neighbours(check_matrix, m_i - 1, m_j + 1)

        if check_matrix[m_i][m_j - 1] == 0 and  check_indexes(m_i, m_j - 1) is True:
            check_matrix[m_i][m_j - 1] = 1
            unveil_neighbours(check_matrix, m_i, m_j - 1)

        if check_matrix[m_i][m_j + 1] == 0 and check_indexes(m_i, m_j + 1) is True:
            check_matrix[m_i][m_j - 1] = 1
            unveil_neighbours(check_matrix, m_i, m_j + 1)

        if check_matrix[m_i + 1][m_j - 1] == 0  and check_indexes(m_i + 1, m_j - 1) is True:
            check_matrix[m_i + 1][m_j - 1] = 1
            unveil_neighbours(check_matrix, m_i + 1, m_j - 1)

        if check_matrix[m_i + 1][m_j] == 0 and check_indexes(m_i + 1, m_j) is True:
            check_matrix[m_i + 1][m_j] = 1
            unveil_neighbours(check_matrix, m_i + 1, m_j)

        if check_matrix[m_i + 1][m_j + 1] == 0 and check_indexes(m_i + 1, m_j + 1) is True:
            check_matrix[m_i + 1][m_j + 1] = 1
            unveil_neighbours(check_matrix, m_i + 1, m_j + 1)

    y = header  # we start at the top of the screen
    for i in range(0, test.rows):
        x = indent  # for every row we start at the left of the screen again
        for j in range(0, test.cols):
            if i == m_i and j == m_j:
                if unveil_matrix[m_i][m_j] == 0:
                    block_assignment(test.main_matrix[i][j], x, y)
                    unveil_matrix[m_i][m_j] = 1
            if unveil_matrix[i][j] == 1:
                block_assignment(test.main_matrix[i][j], x, y)

            x += 16  # for ever item/number in that row we move one "step" to the right
        y += 16  # for every new row we move one "step" downwards
    pygame.display.update()


def init_game():
    y = header  # we start at the top of the screen
    for i in range(0, test.rows):
        x = indent  # for every row we start at the left of the screen again
        for j in range(0, test.cols):
            block(x, y, blank)
            x += 16  # for ever item/number in that row we move one "step" to the right
        y += 16  # for every new row we move one "step" downwards
    pygame.display.update()


def main():
    init_game()
    while True:
        # drawGrid()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                print(pos_x, pos_y)
                if pos_x > header and pos_x < height - header and pos_y > indent and pos_y < width - indent:
                    i = (pos_y - header) // 16
                    j = (pos_x - indent) // 16
                    print(i, j)
                    print(test.main_matrix[i][j])
                    unveil(i, j)
                    check_matrix = np.zeros((rows + 2, cols + 2), dtype=int)
                    unveil_neighbours(check_matrix, i, j)

        pygame.display.update()


# game_intro()
main()
