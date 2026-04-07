# Générateur de Labyrinthe (Maze Generator)

Un module Python autonome responsable de la génération, de la gestion et de la résolution de labyrinthes en 2D. Il est conçu pour être facilement importé et réutilisé dans de futurs projets.

##  Structure du Projet

La classe `MazeGenerator` est composée des méthodes suivantes :

* **`__init__`** : Initialise la configuration de la grille et déclenche automatiquement le processus de génération du labyrinthe.
* **`logo_42`** : Imprime un motif "42" au centre de la grille pour influencer la recherche de chemin (pathfinding).
* **`generate_maze`** : Creuse les chemins du labyrinthe en utilisant un algorithme de "backtracking" (retour sur trace) aléatoire.
* **`open_door`** : Casse les murs des limites extérieures pour ouvrir les coordonnées spécifiques d'entrée et de sortie.
* **`make_imperfect`** : Supprime aléatoirement des murs supplémentaires pour créer des boucles et des chemins multiples si un labyrinthe parfait n'est pas requis.
* **`solve`** : Calcule le chemin le plus court de l'entrée à la sortie en utilisant un algorithme de parcours en largeur (BFS) et renvoie la chaîne de directions.

## Comment Instancier et Utiliser

Le cœur du module est la classe `MazeGenerator`. Vous trouverez ci-dessous un exemple de base montrant comment initialiser le générateur et l'utiliser pour créer un labyrinthe.

### Exemple de base

```python
from maze_generator import MazeGenerator

# 1. Définir les dimensions et les coordonnées
largeur, hauteur = 15, 15
point_entree = (0, 0)
point_sortie = (14, 14)

# 2. Instancier le générateur
labyrinthe = MazeGenerator(
    width=largeur, 
    height=hauteur, 
    entry=point_entree, 
    exit_pos=point_sortie, 
    perfect=False
)

# 3. Afficher la grille 2D générée
print(labyrinthe.grid)