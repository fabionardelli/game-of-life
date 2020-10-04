import random
import curses
from collections import deque


def new_world(screen_h, screen_w):
    """
    Initialize the game world creating a matrix of cells.
    Create a list representing the current generation
    as a (screen_h+2)*(screen_w+2) matrix and initialize it with random
    values in {0, 1} which stand for the dead/live cells.
    The external rows/cols gets initialized to 0 (like a frame).
    Only the screen_h*screen_w submatrix will be printed.
    """

    generation = [[0 if i == 0 or i == screen_w + 1 or j == 0 or j == screen_h + 1
                   else random.randint(0, 1) for i in range(screen_w + 2)]
                  for j in range(screen_h + 2)]


    return generation


def live_neighbors_count(current_gen, row_idx, col_idx):
    """
    Count the live neighbors of the cell indexed by row_idx, col_idx
    """

    count = 0
    for i in range(row_idx - 1, row_idx + 2):
        for j in range(col_idx - 1, col_idx + 2):
            if (current_gen[i][j] == 1 and
                    (i != row_idx or j != col_idx)):
                count += 1
    return count


def next_generation(current_gen):
    """
    Implement Conway's Game of Life. Take a list of cells in input
    which represents a generation of cells and compute the next one.
    """

    # cells to be live in the next generation
    live_queue = deque()
    # cells to be dead in the next generation
    dead_queue = deque()

    for i in range(1, len(current_gen) - 1):
        for j in range(1, len(current_gen[i]) - 1):
            # count the cell's live neighbors
            live_count = live_neighbors_count(current_gen, i, j)

            # a live cell with 2 or 3 live neighbors survives.
            # a dead cell with less or more than 3 live neighbors remains dead.
            # Otherwise,
            # a live cell with less than 2 or more than 3 live neighbors dies
            if current_gen[i][j] == 1 and (live_count < 2 or live_count > 3):
                dead_queue.append([i, j])
            # a dead cell with exactly 3 live neighbors becomes a live cell
            elif current_gen[i][j] == 0 and live_count == 3:
                live_queue.append([i, j])

    # set the live cells in the next generation
    while len(live_queue) > 0:
        next_live = live_queue.popleft()
        current_gen[next_live[0]][next_live[1]] = 1

    # set the dead cells in the next generation
    while len(dead_queue) > 0:
        next_dead = dead_queue.popleft()
        current_gen[next_dead[0]][next_dead[1]] = 0

    return current_gen


def main(stdscr):
    """
    Main function containing the game loop
    """

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(150)

    h, w = stdscr.getmaxyx()
    game_field = new_world(h, w)

    while True:
        stdscr.clear()
        game_field = next_generation(game_field)

        # print the game world.
        for i in range(1, len(game_field)):
            for j in range(1, len(game_field[i])):
                if game_field[i][j] == 1:
                    try:
                        stdscr.addstr(i - 1, j - 1, '*')
                    except curses.error:
                        pass

        stdscr.refresh()

        # exit if the user presses ENTER
        key = stdscr.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            break
        # if window is resized, re-initialize the game field
        # with the new dimensions
        elif key == curses.KEY_RESIZE:
            h, w = stdscr.getmaxyx()
            game_field = new_world(h, w)


curses.wrapper(main)
