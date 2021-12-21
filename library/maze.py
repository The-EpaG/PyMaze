TEXT      = 0
CODE      = 1
COLOR     = 2

ELEMENT   = {
    'Free':    [' ', 0, [255, 255, 255]],
    'Wall':    ['+', 1, [0,   0,   0  ]],
    'Player':  ['➤', 2, [0,   255, 0  ]],
    'End':     ['⚑', 3, [255, 0,   0  ]]
    }

DIRECTION = {
    'Forward':  ( 0,  1),
    'Right':    ( 1,  0),
    'Backards': ( 0, -1),
    'Left':     (-1,  0)
    }

class Maze():
    def __init__(self, maze:any) -> None:
        if isinstance(maze, str):
            maze = strToList(maze)

        self.height = len(maze)
        self.weight = len(maze[0])

        self.maze = maze

        self.player = (0, 0)
        self.end    = (0, 0)

        for line in range(self.height):
            for row in range(self.weight):
                if maze[line][row] == ELEMENT['Player'][CODE]:
                    self.player = (line, row)
                elif maze[line][row] == ELEMENT['End'][CODE]:
                    self.end = (line, row)

    def add(self, direction:tuple) -> tuple:
        return self.player[0] + direction[0], self.player[1] + direction[1]

    def isAPossibleMoves(self, coor:tuple) -> bool:
        if coor[0] < 0 or coor[1] < 0:
            return False
        if coor[0] == self.height or coor[1] == self.weight:
            return False
        if self.maze[coor[0]][coor[1]] == ELEMENT['Free'][CODE] or self.maze[coor[0]][coor[1]] == ELEMENT['End'][CODE]:
            return True

    def allPossibleMoves(self) -> list:
        moves = {'Forward': False, 'Right': False, 'Backards': False, 'Left': False}

        if self.isAPossibleMoves(self.add(DIRECTION['Forward'])):
            moves["Forward"] = True
        if self.isAPossibleMoves(self.add(DIRECTION['Right'])):
            moves["Right"] = True
        if self.isAPossibleMoves(self.add(DIRECTION['Backards'])):
            moves["Backards"] = True
        if self.isAPossibleMoves(self.add(DIRECTION['Left'])):
            moves["Left"] = True
        
        return moves
    
    def move(self, direction:tuple) -> bool:
        direction = DIRECTION[direction]
        coor      = self.add(direction)

        if self.isAPossibleMoves(coor):
            self.maze[coor[0]][coor[1]] = ELEMENT['Player'][CODE]
            self.maze[self.player[0]][self.player[1]] = ELEMENT['Free'][CODE]

            self.player = coor
            return True
        return False
    
    def isAWin(self) -> bool:
        if self.player[0] == self.end[0] and self.player[1] == self.end[1]:
            return True
        return False

    def __str__(self) -> str:
        s = listToStr(self.maze)
        return s[:-1]

def strToList(string:str) -> list:
        string = string.splitlines()

        height = len(string)
        weight = len(string[0])

        maze = []

        for line in range(height):
            maze.append([])
            for row in range(weight):
                if string[line][row] == ELEMENT['Free'][TEXT]:
                    maze[line].append(ELEMENT['Free'][CODE])
                elif string[line][row] == ELEMENT['Wall'][TEXT]:
                    maze[line].append(ELEMENT['Wall'][CODE])
                elif string[line][row] == ELEMENT['Player'][TEXT]:
                    maze[line].append(ELEMENT['Player'][CODE])
                elif string[line][row] == ELEMENT['End'][TEXT]:
                    maze[line].append(ELEMENT['End'][CODE])
        return maze

def pngToStr(filename:str) -> str:
    from PIL import Image
    import numpy

    image = Image.open(filename)
    image = image.convert(mode='L')

    weight, height = image.size

    data = numpy.asarray(image)

    string = ''

    for i in range(height):
        for j in range(weight):
            if data[i][j] == ELEMENT['Free'][COLOR]:
                string += ELEMENT['Free'][TEXT]
            elif data[i][j] == ELEMENT['Wall'][COLOR]:
                string += ELEMENT['Wall'][TEXT]
            elif data[i][j] == ELEMENT['Player'][COLOR]:
                string += ELEMENT['Player'][TEXT]
            elif data[i][j] == ELEMENT['End'][COLOR]:
                string += ELEMENT['End'][TEXT]
        string += '\n'

    return string

def pngToList(filename:str) -> list:
    from PIL import Image
    import numpy

    image = Image.open(filename)

    weight, height = image.size

    data = numpy.asarray(image).tolist()

    for i in range(height):
        for j in range(weight):
            print(data[i][j] == [0,0,0])
            if data[i][j] == ELEMENT['Free'][COLOR]:
                data[i][j] = ELEMENT['Free'][CODE]
            elif data[i][j] == ELEMENT['Wall'][COLOR]:
                data[i][j] = ELEMENT['Wall'][CODE]
            elif data[i][j] == ELEMENT['Player'][COLOR]:
                data[i][j] = ELEMENT['Player'][CODE]
            elif data[i][j] == ELEMENT['End'][COLOR]:
                data[i][j] = ELEMENT['End'][CODE]
    return data

def listToStr(maze:list) -> str:
    height = len(maze)
    weight = len(maze[0])

    string = ''

    for i in range(height):
        for j in range(weight):
            if maze[i][j] == ELEMENT['Free'][CODE]:
                string += ELEMENT['Free'][TEXT]
            elif maze[i][j] == ELEMENT['Wall'][CODE]:
                string += ELEMENT['Wall'][TEXT]
            elif maze[i][j] == ELEMENT['Player'][CODE]:
                string += ELEMENT['Player'][TEXT]
            elif maze[i][j] == ELEMENT['End'][CODE]:
                string += ELEMENT['End'][TEXT]
        string += '\n'

    return string