import random
import curses
from collections import deque


def new_world(h, w):
    # create a list representing the current generation
    # as a h*w matrix and initialize it with random
    # values in [0, 1] which stand for the active cells
    # generation = [random.choices(range(0, 2), k=w) for _ in range(h)]

    # fill with 0s
    generation = [[0 for i in range(w)] for j in range(h)]

    # random initialization
    for i in range(len(generation)):
        for j in range(len(generation[i])):
            generation[i][j] = random.randint(0, 2)

    return generation


'''
count the live neighbors of the cell indexed by row_idx, col_idx
'''


def live_neighbors_count(current_gen, row_idx, col_idx):
    # print("")
    count = 0
    for i in range(row_idx - 1, row_idx + 2):
        for j in range(col_idx - 1, col_idx + 2):
            # print("a[{}][{}]={}".format(i, j, current_gen[i][j]))
            if (current_gen[i][j] == 1 and
                    (i != row_idx or j != col_idx)):
                count += 1
    # print(count)
    return count


'''
implement Convway's Game of Life. Takes a list of cells in input
which represents a generation of cells and computes the next one.
'''


def next_generation(current_gen):
    # cells to be live in the next generation
    live_queue = deque()
    # cells to be dead in the next generation
    dead_queue = deque()

    for i in range(len(current_gen)):
        for j in range(len(current_gen[i])):
            # if a cell has 8 neighbors,
            # that is to say it is not on the
            # boundaries of the game's world,
            # check each of its neighbors
            if (0 < i < len(current_gen) - 1 and
                    0 < j < len(current_gen[i]) - 1):
                # print("a[{}][{}]".format(i, j))
                # count the cell's live neighbors
                live_count = live_neighbors_count(current_gen, i, j)
                # print("a[{}][{}] = {}".format(i, j, live_count))
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
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(150)

    h, w = stdscr.getmaxyx()
    game_field = new_world(h, w)

    # curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    # stdscr.attron(curses.color_pair(1))

    while 1:
        stdscr.clear()
        game_field = next_generation(game_field)

        for i in range(h - 1):
            for j in range(w - 1):
                if game_field[i][j] == 1:
                    stdscr.addstr(i, j, '*')

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

    # stdscr.attroff(curses.color_pair(1))


curses.wrapper(main)
