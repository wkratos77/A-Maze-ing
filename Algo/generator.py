import random

class MazeGenerator:
    def __init__(self, largeur, hauteur, seed:int, entry=(0, 0),
                 exit=None, perfect: bool = True):
        self.width = largeur
        self.height = hauteur
        if exit is None:
            exit = (largeur - 1, hauteur - 1)

        self.entry = self.validate_point(entry, "entry")
        self.exit = self.validate_point(exit, "exit")

        self.seed = seed
        random.seed(seed)

        # Initialisation : 15 signifie que les 4 murs sont fermés (1+2+4+8)
        self.grid = [[15 for _ in range(largeur)] for _ in range(hauteur)]
        self.visite = [[False for _ in range(largeur)] for _ in range(hauteur)]

    def validate_point(self, point, name):
        """Validate the coordonates taken"""
        if not isinstance(point, tuple) or len(point) != 2:
            raise ValueError(f"{name} must be a tuple (x, y)")

        x, y = point
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError(f"{name} must be an intiger")
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(
                f"hors limites : try to change x={x}, y={y}"
            )
        return point

    def showing_42(self):
        """showing '42' at the center"""
        if self.width < 11 or self.height < 7:
            print("Grid to small to show'42'")
            return

        mid_x, mid_y = self.width // 2, self.height // 2
        coords_4 = [
            (mid_x - 3, mid_y - 2),
            (mid_x - 3, mid_y - 1),
            (mid_x - 3, mid_y), (mid_x - 2, mid_y), (mid_x - 1, mid_y),
            (mid_x - 1, mid_y + 1),
            (mid_x - 1, mid_y + 2),
        ]
        coords_2 = [
            (mid_x + 1, mid_y - 2), (mid_x + 2, mid_y - 2), (mid_x + 3, mid_y - 2),
            (mid_x + 3, mid_y - 1),
            (mid_x + 1, mid_y), (mid_x + 2, mid_y), (mid_x + 3, mid_y),
            (mid_x + 1, mid_y + 1),
            (mid_x + 1, mid_y + 2), (mid_x + 2, mid_y + 2), (mid_x + 3, mid_y + 2),
        ]

        for x, y in coords_4:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visite[y][x] = True
                self.grid[y][x] = 15

        for x, y in coords_2:
            # On vérifie les limites pour ne pas sortir de la grille
            if 0 <= x < self.width and 0 <= y < self.height:
                # 1. On marque comme visité pour que l'algorithme contourne
                self.visite[y][x] = True
                # 2. On garde la valeur 15 pour que ce soit un bloc de murs pleins
                self.grid[y][x] = 15

    def generate(self, start_x=None, start_y=None):
        """ Génère  en respectant les murs Nord=1, Est=2, Sud=4, Ouest=8 """
        self.showing_42()

        if start_x is None or start_y is None:
            start_x, start_y = self.entry

        if not (0 <= start_x < self.width and 0 <= start_y < self.height):
            raise ValueError(
                f"Point de depart ({start_x}, {start_y}) hors limits for"
                f"grid {self.width}x{self.height}"
            )
        
        pile = [(start_x, start_y)]
        self.visite[start_y][start_x] = True

        # Directions : (dx, dy, valeur_mur_actuel, valeur_mur_voisin)
        directions = [
            (0, -1, 1, 4), # Nord
            (1, 0, 2, 8),  # Est
            (0, 1, 4, 1),  # Sud
            (-1, 0, 8, 2)  # Ouest
        ]
        # cx = current x, cy = current y, nx = next x, ny = next y
        while pile:
            cx, cy = pile[-1]
            voisins_possibles = []

            for dx, dy, m_actuel, m_voisin in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not self.visite[ny][nx]:
                        voisins_possibles.append((nx, ny, m_actuel, m_voisin))

            if voisins_possibles:
                # Choisir un chemin au hasard
                nx, ny, m_actuel, m_voisin = random.choice(voisins_possibles)
                
                # Casser les murs entre la cellule actuelle et la cellule voisine
                self.grid[cy][cx] -= m_actuel
                self.grid[ny][nx] -= m_voisin
                
                self.visite[ny][nx] = True
                pile.append((nx, ny))
            else:
                pile.pop() # On revient en arrière (Backtracking)

    def afficher_ascii(self):
        for y in range(self.height):
            # Ligne des murs Nord
            ligne_n = ""
            for x in range(self.width):
                ligne_n += "+---" if (self.grid[y][x] & 1) else "+   "
            print(ligne_n + "+")
            
            # Ligne des couloirs et murs Ouest/Est
            ligne_c = ""
            for x in range(self.width):
                mark = "*" if (x, y) == self.entry or (x, y) == self.exit else " "
                # On utilise & 8 pour vérifier si le mur Ouest est présent
                ligne_c += f"| {mark} " if (self.grid[y][x] & 8) else f"  {mark} "
            print(ligne_c + "|")
        # Ligne des murs Sud pour la dernière ligne
        print("+---" * self.width + "+")

if __name__ == "__main__":
    mon_laby = MazeGenerator(15, 11, 40,entry=(2, 0), exit=(7, 3))
    mon_laby.generate()
    mon_laby.afficher_ascii()
