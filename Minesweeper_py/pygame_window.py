import pygame
from mine_board import *
import sys

# ------------------------------------------------ Recursion settings ------------------------------------------------ #

"""
    I found out that I can raise the limit or recursions using the commands below. 
    This is useful to me since I'm using recursion in order to unveil the board.
"""

sys.setrecursionlimit(1500)
print(sys.getrecursionlimit())

pygame.init()

# ------------------------------------------------------ Colors ------------------------------------------------------ #

black = (0, 0, 0)
grey = (160, 160, 160)

red = (200, 0, 0)
bright_red = (255, 0, 0)

green = (0, 200, 0)
bright_green = (0, 255, 0)

bright_yellow = (255, 255, 102)
yellow = (255, 255, 0)

orange = (255, 160, 0)
bright_orange = (255, 205, 0)

# ------------------------------------------------------ Images -------------------------------------------------------#

"""
    Using some images to make the game more attractive.
"""

block1 = pygame.image.load("Images/block1.png")
block2 = pygame.image.load("Images/block2.png")
block3 = pygame.image.load("Images/block3.png")
block4 = pygame.image.load("Images/block4.png")
block5 = pygame.image.load("Images/block5.png")
block6 = pygame.image.load("Images/block6.png")
block7 = pygame.image.load("Images/block7.png")
block8 = pygame.image.load("Images/block8.png")
empty = pygame.image.load("Images/blankblock1.png")
blank = pygame.image.load("Images/blankblock.png")
bomb = pygame.image.load("Images/bomb.png")
flag = pygame.image.load("Images/flag.png")
no_bomb = pygame.image.load("Images/non-bomb.png")
bg = pygame.image.load("Images/bg.png")

# ----------------------------------------------- FIRST INITIALIZATION ----------------------------------------------- #
"""
    These are the first initializations for the number of rows, columns, number of bombs and size of the blocks 
    images. The user will be able to change them in the game. 
"""

rows, cols, no_of_bombs = 20, 25, 45  # setup_board() minim 23 pt max 24 x 34
square_size = 16
indent = 50
header = 50
minutes = 0
seconds = 15
aux_min = 0
aux_sec = 15
clickable = True
font = pygame.font.Font(None, 25)

# ---------------------------------------------------- MAIN MENU ----------------------------------------------------- #

"""
    The next 2 functions helped me create a button when in need very quickly. The function "button"
    has arguments for the message, the coordinates in the window, two colors and the most important,
    its function (action). The first function helps the second one in create the font for the text.
    These 2 function were implemented from : https://pythonprogramming.net/pygame-buttons-part-1-button-rectangle/.
"""


def text_objects(text, font_):
    textSurface = font_.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, width_button, height_button, regular_color, pressed_color, choosen_window, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width_button > mouse[0] > x and y + height_button > mouse[1] > y:
        pygame.draw.rect(choosen_window, pressed_color, (x, y, width_button, height_button))
        if click[0] == 1:
            action()
    else:
        pygame.draw.rect(choosen_window, regular_color, (x, y, width_button, height_button))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (width_button / 2)), (y + (height_button / 2)))
    choosen_window.blit(textSurf, textRect)


"""
    The next 16 functions are the functionality of the buttons from the main menu so that the
    player will be able to raise or lower the number of rows, cols, mines, minutes and seconds.
"""


def C_plus_10():
    global cols
    if cols + 10 < 31:
        cols += 10
    else:
        cols = 30
    print(cols)


def C_plus_1():
    global cols
    if cols + 1 < 31:
        cols += 1
    print(cols)


def R_plus_10():
    global rows
    if rows + 10 < 25:
        rows += 10
    else:
        rows = 24
    print(rows)


def R_plus_1():
    global rows
    if rows + 1 < 25:
        rows += 1
    print(rows)


def M_plus_10():
    global no_of_bombs
    if no_of_bombs + 10 < 100:
        no_of_bombs += 10
    else:
        no_of_bombs = 100
    print(no_of_bombs)


def M_plus_1():
    global no_of_bombs
    if no_of_bombs + 1 < 100:
        no_of_bombs += 1
    print(no_of_bombs)


def C_minus_10():
    global cols
    if cols - 10 > 8:
        cols -= 10
    else:
        cols = 9
    print(cols)


