from library.maze import Maze, pngToList

FILENAME = 'Example/maze.png'

maze = Maze(pngToList(FILENAME))

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
        selected = int(input())
        
    maze.move(list(moves.keys())[selected])

print('congrats')