#!/usr/bin/env python3
import pygame
import sys

res = (w, h) = (1000, 1000)
screen = pygame.display.set_mode(res)
grid = []
active_sim = False

def count_alive(grid, x, y):
    count = 0
    surrounding = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                   (x - 1, y),                 (x + 1, y),
                   (x - 1, y - 1) , (x, y - 1), (x + 1, y - 1)]

    for pos in surrounding:
        if grid[pos[0]][pos[1]]:
            count += 1

    return count

def start_sim(grid):
    """ Begin the simulation """

    new_grid = grid

    for row in range(len(grid)):
        for col in range(len(grid)):
            if not (col == 0 or row == 0 or col == len(grid) - 1 or row == len(grid) - 1):
                # See if a living cell will survive or die
                if grid[row][col]:
                    if count_alive(grid, row, col) < 2 or count_alive(grid, row, col) > 3:
                        new_grid[row][col] = 0

                # See if a dead cell will live
                else:
                    if count_alive(grid, row, col) == 3:
                        new_grid[row][col] = 1

    return new_grid

def draw_cells(grid):
    """ Draw the cells depending on what state they are in. White for living and black for dead """

    square_w = w / len(grid)
    h_space = 0
    for row in range(len(grid)):
        w_space = 0
        for col in range(len(grid)):
            if grid[row][col]:
                pygame.draw.rect(screen, "#ffffff", (0 + w_space, 0 + h_space, square_w, square_w))
            else:
                pygame.draw.rect(screen, "#000000", (0 + w_space, 0 + h_space, square_w, square_w))
            w_space += square_w
        h_space += square_w

def gen_grid(size):
    """ Generating the grid for the board """

    grid = []
    for row in range(size):
        grid.append([])
        for col in range(size):
            grid[row].append(0)

    return grid

def clicked(grid):
    """ Choosing the setup """

    square_w = w / len(grid)
    x = int(pygame.mouse.get_pos()[0] // square_w)
    y = int(pygame.mouse.get_pos()[1] // square_w)

    if grid[y][x]:
        grid[y][x] = 0
    else:
        grid[y][x] = 1

    return grid

def main():
    """ Main function """

    global active_sim

    pygame.init()

    grid = gen_grid(50)

    while True:

        draw_cells(grid)

        # Event loop
        for event in pygame.event.get():
            # Turn off the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # Mouse inputs
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not active_sim:
                    grid = clicked(grid)

            # Keyboard inputs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    active_sim = not active_sim


        if active_sim:
            grid = start_sim(grid)
            pygame.time.delay(1000)

        pygame.display.update()


if __name__ == '__main__':
    main()
