
import random as rd
import tkinter as tk
from tkinter import ttk

'''
def grid_to_string(grid):
    n = len(grid)
    for i in range(n):
        for k in range(long_value(grid)+4):
            print("=", end="")
        print(" ", end="")
    print()
    grid2 = ajustement(grid)
    for j in range(n):
        for i in range(n):
            print("|", grid2[j][i], "|", end=" ")
        print()
        for i in range(n):
            for k in range(long_value(grid)+4):
                print("=", end="")
            print(" ", end="")
        print()
'''

THEMES = {"0": {"name": "Default", 0: "", 2: "2", 4: "4", 8: "8", 16: "16", 32: "32", 64: "64", 128: "128", 256: "256", 512: "512", 1024: "1024", 2048: "2048", 4096: "4096", 8192: "8192"}, "1": {"name": "Chemistry", 0: "", 2: "H", 4: "He", 8: "Li", 16: "Be",
                                                                                                                                                                                                   32: "B", 64: "C", 128: "N", 256: "O", 512: "F", 1024: "Ne", 2048: "Na", 4096: "Mg", 8192: "Al"}, "2": {"name": "Alphabet", 0: "", 2: "A", 4: "B", 8: "C", 16: "D", 32: "E", 64: "F", 128: "G", 256: "H", 512: "I", 1024: "J", 2048: "K", 4096: "L", 8192: "M"}}
THEME = str(0)


def create_grid(n):
    game_grid = []
    for i in range(0, n):
        game_grid.append(['' for _ in range(n)])
    return game_grid


def get_value_new_tile():
    return THEMES[THEME][2 * rd.randint(1, 2)]


def grid_add_new_tile_at_position(grid, x, y):
    var = get_value_new_tile()
    grid[x][y] = var


def get_empty_tiles_positions(grid):
    res = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] in ['', ' ', '0', 0]:
                res.append((i, j))

    return res


def grid_get_value(grid, x, y):
    var = grid[x][y]
    if var == '' or var == ' ':
        var = THEMES[THEME][var]
    return var


def get_new_position(grid):
    res = get_empty_tiles_positions(grid)
    if res != []:
        return rd.choice(res)
    else:
        return None


def get_all_tiles(grid):
    res = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            var = grid[i][j]
            if var == '' or var == ' ':
                var = THEMES[THEME][0]
            res.append(var)
    return res


def grid_add_new_tile(grid):
    coord = get_new_position(grid)
    if coord != None:
        grid_add_new_tile_at_position(grid, coord[0], coord[1])


def inverse_cle_valeur(D):
    res = {}
    for cle, valeur in D.items():
        res[valeur] = cle
    res['0'] = res['']
    return res


def move_row_left(ligne):

    # Étape 1 : Filtrer les zéros pour obtenir seulement les éléments non nuls
    non_zero = [num for num in ligne if num not in [
        0, '0', '', ' ', THEMES[THEME][0]]]
    # Étape 2 : Combiner les éléments adjacents identiques
    combined = []
    # Ajout d'un flag skip pour ne pas traiter un élément deux fois.
    skip = False
    for i in range(len(non_zero)):
        if skip:
            skip = False
            continue
        if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
            # Galère avec les types int/str des différents dico
            combined.append(
                THEMES[THEME][2 * int(inverse_cle_valeur(THEMES[THEME])[str(non_zero[i]).strip()])])
            skip = True  # Sauter le prochain élément
        else:
            combined.append(non_zero[i])

    # Étape 3 : Compléter avec des zéros pour obtenir une liste de longueur 4
    result = combined + ['0'] * (4 - len(combined))
    return result


def transpose(grid):
    n = len(grid)
    grid2 = create_grid(n)
    for i in range(len(grid)):
        for j in range(len(grid)):
            grid2[i][j] = grid[j][i]

    return grid2


def move_grid(grid, move):
    grid2 = create_grid(len(grid))
    if move == 'd':
        for i in range(len(grid)):
            grid2[i] = move_row_right(grid[i])

    elif move == 'g':
        for i in range(len(grid)):
            grid2[i] = move_row_left(grid[i])

    elif move == 'h':
        grid3 = transpose(grid)
        for i in range(len(grid)):
            grid2[i] = move_row_left(grid3[i])
        grid2 = transpose(grid2)

    elif move == 'b':
        grid3 = transpose(grid)
        for i in range(len(grid)):
            grid2[i] = move_row_right(grid3[i])
        grid2 = transpose(grid2)

    return grid2


