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

**NB :** Quand on dit que l'on "propage des informations", cela signifie qu'on fait un niveau 0 (on applique les règles du jeu à la grille). Donc en réalité, le niveau 1 inclut automatiquement un niveau 0.

### Niveau 2
Lorsque le niveau 1 ne parvient pas à résoudre la grille, on passe au niveau 2. Ici, au lieu de regarder toutes les possibilités pour une des cases, on regarde toutes les possibilités pour un **couple de cases** (ce qui fait vite beaucoup de possibilités). De la même manière, on propage les informations avec un niveau 0 après chaque hypothèse.

### Niveau 3, 4, ..., N ? 
On pourrait continuer ainsi en supposant 3, 4 ... N cases si le niveau 2 ne suffit pas. En réalité, en testant de nombreuses grilles (un échantillon de 23 580 grilles de différents niveaux), on s'est aperçu que le niveau 2 permettait de toutes les résoudre (cf le tableau de la diapo 18 de la soutenance). Il n'est donc pas nécessaire d'aller au-delà du niveau 2 qui est déjà assez lourd à calculer. 

*NB : certaines des grilles testées étaient loin d'être faciles (elles étaient même très difficiles), ce qui nous permet de penser que le niveau 2 suffit pour toutes les grilles qui existent*

## Plus court chemin 
La recherche du plus court chemin de résolution est utile pour donner des indices pertinents à l'utilisateur. On peut en effet se dire qu'au lieu de dévoiler une case au hasard en guise d'indice, il est plus efficace de diriger l'utilisateur vers une étape de raisonnement clef (par exemple en montrant sur quelle case réfléchir). On peut obtenir cela en partant du principe que les étapes du plus court chemin de résolution sont aussi les plus faciles à faire pour un humain. 

### Dijkstra, ou presque ...
Pour trouver le plus court chemin, on calcule le "coût" (détails ci-dessous) de chaque étape (niveau 0, niveau 1 sur telle case ...) pour construire le graphe du jeu. Pour la première étape, l'algorithme prend la grille initiale et essaie tous les coups possibles (niveau 0, niveau 1 sur la case (0,0), niveau 1 sur la case (1,0) ... ), en gardant en mémoire le résulat de chaque coup. Une fois tous les coups possibles appliquées, l'algorithme sélectionne le coup dont le coût est le plus faible, puis il refait pareil à partir de la grille initiale à laquelle on a appliqué le coup. 

> *Exemple :* Supposons que le coup de plus faible coût soit un niveau 1 sur la case (1,1), que ce coup coûte 100, et que la grille résultant de ce coup s'appelle A. Alors le programme applique ensuite à A tous les coups possibles, en gardant en mémoire les résultats de ces coups ainsi que le coût résultant. Dans ce cas, si on applique à A un niveau 1 de coût 50, le coût résultant sera 100+50 (supposons aussi que ce soit le coup  de plus faible coût). 
>
> A la prochaine itération, si la grille n'est pas résolue, il faudra repartir de la grille dont le coup est le plus faible. Peut-être que celle-ci sera A + le niveau 1 de coût 50, mais peut-être que cette grille sera celle résultant d'un autre coup que A (disons un coup B de coût 120). 

Cet algorithme nous assure de trouver le chemin de résolution minimisant le coût.

### Le coût
Dans notre algorithme, le coût est défini assez simplement : dès que l'on se sert d'une case pour éliminer une valeur possible dans les cases voisines, on augmente le coût de 1 (cela revient à compter les comparaisons que l'on fait). 

Pour le niveau 1, on choisit de rajouter un coût supplémentaire (car un niveau 1 est plus difficile à faire de tête) pénalisant les cases où il y a beaucoup de valeurs possibles. Il est en effet plus logique pour un humain de regarder une case où il hésite entre deux valeurs plutôt qu'une case où il hésite entre 5 valeurs. 

De même, pour des raisons de rapidité, nous avons choisi de faire un niveau 2 seulement si les niveaux 0 et 1 ne sont pas suffisants. Il est en effet très long de calculer tous les niveaux 2 possibles, et il est très difficile pour un humain de réfléchir à un niveau 2. Donc autant rediriger les joueurs vers les niveaux 2 le moins souvent possible.

## Implémentation
### Les dictionnaires/array utiles
Pour repésenter le jeu, nous utilisons plusieurs dictionnaires et array numpy car certaines représentations sont plus utiles que d'autres selon les situations.

**La grille** : c'est un array tel que `grille[i][j] = [valeur, n° de la cage]`, et où i, j sont les coordonnées spatiales de la case.

**Le dictionnaire d/dico** : dans le solveur, tous les dictionnaires qui s'appellent d ou dico <small>(il faut reconnaître que le nom n'est pas terrible)</small> désignent un objet d'une forme bien particulière : 
```python
d[i][j] = [True, True, False, False, True] #exemple 1 
d[i][j] = [True, False, False] #exemple 2
```
Dans l'exemple 1, la case (i,j) est dans une cage de taille 5 et il est possible de mettre un 1, un 2 ou un 5. 

Dans l'exemple 2, la case (i,j) est dans une cage de taille 3 et il est possible d'y mettre un 1 uniquement (donc la case contient un 1).

**TODO : la suite !!**

**Dico_est_trouve**

**Dico_taille**

**Taille**

**Dico_voisins**

## Implémentations des différents niveaux

## Le plus court chemin

## Quelques difficultés

## Améliorations du plus court chemin
# Partie interface
Ce paragraphe a pour but de détailler la façon dont la grille et les différentes profondeurs de résolution seront représentés, sans considérations sur l'implémentation de cette interface, qui a été codé avec pygame.

## Interface joueur
Deux modes de jeu distincts ont étés implémentés. Le premier permet a joueur de résoudre la grille par lui-même. Il peut pour s'aider afficher les possibilités dans chaque case et les éliminer manuellement.

## Représentation des différents niveaux
Le second mode de jeu permet de voir le chemin de résolution d'une grille par l'algorithme précedemment décrit. Seuls des représentations pour les niveaux 0 et 1 ont étés implémentés, par soucis de lisibilité. Cela suffit pour résoudre la plupart des grilles de Kemaru disponibles. 

### Représentation du niveau 0
Pour représenter le niveau 0, la case qui gagne de l'information en perdant une possibililité est affichée en bleu tandis que la ou les cases utilisés pour déterminer cette information sont affichées en rouge. Le joueur fait avancer la résolution en presssant la touche S.

### Représentation du niveau 1
Pour représenter le niveau 1, on scinde la grille en autant de possibilités que comporte la case de laquelle part la résolution ( celle sur laquelle différentes hypothèses sont faites ). Une résolution de niveau 0 s'engage alors sur chaqu'une de ces grilles. Pour faciliter l'affichage de plusieurs grilles, toutes celles-ci sont déformés pour être carrés.

### (non implémenté) Représentation des niveau supérieurs
Pour n'importe quel autre niveau, le seul paramètre qui change par rapport au niveau 1 est le nombre potentiel de possibilités. On pourrait alors représenter n'importe quel niveau de résolution en scindant la grille en autant de possibilité que d'hypothèse que l'algorithme de résolution fait sur une (on a alors une résolution de niveau 1) ou plusieurs cases.


