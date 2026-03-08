import random

class MazeGenerator:
    def __init__(self, largeur, hauteur, seed):
        self.width = largeur
        self.height = hauteur
        self.seed = seed
        
        # Initialisation : 15 signifie que les 4 murs sont fermés (1+2+4+8)
        self.grid = [[15 for _ in range(largeur)] for _ in range(hauteur)]
        self.visite = [[False for _ in range(largeur)] for _ in range(hauteur)]

    def _ajouter_motif_42(self):
        """Dessine un motif '42' compact et lisible au centre."""
        if self.width < 11 or self.height < 7:
            print("Grille trop petite pour le motif '42'")
            return

        mid_x, mid_y = self.width // 2, self.height // 2

        # Chiffre 4 (3 de large x 5 de haut) avec barre horizontale de 3 carreaux.
        coords_4 = [
            (mid_x - 3, mid_y - 2),
            (mid_x - 3, mid_y - 1),
            (mid_x - 3, mid_y), (mid_x - 2, mid_y), (mid_x - 1, mid_y),
            (mid_x - 1, mid_y + 1),
            (mid_x - 1, mid_y + 2),
        ]

        # Chiffre 2 (3 de large x 5 de haut) avec base de 3 carreaux.
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

    def generate(self, start_x=0, start_y=0):
        """ Génère un labyrinthe parfait en respectant les murs Nord=1, Est=2, Sud=4, Ouest=8 """
        self._ajouter_motif_42()
        
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
        """ Affiche le labyrinthe avec + - | pour vérification visuelle """
        for y in range(self.height):
            # Ligne des murs Nord
            ligne_n = ""
            for x in range(self.width):
                ligne_n += "+---" if (self.grid[y][x] & 1) else "+   "
            print(ligne_n + "+")
            
            # Ligne des couloirs et murs Ouest/Est
            ligne_c = ""
            for x in range(self.width):
                # On utilise & 8 pour vérifier si le mur Ouest est présent
                ligne_c += "|   " if (self.grid[y][x] & 8) else "    "
            print(ligne_c + "|")
        # Ligne des murs Sud pour la dernière ligne
        print("+---" * self.width + "+")

if __name__ == "__main__":
    mon_laby = MazeGenerator(15, 11, 42)
    mon_laby.generate()
    mon_laby.afficher_ascii()
