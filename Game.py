from library.maze import Maze, genMazeList, listToPng

FILENAME = 'Example/maze.png'
SAVEFILENAME = 'Example/save.png'

#maze = Maze(pngToList(FILENAME))
maze  = Maze(genMazeList(32))

while not maze.isAWin():
    moves    = maze.allPossibleMoves()
    selected = None

    while not selected in range(len(moves)):
        for _ in range(10):
            print()

        print('[MAZE]')
        print()
        print(maze)
        print()

        print('Moves:')
        for i in range(len(moves)):
            if moves[list(moves.keys())[i]]:
                print(f"{i}: {list(moves.keys())[i]}")

        print()
        print('chose: ', end='')
        selected = input()
    
        if selected == 'save':
            listToPng(maze.maze, SAVEFILENAME)
            selected = '0'

        selected = int(selected)
    maze.move(list(moves.keys())[selected])

print('congrats')