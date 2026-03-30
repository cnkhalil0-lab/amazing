
from typing import Tuple, List
import random


class MazeGenerator:
    """
    Classe responsable de la génération du labyrinthe pour le projet A-Maze-ing.
    """
    # Le constructeur __init__ reçoit les données du partenaire

    def __init__(self, width: int, height: int, entry: Tuple[int, int], exit_pos: Tuple[int, int], perfect: bool):
        # 1. On stocke les informations de configuration
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_pos = exit_pos
        self.perfect = perfect

        # 2. On prépare notre terrain en mémoire
        self.grid: List[List[int]] = []
        self.visited = []

        # On construit le tableau 2D ligne par ligne avec des boucles simples
        for y in range(self.height):
            ligne_grid: List[int] = []
            ligne_visited = []
            for x in range(self.width):
                # 15 en décimal = 1111 en binaire. Les 4 murs (Nord, Est, Sud, Ouest) sont fermés.
                ligne_grid.append(15)
                ligne_visited.append(False)
            # On ajoute la ligne terminée à notre grille principale
            self.grid.append(ligne_grid)
            self.visited.append(ligne_visited)
        self.logo_42()
        self.generate_maze()
        self.open_door(self.entry)
        self.open_door(self.exit_pos)
        self.make_imperfect()

    def logo_42(self):
        if self.width < 9 or self.height < 7:
            print("Erreur : labyrinthe trop petit pour le 42.")
            return # On quitte la fonction, on ne dessine rien

        # 2. Le Calque du 42
        motif_42 = [
            "1010111",
            "1010001",
            "1110111",
            "0010100",
            "0010111"
        ]

        # 3. Calcul du point de départ pour centrer
        start_x = (self.width - 7) // 2
        start_y = (self.height - 5) // 2

        # 4. Le Tamponnage sur le tableau "visited"
        for y in range(5):
            for x in range(7):
                if motif_42[y][x] == "1":
                    # On verrouille la case en la mettant à True
                    self.visited[start_y + y][start_x + x] = True

    def generate_maze(self):
        # ÉTAPE 1 : Initialisation
        # On utilise l'entrée que ton partenaire t'a donnée (ex: x=0, y=0)
        start_x, start_y = self.entry
        self.visited[start_y][start_x] = True
        
        # Notre "fil rouge" : on ajoute la case de départ dans l'historique
        stack = [(start_x, start_y)]

        # Petite astuce de pro pour les directions : (décalage_x, décalage_y, mur_actuel, mur_voisin)
        # Nord=1, Sud=4, Est=2, Ouest=8
        directions = [
            (0, -1, 1, 4),  # Aller au Nord (y-1) : je casse mon mur Nord(1), le voisin casse son mur Sud(4)
            (0, 1, 4, 1),   # Aller au Sud (y+1) : je casse mon mur Sud(4), le voisin casse son mur Nord(1)
            (1, 0, 2, 8),   # Aller à l'Est (x+1) : je casse mon mur Est(2), le voisin casse son mur Ouest(8)
            (-1, 0, 8, 2)   # Aller à l'Ouest (x-1) : je casse mon mur Ouest(8), le voisin casse son mur Est(2)
        ]

        # ÉTAPE 2 : La Boucle Principale
        while len(stack) > 0:
            # On regarde où on est (la dernière case de la liste)
            current_x, current_y = stack[-1]

            # On cherche les voisins valides
            voisins_valides = []

            for dx, dy, mur_ici, mur_voisin in directions:
                nx = current_x + dx
                ny = current_y + dy

                # Vérification 1 : Est-ce que le voisin est dans la carte ?
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # Vérification 2 : Est-ce qu'il n'est PAS visité (et pas le 42) ?
                    if self.visited[ny][nx] == False:
                        # On garde ce voisin en mémoire avec les murs à casser
                        voisins_valides.append((nx, ny, mur_ici, mur_voisin))

            # ÉTAPE 3 : Avancer (s'il y a des voisins)
            if len(voisins_valides) > 0:
                # On choisit un voisin au hasard
                choix = random.choice(voisins_valides)
                nx, ny, mur_ici, mur_voisin = choix

                # ON CRESUE ! On fait les soustractions pour abattre les murs
                self.grid[current_y][current_x] -= mur_ici
                self.grid[ny][nx] -= mur_voisin

                # On marque la nouvelle case comme visitée
                self.visited[ny][nx] = True

                # On avance notre fil rouge
                stack.append((nx, ny))

            # ÉTAPE 4 : Le Cul-de-sac (Backtrack)
            else:
                # Aucun voisin valide ? On recule en supprimant notre case actuelle
                stack.pop()


    def open_door(self, pos: Tuple[int, int]):
        x, y = pos

        # On vérifie sur quel bord on se trouve.
        # Les elif (sinon si) garantissent qu'on ne casse qu'un seul mur, 
        # même si on est dans un coin.

        if x == 0:
            # On est sur le bord Gauche : on casse le mur Ouest (8)
            self.grid[y][x] -= 8

        elif x == self.width - 1:
            # On est sur le bord Droit : on casse le mur Est (2)
            self.grid[y][x] -= 2

        elif y == 0:
            # On est sur le bord Haut : on casse le mur Nord (1)
            self.grid[y][x] -= 1

        elif y == self.height - 1:
            # On est sur le bord Bas : on casse le mur Sud (4)
            self.grid[y][x] -= 4

        # S'il n'est sur aucun bord (il est au milieu),
        # on ne fait rien ! Il est déjà connecté.
    
    def make_imperfect(self):
        # 1. Si on a demandé un labyrinthe parfait, on s'arrête tout de suite !
        if self.perfect == True:
            return

        # 2. On calcule combien de murs on va casser au hasard.
        # Par exemple : on prend la surface totale et on divise par 20 (environ 5% des murs)
        nb_murs_a_casser = (self.width * self.height) // 20

        for _ in range(nb_murs_a_casser):
            # On choisit une case complètement au hasard.
            # (On utilise 1 et width-2 pour éviter de toucher aux murs du périmètre extérieur)
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)

            # On choisit de casser soit le mur Est, soit le mur Sud (ça suffit pour faire des boucles)
            # Est : x+1, je casse 2, voisin casse 8
            # Sud : y+1, je casse 4, voisin casse 1
            directions = [(1, 0, 2, 8), (0, 1, 4, 1)]
            dx, dy, mur_ici, mur_voisin = random.choice(directions)

            nx = x + dx
            ny = y + dy

            # 3. LA SÉCURITÉ : Est-ce que le mur est toujours là ?
            # On utilise le "&" (ET binaire). Si le résultat n'est pas 0, le mur existe.
            if (self.grid[y][x] & mur_ici) != 0:
                # Le mur est bien là, on le détruit !
                self.grid[y][x] -= mur_ici
                self.grid[ny][nx] -= mur_voisin
    def solve(self) -> str:
        # ==========================================
        # PHASE 1 & 2 : L'INONDATION ET LES POST-IT
        # ==========================================
        
        # 1. La file d'attente de l'eau (on commence sur l'entrée)
        queue = [self.entry]
        
        # 2. Le dictionnaire de Post-it (Clé: Enfant -> Valeur: Parent)
        # L'entrée n'a pas de parent, donc on met None.
        parent_dict = {self.entry: None}
        
        # 3. Un tableau pour se souvenir d'où l'eau est déjà passée
        visited_bfs = []
        for y in range(self.height):
            ligne_visited = []
            for x in range(self.width):
                ligne_visited.append(False)
            visited_bfs.append(ligne_visited)
            
        # On inonde la case de départ
        start_x, start_y = self.entry
        visited_bfs[start_y][start_x] = True

        # Les 4 directions (dx, dy, mur_qui_bloque)
        directions = [
            (0, -1, 1),  # Nord
            (0, 1, 4),   # Sud
            (1, 0, 2),   # Est
            (-1, 0, 8)   # Ouest
        ]

        trouve = False

        # La boucle d'inondation (tant qu'il y a de l'eau qui avance)
        while len(queue) > 0:
            # On prend la première goutte d'eau de la file (pop(0) lit le début de la liste)
            current_x, current_y = queue.pop(0) 

            # Est-ce qu'on a touché la sortie ?
            if (current_x, current_y) == self.exit_pos:
                trouve = True
                break # On coupe le robinet !

            # Sinon, l'eau essaie d'aller dans les 4 directions
            for dx, dy, mur in directions:
                nx = current_x + dx
                ny = current_y + dy

                # Vérif 1 : On reste dans la carte ?
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    
                    # Vérif 2 : Est-ce que le mur a bien été CASSÉ ?
                    # Attention : ici on veut que le résultat soit 0 (mur absent) pour passer !
                    if (self.grid[current_y][current_x] & mur) == 0:
                        
                        # Vérif 3 : Est-ce une nouvelle case non inondée ?
                        if visited_bfs[ny][nx] == False:
                            
                            # On inonde la nouvelle case
                            visited_bfs[ny][nx] = True
                            queue.append((nx, ny))
                            
                            # ON COLLE LE POST-IT ! (On note d'où on vient)
                            parent_dict[(nx, ny)] = (current_x, current_y)

        if not trouve:
            return "" # Sécurité si le labyrinthe est impossible

        chemin_inverse = ""
        actuelle = self.exit_pos

        # On recule de Post-it en Post-it jusqu'à l'Entrée
        while actuelle != self.entry:
            # On lit le dictionnaire pour trouver le parent
            parent = parent_dict[actuelle]
            
            px, py = parent
            ax, ay = actuelle
            
            # On déduit la lettre en comparant les coordonnées
            if ay < py: 
                chemin_inverse += "N" # On est monté
            elif ay > py: 
                chemin_inverse += "S" # On est descendu
            elif ax > px: 
                chemin_inverse += "E" # On est allé à droite
            elif ax < px: 
                chemin_inverse += "W" # On est allé à gauche
            
            # On recule physiquement sur la case parente
            actuelle = parent

        # Le mot a été écrit à l'envers (de la Sortie vers l'Entrée).
        chemin_final = ""
        for lettre in chemin_inverse:
            chemin_final = lettre + chemin_final

        return chemin_final


if __name__ == "__main__":
    # 1. On définit les règles du jeu
    largeur = 10
    hauteur = 10
    entree = (0, 0)         # Coin en haut à gauche
    sortie = (9, 9)         # Coin en bas à droite
    labyrinthe_parfait = False  # On veut des boucles !

    # 2. On construit le labyrinthe (l'__init__ fait tout le travail)
    mon_labyrinthe = MazeGenerator(largeur, hauteur, entree, sortie, labyrinthe_parfait)

    # 3. On lance notre GPS
    chemin_solution = mon_labyrinthe.solve()

    # 4. On affiche les résultats dans le terminal
    print("=== TEST DU LABYRINTHE ===")
    print(f"Taille : {largeur}x{hauteur}")
    print(f"La solution trouvée est : {chemin_solution}")
    print(f"Nombre de pas pour sortir : {len(chemin_solution)}")

