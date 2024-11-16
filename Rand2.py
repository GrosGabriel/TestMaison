import random as rd
from PremierFichier import rd_value
from a2048 import move_row_left


def xx():
    print("hello world")


L = [rd_value(i) for i in range(5)]
print(move_row_left(L))
