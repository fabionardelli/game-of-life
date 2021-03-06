# Conway's Game of Life
# Author: Fabio Nardelli

import random
import curses
from collections import deque


def new_world(world_h, world_w):
    """
    Initialize the game world. Create a world_h * world_w matrix
    representing the first generation of cells and initialize it with random
    values in {0, 1} which stand for the dead/live cells.
    """

    generation = [[random.randint(0, 1) for _ in range(world_w)]
                  for _ in range(world_h)]

    return generation


def live_neighbors_count(current_gen, row_idx, col_idx):
    """
    Count the live neighbors of the cell indexed by row_idx, col_idx.
    Handle the matrix as a wrap-around array.
    """

    count = 0

    rows = len(current_gen)
    cols = len(current_gen[0])

    if current_gen[(row_idx - 1) % rows][(col_idx - 1) % cols] == 1:
        count += 1
    if current_gen[(row_idx - 1) % rows][col_idx % cols] == 1:
        count += 1
    if current_gen[(row_idx - 1) % rows][(col_idx + 1) % cols] == 1:
        count += 1

    if current_gen[row_idx % rows][(col_idx - 1) % cols] == 1:
        count += 1
    if current_gen[row_idx % rows][(col_idx + 1) % cols] == 1:
        count += 1

    if current_gen[(row_idx + 1) % rows][(col_idx - 1) % cols] == 1:
        count += 1
    if current_gen[(row_idx + 1) % rows][col_idx % cols] == 1:
        count += 1
    if current_gen[(row_idx + 1) % rows][(col_idx + 1) % cols] == 1:
        count += 1

    return count


def next_generation(current_gen):
    """
    Implement Conway's Game of Life. Take as input a matrix (list of lists)
    which represents a generation of cells and compute the next one.
    """

    # cells to be live in the next generation
    live_list = []
    # cells to be dead in the next generation
    dead_list = []

    for i, row in enumerate(current_gen):
        for j, item in enumerate(row):
            live_count = live_neighbors_count(current_gen, i, j)
            # print("a[{}][{}] = {}".format(i, j, live_count))
            # a live cell with 2 or 3 live neighbors survives.
            # a dead cell with less or more than 3 live neighbors remains dead.
            # Otherwise,
            # a live cell with less than 2 or more than 3 live neighbors dies
            if current_gen[i][j] == 1 and (live_count < 2 or live_count > 3):
                dead_list.append([i, j])
            # a dead cell with exactly 3 live neighbors becomes a live cell
            elif current_gen[i][j] == 0 and live_count == 3:
                live_list.append([i, j])

    # set the live cells in the next generation
    for cell in live_list:
        current_gen[cell[0]][cell[1]] = 1

    # set the dead cells in the next generation
    for cell in dead_list:
        current_gen[cell[0]][cell[1]] = 0

    return current_gen


def main(stdscr):
    """
    Main function containing the game loop
    """

    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(500)

    h, w = stdscr.getmaxyx()
    game_field = new_world(h - 2, w)

    generation = 1  # generation number

    while True:
        stdscr.clear()
        live_count = 0

        # print the game world.
        for i, row in enumerate(game_field):
            for j, cell in enumerate(row):
                if game_field[i][j] == 1:
                    live_count += 1
                    try:
                        stdscr.addch(i, j, '*')
                    except curses.error:
                        pass

        # print game info and commands
        try:
            keys_info = 'pause: p  exit: q'
            stdscr.addstr(h - 1, w - 18, keys_info)

            generation_info = 'generation:   {}'.format(generation)
            stdscr.addstr(h - 1, 0, generation_info)

            live_info = 'living cells: {}'.format(live_count)
            stdscr.addstr(h - 2, 0, live_info)
        except curses.error:
            pass

        stdscr.refresh()
        game_field = next_generation(game_field)

        # exit if the user presses ENTER/ESC/q
        key = stdscr.getch()
        if (key == ord('q') or key == ord('Q') or key == 27
                or key == curses.KEY_ENTER or key in [10, 13]):
            break
        # pause if the user presses p
        elif key == ord('p') or key == ord('P'):
            keys_info = 'press any key to resume'
            stdscr.addstr(h - 1, w - 24, keys_info)
            stdscr.nodelay(0)
            stdscr.getch()
            stdscr.nodelay(1)
            stdscr.timeout(150)
        # if window is resized, re-initialize the game field
        # with the new dimensions
        elif key == curses.KEY_RESIZE:
            h, w = stdscr.getmaxyx()
            game_field = new_world(h - 2, w)
            generation = 0

        generation += 1


curses.wrapper(main)