def move_row_right(ligne):
    return move_row_left(ligne[::-1])[::-1]


def is_grid_full(grid):
    return get_empty_tiles_positions == []


def move_left(grid):
    """Vérifie si un mouvement vers la gauche est possible"""
    for i in range(len(grid)):
        for j in range(1, len(grid)):
            # Si une case est vide avant une case non vide, ou si deux cases adjacentes sont identiques
            if grid[i][j - 1] in ['', ' ', '0', 0] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible
            if grid[i][j] == grid[i][j - 1] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible par fusion
    return False  # Aucun mouvement possible


def move_right(grid):
    """Vérifie si un mouvement vers la droite est possible"""
    for i in range(len(grid)):
        for j in range(len(grid) - 2, -1, -1):
            if grid[i][j + 1] in ['', ' ', '0', 0] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible
            if grid[i][j] == grid[i][j + 1] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible par fusion
    return False  # Aucun mouvement possible


def move_up(grid):
    """Vérifie si un mouvement vers le haut est possible"""
    for i in range(1, len(grid)):
        for j in range(len(grid)):
            if grid[i - 1][j] in ['', ' ', '0', 0] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible
            if grid[i][j] == grid[i - 1][j] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible par fusion
    return False  # Aucun mouvement possible


def move_down(grid):
    """Vérifie si un mouvement vers le bas est possible"""
    for i in range(len(grid) - 2, -1, -1):
        for j in range(len(grid)):
            if grid[i + 1][j] in ['', ' ', '0', 0] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible
            if grid[i][j] == grid[i + 1][j] and grid[i][j] not in ['', ' ', '0', 0]:
                return True  # Mouvement possible par fusion
    return False  # Aucun mouvement possible


def move_possible(grid):
    """Retourne une liste de booléens pour savoir si un mouvement est possible dans les directions [gauche, droite, haut, bas]"""
    return [move_left(grid), move_right(grid), move_up(grid), move_down(grid)]


def is_game_over(grid):
    return move_possible == [False, False, False, False]


def get_grid_title_max(grid):
    maxi = 0
    for ligne in grid:
        L = [int(inverse_cle_valeur(THEMES[THEME])[str(num).strip()])
             for num in ligne]
        maxi = max(maxi, max(L))
    return maxi


def rd_play(n):

    # initialisation
    grid = create_grid(n)
    grid_add_new_tile(grid)

    # itération
    L = ["g", "d", "h", "b"]

    while not is_game_over(grid):

        if get_grid_title_max(grid) >= 2048:
            print("Wow vous êtes trop fort.")

        # ajout 2 et 4 random
        grid_add_new_tile(grid)

        # affichage
        grid_to_string(grid)
        print(grid[0])

        possibilities = move_possible(grid)
        print(possibilities)
        k_possibles = [i for i in range(
            len(possibilities)) if possibilities[i]]
        print(k_possibles)
        k = rd.choice(k_possibles)
        move = L[k]
        print(move)

        grid = move_grid(grid, move)


# Couleurs associées aux valeurs des cellules
COLORS = {
    '': {"bg": "lightgray", "fg": "black"},
    '0': {"bg": "lightgray", "fg": "black"},
    '2': {"bg": "#eee4da", "fg": "black"},
    '4': {"bg": "#ede0c8", "fg": "black"},
    '8': {"bg": "#f2b179", "fg": "white"},
    '16': {"bg": "#f59563", "fg": "white"},
    '32': {"bg": "#f67c5f", "fg": "white"},
    '64': {"bg": "#f65e3b", "fg": "white"},
    '128': {"bg": "#edcf72", "fg": "white"},
    '256': {"bg": "#edcc61", "fg": "white"},
    '512': {"bg": "#edc850", "fg": "white"},
    '1024': {"bg": "#edc53f", "fg": "white"},
    '2048': {"bg": "#edc22e", "fg": "white"}
}


