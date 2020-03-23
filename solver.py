import pygame as pg
import pygame.freetype as freetype
from pygame import *

# Empty Board
# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

# Easy Example
# board = [
#     [6, 0, 0, 0, 5, 0, 0, 4, 1],
#     [0, 5, 4, 0, 0, 8, 0, 3, 0],
#     [7, 0, 3, 0, 9, 0, 0, 0, 8],
#     [2, 4, 0, 0, 0, 1, 0, 6, 5],
#     [0, 0, 7, 0, 0, 0, 2, 0, 0],
#     [5, 6, 0, 9, 0, 0, 0, 7, 3],
#     [1, 0, 0, 0, 7, 0, 3, 0, 4],
#     [0, 8, 0, 5, 0, 0, 7, 9, 0],
#     [3, 7, 0, 0, 4, 0, 0, 0, 2]
# ]

# Harder Example
board = [
    [9, 0, 3, 8, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 4, 0, 5, 0, 0],
    [0, 0, 2, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 7, 4, 6, 8],
    [0, 0, 0, 6, 0, 9, 0, 0, 0],
    [2, 7, 6, 4, 0, 0, 0, 0, 9],
    [0, 0, 0, 0, 0, 0, 8, 0, 0],
    [0, 0, 1, 0, 2, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 5, 7, 0, 6]
]

# Possible numbers on the game board
nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}

# Game logic

def getRow(index):
    return board[index]

def getCol(index):
    return list(list(zip(*board))[index])

def getBox(index):
    (row, col) = boxToCoords(index)
    return getBoxFromCoords(row, col)

def getBoxFromCoords(x, y):
    out = []
    (row, col) = boxToCoords(coordsToBox(x, y)) # Convert any coords to top left of box
    for i in range(row, row+3):
        for j in range (col, col+3):
            out.append(board[i][j])

    return out

def isValidRow(index):
    seen = set()
    for i in board[index]:
        if (i != 0 and i in seen): return False
        seen.add(i)
    return True

def isCompleteRow(index):
    return board[index].count(0) == 0

def isValidCol(index):
    seen = set()
    for i in list(zip(*board))[index]:
        if (i != 0 and i in seen): return False
        seen.add(i)
    return True

def isCompleteCol(index):
    return list(zip(*board))[index].count(0) == 0
    
def isValidBox(index):
    (row, col) = boxToCoords(index)
    seen = set()

    for i in range(row, row+3):
        for j in range(col, col+3):
            if (board[i][j] != 0 and board[i][j] in seen): return False
            seen.add(board[i][j])
    return True

def isCompleteBox(index):
    (row, col) = boxToCoords(index)
    for i in range(row, row+3):
        for j in range(col, col+3):
            if (board[i][j] == 0): return False
    return True

