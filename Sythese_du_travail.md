# Règle du jeu :
Remplir une grille en respectant deux restrictions :
1. Deux chiffres identiques ne peuvent être voisins (même en diagonale)
2. Une cage de taille N doit contenir tous les chiffres de 1 à N

*NB : cf l'exemple donné dans la présentation pour voir à quoi ressemble concrètement une grille*
# Description du projet :
 - Réalisation d'un algorithme de résolution du jeu Kemaru par recherche du plus court chemin de résolution
 - Réalisation d'une interface graphique pour l'utilisateur
 - Utilisation des deux algorithmes pour pouvoir donner des indices pertinents à un joueur bloqué dans la résolution d'une grille

# Répartition du travail
## Membres du groupe
- Raphaël Oculi
- Raphaël Poux
- Gabriel Patry
- Mathis Verdan

## Organisation du travail
 1. Début de la partie algorithmique (niveau 0) avec tout le groupe sur Liveshare
 2. Raphaël P. et Gabriel &rarr; travail sur l'interface graphique / Raphaël O. et Mathis &rarr; travail sur la partie algorithmique
 3. Mise en commun des travaux avec github

# Partie algorithmique 
Ce paragraphe a pour but de détailler l'algorithme de résolution du jeu, notamment en donnant des détails sur le fichier `solver.py`. 

## Différents raisonnements

Pour résoudre une grille de Kemaru de façon algorithmique, on emploie différents raisonnements appelés **niveau 0, 1 et 2**.

### Niveau 0
Ce raisonnement consiste à appliquer simplement les règles du jeu : il faut pour cela **propager les informations** des cases déjà remplies vers les cases vides pour en faire des déductions. 

> *Exemple :* Si dans une cage de taille 3, une case possède un 1 et un 2 comme voisins, on en déduit que la case contient forcément un 3.

### Niveau 1
Il se peut qu'à l'issue du niveau 0 certaines cases de la grille restent vides. Il faut utiliser un raisonnement plus complexe pour trouver leur valeur. Le niveau 1 consiste à **supposer la valeur d'une des cases** parmi les valeurs possibles que celle-ci peut prendre et à en tirer des conclusions en appliquant ensuite un niveau 0. 

Si la case de coordonnées *(i,j)* peut prendre N valeurs différentes, le niveau 1 va tester toutes ces valeurs successivement et voir si cela apporte des nouvelles informations.

> *Exemple 1 :* Si, pour une certaine case notée A, on hésite entre les valeurs 1 et 4, alors le niveau 1 va créer deux *univers parallèles*. L'un dans lequel la case contient un 2, et l'autre dans lequel elle contient un 4. Comme la grille n'a qu'une solution, il y a forcément un des deux *univers* qui est faux (mais on ne le sait pas encore). On propage ensuite les informations "la case est un 2" et "la case est un 4" dans les deux univers. Si l'on s'aperçoit que l'univers "la case est un deux" donne une grille impossible (avec par exemple une case B dans laquelle on ne peut mettre aucune valeur), alors on sait que la case A comporte finalement un 4. 

> *Exemple 2 :* Même situation, on hésite entre mettre un 2 ou un 4 dans une des cases, toujours notée A. Cette fois, la propagation des informations dans les deux *univers parallèles* ne donne pas de contradictions (il reste des cases vides dans les deux univers et on ne sait pas encore lequel est faux, car on n'a pas assez d'informations pour détecter une contradiction). Toutefois, imaginons que dans une autre case de la grille notée B (vide avant l'application du niveau 1, et qui peut prendre les valeurs 1,2, 3 et 4 par exemple) la propagation des informations donne le résultat suivant : 
> - dans l'univers "la case A est un 2", on arrive à remplir la case B par un 1
> - dans l'univers "la case A est un 4", on arrive à remplir la case B par un 3
>
> Alors en regardant les deux univers parallèles, on constate que la case B ne prend jamais les valeurs 2 et 4, ce qui signifie que les valeurs possibles pour cette case passent de 1,2,3,4 à 1,3. 
>
> On a ici réduit les possibilités pour une case en faisant **l'union** des valeurs possibles trouvées dans les univers parallèles. Ce genre de déduction permet potentiellement de tirer de nouvelles conclusions en appliquant un niveau 0 ou un autre niveau 1 après l'union. 

Ces deux exemples simples illustrent la puissance du niveau 1, qui consiste finalement à **faire des suppositions** et à **combiner les informations en faisant l'union des valeurs possibles des "univers parallèles**.

### Niveau 2
Lorsque le niveau 1 ne parvient pas à résoudre la grille, on passe au niveau 2. Ici, au lieu de regarder toutes les possibilités pour une des cases, on regarde toutes les possibilités pour un **couple de cases** (ce qui fait vite beaucoup de possibilités). De la même manière, on propage les informations avec un niveau 0 après chaque hypothèse.

### Niveau 3, 4, ..., N ? 
On pourrait continuer ainsi en supposant 3, 4 ... N cases si le niveau 2 ne suffit pas. En réalité, en testant de nombreuses grilles (un échantillon de 23 580 grilles de différents niveaux), on s'est aperçu que le niveau 2 permettait de toutes les résoudre (cf le tableau de la diapo 18 de la soutenance). Il n'est donc pas nécessaire d'aller au-delà du niveau 2 qui est déjà assez lourd à calculer. 

*NB : certaines des grilles testées étaient loin d'être faciles (elles étaient même très difficiles), ce qui nous permet de penser que le niveau 2 suffit pour toutes les grilles qui existent*