def key_pressed(event, cells):
    global grid_game
    """Gère les pressions de touches pour déplacer la grille de jeu."""
    move = event.keysym  # Récupérer le nom de la touche (gauche, droite, haut, bas)
    print(f"Key pressed: {move}")  # Afficher la touche pressée dans la console

    # Selon la touche pressée, déplacer la grille
    if move == "Left":
        grid_game = move_grid(grid_game, 'g')  # 'g' pour gauche
    elif move == "Right":
        grid_game = move_grid(grid_game, 'd')  # 'd' pour droite
    elif move == "Up":
        grid_game = move_grid(grid_game, 'h')  # 'h' pour haut
    elif move == "Down":
        grid_game = move_grid(grid_game, 'b')  # 'b' pour bas

    # Mettre à jour l'affichage de la grille
    grid_add_new_tile(grid_game)
    display_and_update_graphical_grid(cells)


def graphical_grid_init(game_window, n):
    """Initialise la grille graphique pour la fenêtre de jeu."""
    cells = []  # Liste pour contenir toutes les cellules (frames) du jeu

    # Création d'une Frame de fond pour la grille de jeu
    background = tk.Frame(game_window, bg="lightgray")
    background.pack(padx=20, pady=20)

    # Taille de la grille

    cell_size = 100  # Taille de chaque cellule (en pixels)

    # Initialiser les cellules avec des labels vides
    for i in range(n):
        row = []
        for j in range(n):
            # Créer chaque cellule avec une Frame et un Label à l'intérieur
            cell = tk.Frame(background, width=cell_size, height=cell_size,
                            bg="#CCC0B3", bd=5, relief="solid")
            cell.grid(row=i, column=j, padx=5, pady=5)

            # Label pour afficher la valeur de la tuile (initialement vide)
            label = tk.Label(cell, text="", font=(
                "Arial", 24), width=5, height=2)
            label.pack(fill=tk.BOTH, expand=True)
            row.append(label)

        cells.append(row)

    return cells


def display_and_update_graphical_grid(cells):
    global grid_game
    """Met à jour les tuiles graphiques en fonction de la grille de jeu."""
    for i in range(4):
        for j in range(4):
            value = grid_game[i][j]
            if value in [0, '0', '', ' ']:
                value = ''
            # Trouver le label correspondant à la cellule (i, j)
            label = cells[i][j]
            # Mettre à jour le texte du label avec la valeur de la tuile
            # label.config(text=value , bg="#CCC0B3" if value == '' else "#F4A300")
            label.config(text=value, bg=COLORS[str(inverse_cle_valeur(THEMES[THEME])[
                         value])]["bg"], fg=COLORS[str(inverse_cle_valeur(THEMES[THEME])[value])]["fg"])


def transfert_theme(theme):
    if theme == "Default":
        return '0'
    elif theme == "Chemistry":
        return '1'
    elif theme == "Alphabet":
        return '2'


class Game2048:
    global grid_game
    global THEME

    def __init__(self, root):

        self.root = root
        self.root.title("2048")

        # Fenêtre de sélection pour choisir la taille de la grille et le thème
        self.setup_window = tk.Toplevel(self.root)
        self.setup_window.title("Menu configuration 2048")

        # Choisir la taille de la grille
        tk.Label(self.setup_window, text="Choose grid size").pack(pady=5)
        self.grid_size_var = tk.StringVar(value="4")
        grid_size_selector = ttk.Combobox(
            self.setup_window, textvariable=self.grid_size_var, values=["3", "4", "5", "6"])
        grid_size_selector.pack(pady=5)

        # Choisir le thème
        tk.Label(self.setup_window, text="Choose a theme").pack(pady=5)
        self.theme_var = tk.StringVar(value="Default")
        theme_selector = ttk.Combobox(self.setup_window, textvariable=self.theme_var, values=[
                                      "Default", "Chemistry", "Alphabet"])
        theme_selector.pack(pady=5)

        # Boutons Quit et Play
        button_frame = tk.Frame(self.setup_window)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Quit", command=self.root.quit).grid(
            row=0, column=0, padx=5)
        tk.Button(button_frame, text="Play", command=self.start_game).grid(
            row=0, column=1, padx=5)

    def start_game(self):
        global THEME
        global grid_game

        # print(THEME)

        # Fermer la fenêtre de configuration et démarrer le jeu

        self.setup_window.destroy()
        # Création de la fenêtre de jeu
        game_window = tk.Toplevel(root)
        game_window.title("2048 Game")

        game_window.focus_set()  # Assurez-vous que la fenêtre de jeu a le focus

        grid_size = int(self.grid_size_var.get())
        theme = self.theme_var.get()
        THEME = transfert_theme(theme)
        # print(THEME)

        # Initialiser la grille graphique
        cells = graphical_grid_init(game_window, grid_size)

        # Lier l'événement de touche à la fonction key_pressed
        game_window.bind("<KeyPress>", lambda event: key_pressed(event, cells))

        grid_game = create_grid(grid_size)
        grid_add_new_tile(grid_game)
        grid_add_new_tile(grid_game)

        # Afficher la grille initiale
        display_and_update_graphical_grid(cells)