def coordsToBox(i, j):
    return (j // 3) + 3 * (i//3)

# Return coordinates of top left of box
def boxToCoords(index):
    row = 3 * (index // 3)
    col = 3 * (index % 3)
    return (row, col)

def getValidNums(i, j):
    return nums - set(getRow(i)) - set(getCol(j)) - set(getBoxFromCoords(i, j))

def squareIsValid(i, j):
    return isValidRow(i) and isValidCol(j) and isValidBox(coordsToBox(i, j))

def isValidBoard():
    curr = True
    for i in range(len(board)):
        curr = curr and isValidBox(i) and isValidCol(i) and isValidRow(i)

    return curr

def nextSquare(i, j):
    if (j + 1 > 8 and i + 1 > 8): return (-1,-1) # End of board case
    if (j + 1 > 8): return (i + 1, 0)
    return (i, j + 1)

def hasNextSquare(i, j):
    return not (i == 8 and j == 8)

def solve(ui=False):
    solveHelper(0, 0, 0, ui=ui)

def solveHelper(i, j, numsIndex, ui=False):
    nums = list(getValidNums(i, j))
    # print(i, j, nums)

    if (hasNextSquare(i, j)):
        if (board[i][j] == 0):
            if (numsIndex >= len(nums)): return False # Cannot proceed, must backtrack
            board[i][j] = nums[numsIndex]

            if ui:
                drawCell(i, j)

            (nextI, nextJ) = nextSquare(i, j)
            if (not solveHelper(nextI, nextJ, 0, ui)):
                board[i][j] = 0
                return solveHelper(i, j, numsIndex + 1, ui)
            else:
                return True # Solution was found?
        else:
            (nextI, nextJ) = nextSquare(i, j)
            return solveHelper(nextI, nextJ, 0, ui)
    else:
        if (board[i][j] == 0): board[i][j] = nums[numsIndex]
        return True # Solved sudoku board

# UI
def drawBoxes(color):
    size = boxSize
    box = Rect(0, 0, size, size)

    for i in range(3):
        for j in range(3):
            box.left = j * box.width
            box.top = i * box.height
            pg.draw.rect(screen, color, box, 2)

def drawCells(color):
    size = cellSize
    cell = Rect(0, 0, size, size)

    for i in range(9):
        for j in range(9):
            cell.left = j * cell.width
            cell.top = i * cell.height
            pg.draw.rect(screen, color, cell, 2)

            # Draw values
            font = freetype.SysFont('arial', size)
            value = ""
            if board[i][j] != 0: value = str(board[i][j]) 
            font.render_to(screen, (j * size + (size // 4), i * size + (size // 8)), value, color)

def drawCell(i, j):
    size = cellSize
    color = cellColor
    fontColor = solvedColor

    cell = Rect(0, 0, size, size)
    cell.left = j * cell.width
    cell.top = i * cell.height
    pg.draw.rect(screen, white, cell, 0)
    pg.draw.rect(screen, color, cell, 2)
    drawBoxes(red)

    # Draw values
    font = freetype.SysFont('arial', size)
    value = ""
    if board[i][j] != 0: value = str(board[i][j]) 
    font.render_to(screen, (j * size + (size // 4), i * size + (size // 8)), value, fontColor)

    pg.display.update()
    # pg.time.Clock().tick(60)

def clearCell(i, j):
    size = cellSize
    color = cellColor

    cell = Rect(0, 0, size, size)
    cell.left = j * cell.width
    cell.top = i * cell.height
    pg.draw.rect(screen, white, cell, 0)
    pg.draw.rect(screen, color, cell, 2)
    drawBoxes(red)

    pg.display.update()
    # pg.time.Clock().tick(60)
            
if __name__ == "__main__":
    # Initialization
    pg.init()
    gameWidth = 450 # Make sure divisible by 9
    gameHeight = 450
    screenWidth = gameWidth + gameWidth // 5 # 120% of gameWidth for input, buttons, etc.
    pg.display.set_caption('Sudoku Solver')
    # global screen
    screen = pg.display.set_mode((screenWidth,gameHeight))
    # TODO: Set title of window
    screen.fill(Color('white'))

    # Colors
    black = Color('black')
    red = Color('red')
    blue = Color('blue')
    white = Color('white')

    # Constants
    cellSize = gameWidth // 9
    boxSize = gameWidth // 3
    cellColor = black
    boxColor = red
    givenColor = black
    solvedColor = blue

    # Objects
    solveText = "Solve!"
    solveFont = freetype.SysFont('arial', gameHeight // 20)
    solvePos = (gameWidth + 10, gameHeight // 2)
    solveRect = solveFont.get_rect(solveText)
    solveRect = solveRect.inflate(10, 10)
    solveRect.centery = solvePos[1] + 5
    solveRect.left = solvePos[0] - 5

    # Draw elements
    drawCells(black)
    drawBoxes(red)
    pg.draw.rect(screen, red, solveRect)
    solveFont.render_to(screen, solvePos, solveText, black)

    pg.display.update()

    running = True
    while running:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                running = False
                pg.quit()
            if i.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = i.pos  # gets mouse position

                # Clicked on Solve button
                if solveRect.collidepoint(mouse_pos):
                    # prints current location of mouse
                    # UI Info: (cell size, cell color, font color)
                    solve(ui=True) # Blocks other UI updates
                    # drawCells(black)
                    # drawBoxes(red)

        if not running: break
        pg.display.update()

    # Text based solving
    # print(board)
    # solve()
    # print(board)
    # print(isValidBoard())
