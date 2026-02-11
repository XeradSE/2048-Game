import random
import copy

class Game():

    def __init__(self):
        super().__init__()

        self.score = 0

        # Initialisation d'une grille vide (0 partout)
        self.grid = [[0] * 4 for _ in range(4)]
        # Résultat : [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

        self.add_new_tile()
        self.add_new_tile()
    
    def reverse(self):
        # On inverse chaque ligne de la grille
        self.grid = [row[::-1] for row in self.grid]

    def transpose(self):
        # zip(*self.grid) prend la colonne 0 de chaque ligne et en fait une nouvelle ligne
        # map(list, ...) retransforme les tuples en listes modifiables
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_left(self):
        new_grid = []
        
        for row in self.grid:
            # [2, 0, 2, 0] devient [2, 2]
            temp_row = [num for num in row if num != 0]
            
            # On parcourt la liste compressée. Si deux nombres se suivent, on fusionne.
            # On s'arrête à l'avant-dernier élément (len - 1)
            i = 0
            while i < len(temp_row) - 1:
                if temp_row[i] == temp_row[i+1]:
                    temp_row[i] *= 2      # On double la valeur
                    self.score += temp_row[i]
                    temp_row[i+1] = 0     # On met le voisin à 0 (il sera nettoyé après)
                    i += 1                # On saute le prochain puisqu'on vient de le fusionner
                i += 1
            
            # À ce stade, [2, 2] est devenu [4, 0] s'il y a eu fusion
            # Ou [2, 2, 2, 2] est devenu [4, 0, 4, 0]
            
            # On refait une compression pour virer les 0 créés par la fusion
            final_row = [num for num in temp_row if num != 0]
            
            # On rajoute des 0 à la fin pour revenir à une taille de 4
            while len(final_row) < 4:
                final_row.append(0)
            
            new_grid.append(final_row)
        
        self.grid = new_grid

    def move_right(self):
        self.reverse()       # 1. On inverse
        self.move_left()     # 2. On applique la logique gauche
        self.reverse()       # 3. On remet à l'endroit

    def move_up(self):
        self.transpose()     # 1. Les colonnes deviennent des lignes
        self.move_left()     # 2. On applique la logique gauche
        self.transpose()     # 3. On remet les lignes en colonnes

    def move_down(self):
        self.transpose()     # 1. Transpose
        self.reverse()       # 2. Inverse (donc on est en config "Bas -> Gauche")
        self.move_left()     # 3. Logique
        self.reverse()       # 4. Inverse retour
        self.transpose()     # 5. Transpose retour

    def add_new_tile(self):
        # On crée une liste de tuples (ligne, colonne) pour chaque case qui vaut 0
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]

        # Sécurité : Si la grille est pleine, on arrête tout (Game Over potentiel)
        if not empty_cells:
            return

        # Etape 2 : Choisir une case au hasard
        # random.choice prend un élément aléatoire dans une liste.
        (r, c) = random.choice(empty_cells)

        # Règle : 90% de chance d'avoir un 2, 10% d'avoir un 4
        if random.random() < 0.9:
            self.grid[r][c] = 2
        else:
            self.grid[r][c] = 4

    def is_game_over(self):
        # 1. Reste-t-il des cases vides ?
        for row in self.grid:
            if 0 in row:
                return False

        # 2. Fusions horizontales possibles ?
        # On s'arrête à la colonne 2 (index 3 exclut) pour comparer avec col+1
        for r in range(4):
            for c in range(3):
                if self.grid[r][c] == self.grid[r][c+1]:
                    return False

        # 3. Fusions verticales possibles ?
        # On s'arrête à la ligne 2 pour comparer avec ligne+1
        for r in range(3):
            for c in range(4):
                if self.grid[r][c] == self.grid[r+1][c]:
                    return False

        return True