grid_game = create_grid(4)

# Création de la fenêtre principale
root = tk.Tk()
root.title("2048")
root.withdraw()  # Masquer la fenêtre principale

game = Game2048(root)  # Création de l'interface menu


# Lancer l'application

root.mainloop()


'''

def test_move_row_left():
    assert move_row_left(['0', '0', '0', '2']) == ['2', '0', '0', '0']
    assert move_row_left(['0', '2', '0', '4']) == ['2', '4', '0', '0']
    assert move_row_left(['2', '2', '0', '4']) == ['4', '4', '0', '0']
    assert move_row_left(['2', '2', '2', '2']) == ['4', '4', '0', '0']
    assert move_row_left(['4', '2', '0', '2']) == ['4', '4', '0', '0']
    assert move_row_left(['2', '0', '0', '2']) == ['4', '0', '0', '0']
    assert move_row_left(['2', '4', '2', '2']) == ['2', '4', '4', '0']
    assert move_row_left(['2', '4', '4', '0']) == ['2', '8', '0', '0']
    assert move_row_left(['4', '8', '16', '32']) == ['4', '8', '16', '32']


def test_move_row_right():
    assert move_row_right(['2', '0', '0', '0']) == ['0', '0', '0', '2']
    assert move_row_right(['0', '2', '0', '4']) == ['0', '0', '2', '4']
    assert move_row_right(['2', '2', '0', '4']) == ['0', '0', '4', '4']
    assert move_row_right(['2', '2', '2', '2']) == ['0', '0', '4', '4']
    assert move_row_right(['4', '2', '0', '2']) == ['0', '0', '4', '4']
    assert move_row_right(['2', '0', '0', '2']) == ['0', '0', '0', '4']
    assert move_row_right(['2', '4', '2', '2']) == ['0', '2', '4', '4']
    assert move_row_right(['2', '4', '4', '0']) == ['0', '0', '2', '8']
    assert move_row_right(['4', '8', '16', '32']) == ['4', '8', '16', '32']

def test_move_grid():
    assert move_grid([['2', '0', '0', '2'], ['4', '4', '0', '0'], ['8', '0', '8', '0'], ['0', '2', '2', '0']], "g") == [
        ['4', '0', '0', '0'], ['8', '0', '0', '0'], ['16', '0', '0', '0'], ['4', '0', '0', '0']]  , "problème à gauche"
    assert move_grid([['2', '0', '0', '2'], ['4', '4', '0', '0'], ['8', '0', '8', '0'], ['0', '2', '2', '0']], "d") == [
        ['0', '0', '0', '4'], ['0', '0', '0', '8'], ['0', '0', '0', '16'], ['0', '0', '0', '4']] , "problème à droite"
    assert move_grid([['2', '0', '0', '2'], ['2', '4', '0', '0'], ['8', '4', '2', '0'], ['8', '2', '2', '0']], "h") == [
        ['4', '8', '4', '2'], ['16', '2', '0', '0'], ['0', '0', '0', '0'], ['0', '0', '0', '0']]    ,"problème en haut"
    assert move_grid([['2', '0', '0', '2'], ['2', '4', '0', '0'], ['8', '4', '2', '0'], ['8', '2', '2', '0']], "b") == [
        ['0', '0', '0', '0'], ['0', '0', '0', '0'], ['4', '8', '0', '0'], ['16', '2', '4', '2']]    ,"problème en bas"



'''