def C_minus_1():
    global cols
    if cols - 1 > 8:
        cols -= 1
    print(cols)


def R_minus_10():
    global rows
    if rows - 10 > 8:
        rows -= 10
    else:
        rows = 9
    print(rows)


def R_minus_1():
    global rows
    if rows - 1 > 8:
        rows -= 1
    print(rows)


def M_minus_10():
    global no_of_bombs
    if no_of_bombs - 10 > 5:
        no_of_bombs -= 10
    else:
        no_of_bombs = 6
    print(no_of_bombs)


def M_minus_1():
    global no_of_bombs
    if no_of_bombs - 1 > 5:
        no_of_bombs -= 1
    print(no_of_bombs)


def min_plus_1():
    global minutes, aux_min
    if minutes < 9:
        minutes += 1
        aux_min = minutes
    print(minutes)


def sec_plus_1():
    global seconds, aux_sec
    ok = True
    if seconds == 59:
        seconds = 0
        aux_sec = seconds
        ok = False
    if seconds < 59 and ok is True:
        seconds += 1
        aux_sec = seconds

    print(seconds)


def min_minus_1():
    global minutes, aux_min
    if minutes > 0:
        minutes -= 1
        aux_min = minutes
    print(minutes)


def sec_minus_1():
    global seconds, aux_sec
    if seconds > 0:
        seconds -= 1
        aux_sec = seconds
    if seconds == 0:
        seconds = 59
        aux_sec = seconds
    print(seconds)


def set_time():
    global minutes, seconds, aux_min, aux_sec
    minutes = aux_min
    seconds = aux_sec


"""
    The "no_of_mines_protection" function keeps the game from crashing. In order to function correctly,
    the number of mines always has to smaller than the product between the number of rows and cols. So
    if the user, willingly or unwillingly, chooses to have more than the permitted amount of mines, the 
    program will lower the number.

"""


def no_of_mines_protection():
    global no_of_bombs, rows, cols
    if rows * cols < no_of_bombs:
        no_of_bombs = (rows - 1) * (cols - 1)
    print("Protection:", no_of_bombs)


"""
    These are 3 presets for difficulty (Easy, Medium, Hard).
"""


def diff_beg():
    global no_of_bombs, rows, cols, minutes, seconds
    rows = 9
    cols = 9
    no_of_bombs = 10
    minutes = 0
    seconds = 30


def diff_medium():
    global no_of_bombs, rows, cols, minutes, seconds
    rows = 16
    cols = 16
    no_of_bombs = 40
    minutes = 2
    seconds = 30


def diff_hard():
    global no_of_bombs, rows, cols, minutes, seconds
    rows = 16
    cols = 30
    no_of_bombs = 99
    minutes = 6
    seconds = 0


"""
    Starting the clock.
"""

clock = pygame.time.Clock()

"""
    The "window_setup" functions creates a the playing window. The indent and the header are
    the blank spaces between the walls of the window and the drawn matrix. The program builds
    the height and width of the window taking in the consideration the indent and number of columns
    multiplied by 16 and header and number of rows multiplied by 16. The images are all 17 by 17 
    pixels but I did not like how the final product turned out so I chose to remain with 16. After 
    that, the program creates the window and gives it a grey background.  
"""


def window_setup():
    global height, width, window

    height = indent * 2 + cols * square_size
    width = header * 2 + rows * square_size

    window = pygame.display.set_mode((height, width))
    window.fill(grey)
    pygame.display.get_surface().fill(grey)
    pygame.display.update()


"""
        The main menu of the game resides in the game_intro() function. The main functionality of this menu is that the 
    user can choose the number of rows, columns and bombs. He can either choose from 3 presets with different levels of 
    difficulty or he can create his own version of the game. After he made his choice he can play start and enjoy 
    the game. 
        I created a new window (intro_window) this time with a fixes resolution. I started a while loop where the 
    program loads a background, checks for the QUIT event, loads the buttons from where it is possible to change the 
    parameters of the game, updating them and showing them. I made the buttons using the previously presented function. 
    The start button is different because is created "manually".If the buttons is pressed the While loop is stopped and 
    the main game window stars running. 
"""


