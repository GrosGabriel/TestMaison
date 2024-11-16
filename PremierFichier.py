import random as rd

from 2048 import move_row_ left


def rd_value(n):
    return n * rd.randint(0, 1)


    
def get_empty_tiles_positions(grid):
    res = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] in ['', ' ', '0', 0]:
                res.append((i, j))

    return res
