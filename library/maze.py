TEXT      = 0
CODE      = 1
COLOR     = 2

ELEMENT   = {
    'Free':    [' ', 0, [255, 255, 255]],
    'Wall':    ['+', 1, [0,   0,   0  ]],
    'Player':  ['➤', 2, [0,   255, 0  ]],
    'End':     ['⚑', 3, [255, 0,   0  ]],
    'View':    ['•', 4, [255, 0,   255]],
    'Current': ['△', 5, [255, 255, 0  ]]
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

def genMazeList(dim:int) -> list:
    class Cell():
        TOP    = 0
        RIGHT  = 1
        BOTTOM = 2
        LEFT   = 3

        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y

            self.walls   = [True, True, True, True]
            self.visited = False

        def draw(self):
            l = [ 
                    [ELEMENT['Wall'][CODE], ELEMENT['Free'][CODE], ELEMENT['Wall'][CODE]],
                    [ELEMENT['Free'][CODE], ELEMENT['Free'][CODE], ELEMENT['Free'][CODE]],
                    [ELEMENT['Wall'][CODE], ELEMENT['Free'][CODE], ELEMENT['Wall'][CODE]]
                ]

            if self.walls[self.TOP]:
                l[0][1] = ELEMENT['Wall'][CODE]
            if self.walls[self.RIGHT]:
                l[1][2] = ELEMENT['Wall'][CODE]
            if self.walls[self.BOTTOM]:
                l[2][1] = ELEMENT['Wall'][CODE]
            if self.walls[self.LEFT]:
                l[1][0] = ELEMENT['Wall'][CODE]

            return l
        
        def visit(self) -> None:
            self. visited = True

    def render(cells:list, startCoor:tuple, endCoor:tuple) -> list:
        grid  = []

        # Create Grid
        for i in range(len(cells) * 2 + 1):
            grid.append([])
            for j in range(len(cells[0]) * 2 + 1):
                grid[i].append(None)

        # Render cells on Grids
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                cell     = cells[i][j]
                cellDraw = cell.draw()

                for n in range(len(cellDraw)):
                    for m in range(len(cellDraw[0])):
                        grid[(cell.y * 2) + n][(cell.x * 2) + m] = cellDraw[n][m]
        
        grid[(startCoor[1] * 2) + 1][(startCoor[0] * 2) + 1] = ELEMENT['Player' ][CODE]
        grid[(endCoor[1] * 2) + 1][(endCoor[0] * 2) + 1]     = ELEMENT['End'    ][CODE]

        return grid

    def checkNeighbors(cells:list, current:Cell) -> list:
        neighbors = []

        if current.y > 0 :
            neighbors.append(cells[current.x][current.y - 1])
        if current.x < len(cells) - 1:
            neighbors.append(cells[current.x + 1][current.y])
        if current.y < len(cells[0]) - 1:
            neighbors.append(cells[current.x][current.y + 1])
        if current.x > 0:
            neighbors.append(cells[current.x - 1][current.y])
        
        for neighbor in neighbors.copy():
            if neighbor.visited:
                neighbors.remove(neighbor)
        
        return neighbors

    def choseNeighbors(neighbors:list) -> Cell:
        from random import randint
        return neighbors[randint(0, len(neighbors) - 1)]

    def removeWalls(a:Cell, b:Cell) -> None:
        x = a.x - b.x
        y = a.y - b.y

        if x == -1:         #Right
            a.walls[a.RIGHT]  = False
            b.walls[b.LEFT]   = False
        elif x == 1:        #Left
            a.walls[a.LEFT]   = False
            b.walls[b.RIGHT]  = False
        elif y == 1:        #Top
            a.walls[a.TOP]    = False
            b.walls[b.BOTTOM] = False
        elif y == -1:       #Bottom
            a.walls[a.BOTTOM] = False
            b.walls[b.TOP]    = False

    cells = []
    dim   = int(dim/2)

    current = None
    step    = []

    distance    = 0
    maxDistance = 0
    endCoor     = (0, 0)
    startCoor   = (0, 0)

    cellsLeft = dim * dim - 1

    # Create cells
    for i in range(dim):
        cells.append([])
        for j in range(dim):
            cells[i].append(Cell(i, j))

    current = cells[startCoor[0]][startCoor[1]]
    current.visit()

    while cellsLeft > 0:
        neighbors = checkNeighbors(cells, current)
        while len(neighbors) > 0:
            step.append(current)

            next = choseNeighbors(neighbors)
            next.visit()
            cellsLeft -= 1
            removeWalls(current, next)

            current = next
            neighbors = checkNeighbors(cells, current)

            distance += 1

        if len(step) > 0:
            if distance > maxDistance:
                maxDistance = distance
                endCoor = (current.x, current.y)
            distance -= 1

            current = step.pop()
    return render(cells, startCoor, endCoor)

def strToPng(string:str, filename='maze.png') -> None:
    from PIL import Image
    from numpy import asarray, uint8

    string = string.splitlines()

    height = len(string)
    weight = len(string[0])

    maze = []

    for row in range(weight):
        maze.append([])
        for col in range(height):
            if string[row][col] == ELEMENT['Free'][TEXT]:
                maze[row].append(ELEMENT['Free'][COLOR])
            elif string[row][col] == ELEMENT['Wall'][TEXT]:
                maze[row].append(ELEMENT['Wall'][COLOR])
            elif string[row][col] == ELEMENT['Player'][TEXT]:
                maze[row].append(ELEMENT['Player'][COLOR])
            elif string[row][col] == ELEMENT['End'][TEXT]:
                maze[row].append(ELEMENT['End'][COLOR])
                

    image = Image.fromarray(asarray(maze).astype(uint8))
    image.save(filename)

def listToPng(maze:list, filename='maze.png') -> None:
    from PIL import Image
    from numpy import asarray, uint8


    height = len(maze)
    weight = len(maze[0])

    export = []

    for row in range(weight):
        export.append([])
        for col in range(height):
            if maze[row][col] == ELEMENT['Free'][CODE]:
                export[row].append(ELEMENT['Free'][COLOR])
            elif maze[row][col] == ELEMENT['Wall'][CODE]:
                export[row].append(ELEMENT['Wall'][COLOR])
            elif maze[row][col] == ELEMENT['Player'][CODE]:
                export[row].append(ELEMENT['Player'][COLOR])
            elif maze[row][col] == ELEMENT['End'][CODE]:
                export[row].append(ELEMENT['End'][COLOR])
                
    image = Image.fromarray(asarray(export).astype(uint8))
    image.save(filename)

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