def game_intro():
    global window_intro

    set_time()
    window_intro = pygame.display.set_mode((500, 500))

    intro_font = pygame.font.SysFont('cambriacambriamath', 30)
    intro = True

    while intro:
        window_intro.blit(bg, (0, 0))
        mouse_intro = pygame.mouse.get_pos()
        click_intro = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        text = intro_font.render("COLUMN", True, black)
        window_intro.blit(text, (10, 110))
        text = intro_font.render("ROWS", True, black)
        window_intro.blit(text, (10, 185))
        text = intro_font.render("MINES", True, black)
        window_intro.blit(text, (10, 260))
        text = intro_font.render("TIME", True, black)
        window_intro.blit(text, (10, 335))

        button("-10", 150, 100, 50, 50, green, bright_green, window_intro, C_minus_10)
        button("-10", 150, 175, 50, 50, green, bright_green, window_intro, R_minus_10)
        button("-10", 150, 250, 50, 50, green, bright_green, window_intro, M_minus_10)
        button("-1m", 150, 325, 50, 50, green, bright_green, window_intro, min_minus_1)

        button("-1", 225, 100, 50, 50, green, bright_green, window_intro, C_minus_1)
        button("-1", 225, 175, 50, 50, green, bright_green, window_intro, R_minus_1)
        button("-1", 225, 250, 50, 50, green, bright_green, window_intro, M_minus_1)
        button("-1s", 225, 325, 50, 50, green, bright_green, window_intro, sec_minus_1)

        text_cols = intro_font.render(str(cols), True, black)
        text_rows = intro_font.render(str(rows), True, black)
        text_mines = intro_font.render(str(no_of_bombs), True, black)

        font_time = pygame.font.SysFont('cambriacambriamath', 30)
        time_intro = "{0:01}:{1:02}".format(minutes, seconds)
        text_time = font_time.render(time_intro, True, black)

        window_intro.blit(text_cols, (300, 110))
        window_intro.blit(text_rows, (300, 185))
        window_intro.blit(text_mines, (300, 260))
        window_intro.blit(text_time, (285, 330))

        button("+1", 355, 100, 50, 50, green, bright_green, window_intro, C_plus_1)
        button("+1", 355, 175, 50, 50, green, bright_green, window_intro, R_plus_1)
        button("+1", 355, 250, 50, 50, green, bright_green, window_intro, M_plus_1)
        button("+1s", 355, 325, 50, 50, green, bright_green, window_intro, sec_plus_1)

        button("+10", 430, 100, 50, 50, green, bright_green, window_intro, C_plus_10)
        button("+10", 430, 175, 50, 50, green, bright_green, window_intro, R_plus_10)
        button("+10", 430, 250, 50, 50, green, bright_green, window_intro, M_plus_10)
        button("+1m", 430, 325, 50, 50, green, bright_green, window_intro, min_plus_1)

        button("Easy", 70, 30, 80, 50, yellow, bright_yellow, window_intro, diff_beg)
        button("Medium", 200, 30, 80, 50, orange, bright_orange, window_intro, diff_medium)
        button("Hard", 330, 30, 80, 50, red, bright_red, window_intro, diff_hard)

        x_button = 200
        y_button = 425
        width_button = 70
        height_button = 50

        if x_button + width_button > mouse_intro[0] > x_button and y_button + height_button > mouse_intro[1] > y_button:
            # print(mouse_intro)
            pygame.draw.rect(window_intro, bright_green, (x_button, y_button, width_button, height_button))
            if click_intro[0] == 1:
                no_of_mines_protection()
                intro = False
        else:
            pygame.draw.rect(window_intro, green, (x_button, y_button, width_button, height_button))

        startText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Start", startText)
        textRect.center = (x_button + width_button // 2, y_button + height_button // 2)
        window_intro.blit(textSurf, textRect)
        pygame.display.update()
        clock.tick(10)


# -------------------------------------------------- TIME ------------------------------------------------------------ #
"""
    In order to have a countdown timer, I created the function time() which measures time. Each tick, the frame_count
    is incremented and so, the program manages to keep tabs on the minutes and seconds. Then, it's placed in the 
    top-left corner of the game window. 
"""

frame_count = 0


def time(unveil_Matrix):
    global minutes, seconds, frame_count

    times_up = False
    if no_of_tiles_revealed(unveil_Matrix) != 0 and clickable is True:
        if seconds < 60 and frame_count % 60 == 0:
            seconds -= 1
            frame_count /= 60

        elif seconds == 0:
            minutes -= 1
            seconds += 60

        frame_count += 1

    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
    font_time = pygame.font.Font(None, 25)
    text = font_time.render(output_string, True, black)
    window.blit(text, [width // 25, 25])

    clock.tick(60)
    pygame.display.flip()


# ------------------------------------------------- BLOCKS ----------------------------------------------------------- #

"""
    The blocks related functions functions are very simple and they only placed the images on the X and Y coordonates
    depending on the first argument of the function. So for 1 to 8 there are unveiled numbered blocks, f stands for 
    flag, b for a hidden block, w for a crossed bomb (in case the user choose to place a flag where a there was no bomb),
    0 is for an empty block and finally bombs.
"""


def block(x, y, blockImg):
    window.blit(blockImg, (x, y))


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
    elif val == 'f':
        block(x, y, flag)
    elif val == 'b':
        block(x, y, blank)
    elif val == 'w':
        block(x, y, no_bomb)
    elif val == 0:
        block(x, y, empty)
    else:
        block(x, y, bomb)


# -------------------------------------------------- FUNCTIONALITY --------------------------------------------------- #
# ~ BLOCKS ~ #

"""
    First and foremost, after the game window has been initialized, it's time for the init_game function to create the
    graphical matrix with all its blank blocks (the initial blocks). The function passes through the whole matrix and 
    and "draws" a blank tile. While passing, the function also adds the square_size to the coordinates and so it can
    calculate the exact position the block can be placed.
"""


def init_game():
    y = header  # we start at the top of the screen
    for i in range(0, rows):
        x = indent  # for every row we start at the left of the screen again
        for j in range(0, cols):
            block(x, y, blank)
            x += square_size  # for ever item/number in that row we move one "step" to the right
        y += square_size  # for every new row we move one "step" downwards
    pygame.display.update()


"""
    check_indexes is a simple function that returns True if i and j can be found inside the matrix, otherwise it returns
    False.
"""


def check_indexes(i, j):
    if i >= 0 and i <= rows and j >= 0 and j <= cols:
        return True
    return False


"""
        I believe that the unveil_neighbours function is the most important one from a functional point of view. It is a
    recursive function. As arguments, it receives a matrix called check_matrix and the coordinates in that matrix.
    check_matrix is a matrix full of zeros. When the program calls this function, it first checks to see if under the
    blank block (the initial blocks) there is an empty one (only empty blocks can be revealed in groups). If it is, then 
    it checks the check_matrix value for the neighbouring blocks (maximum 8 neighbours; if it's 0 the function did not 
    pass through that block, if it's 1, it did), then checks to see if m_i and m_j are valid clicks (within the matrix) 
    and finally, if there is a flag, it will not switch to a revealed block.
        After the condition, it marks the value from the matrix with 1 and then proceeds to recall the function. As I
    said before, it does this for its neighbours and stops only when it reached the exterior columns and rows or its
    current value is circled by only values of 1 or there is a flag placed by the player there.
        All things mentioned above happen only if the tiles under the hidden blocks are empty tiles (with no numbers),
    but this function can also be called if the player clicked on a numbered block. In this case, it will change only
    one value in the check_matrix.

"""


def unveil_neighbours(check_Matrix, m_i, m_j, flag_Matrix, main_Matrix):
    if main_Matrix[m_i][m_j] == 0:

        if check_indexes(m_i - 1, m_j - 1) is True:
            if check_Matrix[m_i - 1][m_j - 1] == 0 and flag_Matrix[m_i - 1][m_j - 1] == 0:
                check_Matrix[m_i - 1][m_j - 1] = 1
                unveil_neighbours(check_Matrix, m_i - 1, m_j - 1, flag_Matrix, main_Matrix)

        if check_indexes(m_i - 1, m_j) is True:
            if check_Matrix[m_i - 1][m_j] == 0 and flag_Matrix[m_i - 1][m_j] == 0:
                check_Matrix[m_i - 1][m_j] = 1
                unveil_neighbours(check_Matrix, m_i - 1, m_j, flag_Matrix, main_Matrix)

        if check_indexes(m_i - 1, m_j + 1) is True:
            if check_Matrix[m_i - 1][m_j + 1] == 0 and flag_Matrix[m_i - 1][m_j + 1] == 0:
                check_Matrix[m_i - 1][m_j + 1] = 1
                unveil_neighbours(check_Matrix, m_i - 1, m_j + 1, flag_Matrix, main_Matrix)

        if check_indexes(m_i, m_j - 1) is True:
            if check_Matrix[m_i][m_j - 1] == 0 and flag_Matrix[m_i][m_j - 1] == 0:
                check_Matrix[m_i][m_j - 1] = 1
                unveil_neighbours(check_Matrix, m_i, m_j - 1, flag_Matrix, main_Matrix)

        if check_indexes(m_i, m_j + 1) is True:
            if check_Matrix[m_i][m_j + 1] == 0 and flag_Matrix[m_i][m_j + 1] == 0:
                check_Matrix[m_i][m_j + 1] = 1
                unveil_neighbours(check_Matrix, m_i, m_j + 1, flag_Matrix, main_Matrix)

        if check_indexes(m_i + 1, m_j - 1):
            if check_Matrix[m_i + 1][m_j - 1] == 0 and flag_Matrix[m_i + 1][m_j - 1]:
                check_Matrix[m_i + 1][m_j - 1] = 1
                unveil_neighbours(check_Matrix, m_i + 1, m_j - 1, flag_Matrix, main_Matrix)

        if check_indexes(m_i + 1, m_j) is True:
            if check_Matrix[m_i + 1][m_j] == 0 and flag_Matrix[m_i + 1][m_j] == 0:
                check_Matrix[m_i + 1][m_j] = 1
                unveil_neighbours(check_Matrix, m_i + 1, m_j, flag_Matrix, main_Matrix)

        if check_indexes(m_i + 1, m_j + 1) is True:
            if check_Matrix[m_i + 1][m_j + 1] == 0 and flag_Matrix[m_i + 1][m_j + 1] == 0:
                check_Matrix[m_i + 1][m_j + 1] = 1
                unveil_neighbours(check_Matrix, m_i + 1, m_j + 1, flag_Matrix, main_Matrix)

    elif main_Matrix[m_i][m_j] != 9:
        check_Matrix[m_i][m_j] = 1


"""
    The next function, unveil_check_matrix, "shows" graphically what happens with the matrix and will switch the blank
    squares for numbered ones using the check_matrix that was previously updated by unveil_neighbours function.
"""


def unveil_check_matrix(check_matrix, unveil_Matrix, flag_Matrix, main_Matrix):
    y = header
    for i in range(0, rows):
        x = indent
        for j in range(0, cols):
            if check_matrix[i][j] == 1 and flag_Matrix[i][j] == 0 and main_Matrix[i][j] != 9 and unveil_Matrix[i][
                j] == 0:
                block_assignment(main_Matrix[i][j], x, y)
                unveil_Matrix[i][j] = 1

            x += square_size
        y += square_size
    pygame.display.update()


"""
    The function unveil_all_bombs displays all the bombs (as a flag or as a mine) when the player loses the game. It
    checks to see if the coordinates from the list of bombs match with i and j then checks to see if the unveil_matrix
    is 0 and finally if there is no flag on that tile.
"""


def unveil_all_bombs(char, unveil_Matrix, bomb_coords, flag_Matrix):
    y = header
    for i in range(0, rows):
        x = indent
        for j in range(0, cols):
            for x_coord, y_coord in bomb_coords:
                if unveil_Matrix[i][j] == 0 and i == x_coord and j == y_coord and flag_Matrix[i][j] == 0:
                    block_assignment(char, x, y)
                    unveil_Matrix[i][j] = 1
            x += square_size
        y += square_size
    pygame.display.update()


# ~ FLAGS ~ #

"""
    Another part of this game is represented by flags, marks left by the player on different tiles in order to remember
    where the the tiles with the mines under them are. He have the "check_if" variable that is first equal with -1 and 
    this function takes the same path as the ones above. We pass through a flag_matrix this time and check if its value
    is 0 and the value from the unveil_matrix is also 0 (the player can place a flag if and only if the square is blank,
    it's not pressed), then we can place a flag, and check_if is 1. Otherwise, if there is already a flag on that tile, 
    we can remove it and change the value in the flag_matrix. Finally, we return check_if (0 if it removed a flag, 1
    if it placed one).

"""


def place_flag(m_i, m_j, unveil_Matrix, flag_Matrix):
    check_if = -1
    y = header
    for i in range(0, rows):
        x = indent
        for j in range(0, cols):
            if i == m_i and j == m_j and unveil_Matrix[m_i][m_j] == 0:
                if flag_Matrix[m_i][m_j] == 0 and check_if == -1:
                    flag_Matrix[m_i][m_j] = 1
                    block_assignment('f', x, y)
                    check_if = 1
                if flag_Matrix[m_i][m_j] == 1 and check_if == -1:
                    block_assignment('b', x, y)
                    flag_Matrix[m_i][m_j] = 0
                    check_if = 0

            x += square_size
        y += square_size

    print(flag_Matrix)
    print(m_i, m_j)
    pygame.display.update()
    return check_if


"""
    The player is bound to do mistakes by placing the flags on non-bombs tiles and clicking on a bomb thinking is a 
    numbered square. When that happens, the game is over and the player lost; also the wrong_flag function is called 
    and switches the flags for crossed bombs.
"""


def wrong_flag(m_i, m_j, unveil_Matrix):
    y = header
    for i in range(0, rows):
        x = indent
        for j in range(0, cols):
            if i == m_i and j == m_j:
                if unveil_Matrix[m_i][m_j] == 0:
                    block_assignment('w', x, y)
                    unveil_Matrix[m_i][m_j] = 1

            x += square_size
        y += square_size
    pygame.display.update()


# ~ WIN ~ #

"""
    The condition to win is for the player to click on all the tiles apart from those which hid bombs underneath them.
    If the player leaves those tiles untouched, he wins. The function win computes first the numbers of "bombless" tiles 
    and compares it with the return value of the no_of_tiles_revealed function (this uses the unveil_matrix to number
    all the values of 1). If the values are equal, variable gameWon turns False and if all the hidden tiles are bombs,
    it remains that way and returns the value.
"""


def win(unveilMatrix, mainMatrix):
    tiles_no_bombs = cols * rows - no_of_bombs
    gameWon = True
    if tiles_no_bombs == no_of_tiles_revealed(unveilMatrix):
        gameWon = False
        for i in range(rows):
            for j in range(cols):
                if unveilMatrix[i][j] == 0 and mainMatrix[i][j] != 9:
                    print(gameWon)
                    gameWon = True
    return gameWon


def no_of_tiles_revealed(unveil_Matrix):
    nr = 0
    for i in range(rows):
        for j in range(cols):
            if unveil_Matrix[i][j] == 1:
                nr += 1
    return nr


# ------------------------------------------------------- MAIN ------------------------------------------------------- #

def main():
    global clickable

    """ Names for the types of mouse buttons """
    LEFT_MB = 1
    RIGHT_MB = 3

    """ Creating the game window """
    window_setup()

    """ Initializing the 3 main matrices used by the program """
    matrix = np.zeros((rows + 1, cols + 1), dtype=int)
    unveil_matrix = np.zeros((rows, cols), dtype=int)  # (0 - hidden, 1 - revealed)
    flag_matrix = np.zeros((rows + 1, cols + 1), dtype=int)  # (0 - no flag, 1 - flag)

    """ Creating an object of type Board and calling the methods """
    board = Board(rows, cols, no_of_bombs, matrix)
    board.place_bombs()
    board.place_numbers()
    board.print_matrix()

    """ Initializing the board (graphically) """
    init_game()
    text = font.render("Flags: " + str(no_of_bombs), True, black)
    window.fill(grey, (width // 2, 0, width, 50))
    window.blit(text, [width * 3 // 4, 25])

    """ Variables """
    remaining_flags = no_of_bombs
    coord_list_flags = []  # list for the coordinates of the flags
    clickable = True  # variable that tells the program if the player can click on the matrix or not
    notQuitGame = True  # variable for the while loop

    while notQuitGame:

        """ Checking for events"""
        for event in pygame.event.get():

            """ Quit event """
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """ Mouse press event """
            if event.type == pygame.MOUSEBUTTONUP:
                """ While the player is still playing """
                if clickable:
                    """ Getting the positions of the mouse """
                    pos_x, pos_y = pygame.mouse.get_pos()
                    # print(pos_x, pos_y)

                    """ Checking if the click happend inside the border of the matrix """
                    if pos_x > header and pos_x < height - header and pos_y > indent and pos_y < width - indent:
                        """ If it did he compute i and j (the coords of the matrices) with these formulas """
                        i = (pos_y - header) // square_size
                        j = (pos_x - indent) // square_size

                        """ If the left mouse button has been pressed we first to check if the flag_matrix is 0"""
                        if event.button == LEFT_MB and flag_matrix[i][j] == 0:
                            """ If it is we create a new matrix that is used as parameter for the unveil_neighbours and 
                                unveil_check_matrix functions """
                            check_matrix = np.zeros((rows + 1, cols + 1), dtype=int)
                            unveil_neighbours(check_matrix, i, j, flag_matrix, board.main_matrix)
                            unveil_check_matrix(check_matrix, unveil_matrix, flag_matrix, board.main_matrix)

                            """ Otherwise if the player clicked on bomb (9) the program will reveal all the bombs,
                                will keep the correct flags on the board and will change the wrong flags for a crossed
                                bomb image. The clickable variable becomes False and the game ends """
                            if board.main_matrix[i][j] == 9:
                                unveil_all_bombs('9', unveil_matrix, board.coord_list, flag_matrix)
                                for (flag_coord1, flag_coord2) in coord_list_flags:
                                    if (flag_coord1, flag_coord2) not in board.coord_list:
                                        wrong_flag(flag_coord1, flag_coord2, unveil_matrix)
                                clickable = False

                        """ If the right mouse button has been pressed the player can place or remove a flag """
                        if event.button == RIGHT_MB:
                            if place_flag(i, j, unveil_matrix, flag_matrix) == 1 and unveil_matrix[i][j] == 0:
                                """ The program checks to see if the coords of the flag are in the list and if they are
                                    not it adds them and decrements the remaining flags """
                                if (i, j) not in coord_list_flags:
                                    remaining_flags -= 1
                                    coord_list_flags.append((i, j))
                            else:
                                """ And here it removes the coords from the list """
                                if (i, j) in coord_list_flags:
                                    remaining_flags += 1
                                    coord_list_flags.remove((i, j))

                            """ In the top-right of the screen a counter with the number of flags will be placed """
                            text = font.render("Flags: " + str(remaining_flags), True, black)
                            window.fill(grey, (width // 2, 0, width, 50))
                            window.blit(text, [width * 3 // 4, 25])
                            print(coord_list_flags)

                        """ Checking to see if the player won the game """
                        if not win(unveil_matrix, board.main_matrix):
                            """ If it did, clickable becomes false and all the bombs become visible """
                            clickable = win(unveil_matrix, board.main_matrix)
                            unveil_all_bombs('f', unveil_matrix, board.coord_list, flag_matrix)
                            text = font.render("YOU WON", True, black)
                            window.blit(text, [width // 2 - 20, height // 2 - 10])

        """ Creating a return to menu button (useful when the player wants to change the difficulty or just restart """
        x_mouse, y_mouse = pygame.mouse.get_pos()
        click_intro = pygame.mouse.get_pressed()
        box_w = 140
        box_h = 30

        if height // 2 + box_w // 2 > x_mouse > height // 2 - box_w // 2 and width - header + box_h > y_mouse > width - header - box_h + 30:
            pygame.draw.rect(window, bright_red,
                             (height // 2 - box_w // 2, width - header + box_h // 2 / 3, box_w, box_h))
            if click_intro[0] == 1:
                notQuitGame = False

        else:
            pygame.draw.rect(window, red, (height // 2 - box_w // 2, width - header + box_h // 2 / 3, box_w, box_h))

        returnText = font.render("Return to menu", True, black)
        window.blit(returnText, (height // 2 - box_w // 2 + 7, width - header + box_h // 2 - 2))

        """ Creating the timer and placing a condtion: in case the time runs out, the player loses """
        window.fill(grey, (0, 0, width // 2, 40))
        time(unveil_matrix)
        if minutes == 0 and seconds == 0:
            clickable = False

        pygame.display.update()


if __name__ == "__main__":
    while 1:
        game_intro()
        main()
