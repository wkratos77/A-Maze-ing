import random


class MazeGenerator:
    def __init__(self, largeur, hauteur, seed: int, entry=(0, 0),
                 exit=None, perfect: bool = True):
        self.width = largeur
        self.height = hauteur
        if exit is None:
            exit = (largeur - 1, hauteur - 1)

        self.entry = self.validate_point(entry, "entry")
        self.exit = self.validate_point(exit, "exit")

        self.seed = seed
        random.seed(seed)
        # WALID: this stores all (x, y) cells of the 42
        self.pattern_42 = set()

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
            raise ValueError("Grid too small to show'42'")
            return

        mid_x, mid_y = self.width // 2, self.height // 2
        coords_4 = [
            (mid_x - 3, mid_y - 2),
            (mid_x - 3, mid_y - 1),
            (mid_x - 3, mid_y), (mid_x - 2, mid_y),
            (mid_x - 1, mid_y),
            (mid_x - 1, mid_y + 1),
            (mid_x - 1, mid_y + 2),
        ]
        coords_2 = [
            (mid_x + 1, mid_y - 2), (mid_x + 2, mid_y - 2),
            (mid_x + 3, mid_y - 2),
            (mid_x + 3, mid_y - 1),
            (mid_x + 1, mid_y), (mid_x + 2, mid_y),
            (mid_x + 3, mid_y),
            (mid_x + 1, mid_y + 1),
            (mid_x + 1, mid_y + 2), (mid_x + 2, mid_y + 2),
            (mid_x + 3, mid_y + 2),
        ]

        for x, y in coords_4:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.visite[y][x] = True
                self.grid[y][x] = 15
                # WALID: this remembers that cell is part of the 42
                self.pattern_42.add((x, y))

        for x, y in coords_2:
            # On vérifie les limites pour ne pas sortir de la grille
            if 0 <= x < self.width and 0 <= y < self.height:
                # 1. On marque comme visité pour que l'algorithme contourne
                self.visite[y][x] = True
                # 2. On garde la valeur 15 pour que ce soit un bloc murs pleins
                self.grid[y][x] = 15
                # WALID: this remembers that this cell is part of the 42
                self.pattern_42.add((x, y))

    def generate_perfect_maze(self, start_x=None, start_y=None):
        """ Génère  en respectant les murs Nord=1, Est=2, Sud=4, Ouest=8 """
        self.showing_42()
        if self.entry in self.pattern_42:
            raise ValueError(
                f"Entry point {self.entry} is part of the '42' pattern, "
                "please choose another entry point."
            )
        if self.exit in self.pattern_42:
            raise ValueError(
                f"Exit point {self.exit} is part of the '42' pattern, "
                "please choose another exit point."
            )
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
            (0, -1, 1, 4),  # Nord
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

                # Casser les murs entre la cellule actuelle, la cellule voisine
                self.grid[cy][cx] -= m_actuel
                self.grid[ny][nx] -= m_voisin

                self.visite[ny][nx] = True
                pile.append((nx, ny))
            else:
                pile.pop()  # On revient en arrière (Backtracking)

    def generate_imperfect_maze(self, start_x=None, start_y=None):
        """Generate a maze with loops (more than one path between points)."""
        # building a maze, then removing some walls
        self.generate_perfect_maze(start_x=start_x, start_y=start_y)

        # Keep only East and South checks to not removing two times the wall
        directions = [
            (1, 0, 2, 8),  # Est
            (0, 1, 4, 1),  # Sud
        ]

        breakable_walls = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_42:
                    continue
                for dx, dy, m_actuel, m_voisin in directions:
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue
                    if (nx, ny) in self.pattern_42:
                        continue
                    # Candidate is valid only if a separating wall still exists
                    if ((self.grid[y][x] & m_actuel) and
                            (self.grid[ny][nx] & m_voisin)):
                        breakable_walls.append(
                                    (x, y, nx, ny, m_actuel, m_voisin))

        # opening some walls to get extra paths
        if breakable_walls:
            wall_to_open = max(1, len(breakable_walls) // 10)
        else:
            wall_to_open = 0
        random.shuffle(breakable_walls)
        for x, y, nx, ny, m_actuel, m_voisin in breakable_walls[:wall_to_open]:
            self.grid[y][x] -= m_actuel
            self.grid[ny][nx] -= m_voisin

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
                if (x, y) == self.entry or (x, y) == self.exit:
                    mark = "*"
                else:
                    mark = " "
                # On utilise & 8 pour vérifier si le mur Ouest est présent
                if (self.grid[y][x] & 8):
                    ligne_c += f"| {mark} "
                else:
                    ligne_c += f"  {mark} "
            print(ligne_c + "|")
        # Ligne des murs Sud pour la dernière ligne
        print("+---" * self.width + "+")


if __name__ == "__main__":
    # Exemple d'utilisation
    mg = MazeGenerator(15, 10, 42, (1, 0), (14, 9), perfect=True)
    mg.generate_imperfect_maze()
    mg.afficher_ascii()
